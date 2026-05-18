from __future__ import annotations

from v1700.graph_nexus.narrative_graph import NarrativeGraph, NarrativeNode, NarrativeEdge
from v1700.ir.style_profile import StyleProfileIR
from v1700.ledgers.character_event_time import CharacterEventTimeLedger
from v1700.ledgers.reveal_budget import RevealBudget
from v1700.literary_formulas import (
    DRSEEngine,
    DRSEInputNode,
    EmotionalMomentumTracker,
    MiseEnSceneCompiler,
    SceneGraphQueryEngine,
)
from v1700.nodes.node2_prose_renderer import Node2ProseCompiler
from .contracts import LongformExecutionReport
from .planners import LongformPlanBuilder, SceneExpansionEngine
from .refinement import LiteraryRefinementLoop


class LongformExecutionEngine:
    def __init__(self) -> None:
        self.plan_builder = LongformPlanBuilder()
        self.scene_expander = SceneExpansionEngine()
        self.drse = DRSEEngine()
        self.momentum = EmotionalMomentumTracker()
        self.mise = MiseEnSceneCompiler()
        self.renderer = Node2ProseCompiler()
        self.refiner = LiteraryRefinementLoop()

    def execute(self, prompt: str) -> LongformExecutionReport:
        plan = self.plan_builder.build(prompt)
        scenes = self.scene_expander.expand_first_scenes(plan)
        graph = NarrativeGraph.from_scene_intents(list(scenes))
        first = scenes[0]
        focus = SceneGraphQueryEngine().focus(graph, first.scene_id)
        nodes = list(focus.nodes) + [
            DRSEInputNode("stage39.execution", "legacy_causality", "temporal continuity branch rollback emotional pressure", ("causal", "legacy"), ("stage39",)),
            DRSEInputNode("stage50.three_episode", "macro_structure", "three episode proof season arc episode turn", ("causal", "motif"), ("stage50",)),
            DRSEInputNode("stage56.quality", "literary_quality", "reader surface rhythm emotion naturalness", ("emotion", "residue"), ("stage56",)),
        ]
        drse_context = self.drse.score(first.scene_goal, tuple(nodes))
        momentum = self.momentum.from_scene_terms(first.conflict, first.emotional_delta.from_state, first.emotional_delta.to_state)
        directive = self.mise.compile(first.scene_id, drse_context, momentum)
        style = StyleProfileIR(sensory_axis=("light", "temperature", "object_texture"))
        rendered = list(self.renderer.compile_many(list(scenes), style))
        refined, refinement = self.refiner.refine_once(first, rendered[0])
        rendered[0] = refined
        forbidden = set(item for scene in scenes for item in scene.forbidden_reveals)
        reveal_budget = RevealBudget(forbidden)
        leakage = [item for item in rendered for item in reveal_budget.leakage(item.final_text)]
        ledger = CharacterEventTimeLedger(
            facts=[fact for scene in scenes for fact in scene.must_keep_facts],
            timeline_position=scenes[-1].timeline_position,
        )
        issues: list[str] = []
        if leakage:
            issues.append("reveal_budget_leakage")
        if len(plan.episodes) != 3:
            issues.append("three_episode_plan_missing")
        return LongformExecutionReport(
            status="pass" if not issues and refinement.status == "pass" else "blocked",
            plan=plan,
            scenes=scenes,
            rendered=tuple(rendered),
            drse=drse_context.to_dict(),
            emotional_momentum=momentum.to_dict(),
            mise_en_scene=directive.to_dict(),
            ledger={"fact_count": len(ledger.facts), "timeline_position": ledger.timeline_position},
            reveal_budget={"forbidden_count": len(forbidden), "leakage": leakage},
            refinement=refinement.to_dict(),
            issues=tuple(issues),
            provider_default_calls=0,
            node2_raw_reveal_access_count=0,
        )


def run_longform_execution_smoke(prompt: str = "침묵한 조력자와 사라진 증거를 둘러싼 장편 드라마") -> dict:
    return LongformExecutionEngine().execute(prompt).to_dict()
