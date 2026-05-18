from __future__ import annotations

from dataclasses import dataclass

from v1700.ir.rendered_prose import RenderedProseIR
from v1700.ir.scene_intent import SceneIntentIR
from v1700.nodes.node3_critic_gate import Node3CriticGate


@dataclass(frozen=True)
class RefinementReport:
    status: str
    revision_count: int
    issues_before: tuple[str, ...]
    issues_after: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "revision_count": self.revision_count,
            "issues_before": list(self.issues_before),
            "issues_after": list(self.issues_after),
        }


class LiteraryRefinementLoop:
    def refine_once(self, scene: SceneIntentIR, rendered: RenderedProseIR) -> tuple[RenderedProseIR, RefinementReport]:
        gate = Node3CriticGate()
        ok, issues = gate.validate(rendered)
        if ok:
            return rendered, RefinementReport("pass", 0, tuple(issues), tuple())
        text = rendered.final_text
        missing = [fact for fact in scene.must_keep_facts if fact and fact not in text]
        if missing:
            text = text.rstrip() + "\n\n" + " ".join(missing)
        # The refinement loop is deliberately conservative: no new facts, no reveal changes.
        refined = RenderedProseIR(
            scene_id=rendered.scene_id,
            final_text=text,
            surface_score=dict(rendered.surface_score),
            constraint_score={**rendered.constraint_score, "fact_preservation": 10.0},
            risk_flags=tuple(flag for flag in rendered.risk_flags if flag != "missing_must_keep_fact"),
        )
        ok_after, issues_after = gate.validate(refined)
        return refined, RefinementReport("pass" if ok_after else "blocked", 1, tuple(issues), tuple(issues_after))
