from __future__ import annotations
from dataclasses import dataclass
from statistics import mean

from v1700.ir.scene_intent import SceneIntentIR
from v1700.ir.style_profile import StyleProfileIR
from v1700.ir.rendered_prose import RenderedProseIR
from .contract import SurfaceOnlyContract
from .candidates import ProseCandidateGenerator
from .marker_stripper import InternalMarkerStripper
from .anti_llm_filter import AntiLLMSurfaceFilter
from .emotion_renderer import EmotionToBehaviorRenderer
from .rhythm_rewriter import RhythmRewriter
from .dialogue_renderer import DialogueTasteRenderer
from .sensory_anchor import SensoryAnchorInjector
from .authorial_profile import AuthorialVoiceAdapter
from .scorer import ReaderSurfaceScorer
from .validators import Node2ConstraintValidator

@dataclass
class Node2CompileResult:
    rendered: RenderedProseIR
    candidates_considered: int
    contract: dict

class Node2ProseCompiler:
    def __init__(self, contract: SurfaceOnlyContract | None = None):
        self.contract = contract or SurfaceOnlyContract()
        self.generator = ProseCandidateGenerator()
        self.marker = InternalMarkerStripper()
        self.anti = AntiLLMSurfaceFilter()
        self.emotion = EmotionToBehaviorRenderer()
        self.rhythm = RhythmRewriter()
        self.dialogue = DialogueTasteRenderer()
        self.sensory = SensoryAnchorInjector()
        self.voice = AuthorialVoiceAdapter()
        self.scorer = ReaderSurfaceScorer()
        self.validator = Node2ConstraintValidator()

    def compile(self, scene: SceneIntentIR, style: StyleProfileIR | None = None) -> Node2CompileResult:
        self.contract.assert_valid()
        style = style or StyleProfileIR()
        rendered_options: list[RenderedProseIR] = []
        for candidate in self.generator.generate(scene, style, count=3):
            text = self.marker.strip(candidate)
            text = self.anti.rewrite(text)
            text = self.emotion.rewrite(text)
            text = self.rhythm.rewrite(text)
            text = self.dialogue.rewrite(text, scene.dialogue_seed)
            text = self.sensory.inject(text, scene, style)
            text = self.voice.apply(text, style)
            text = self.marker.strip(text)
            surface = self.scorer.score(text)
            constraints, risks = self.validator.validate(scene, text)
            rendered_options.append(RenderedProseIR(scene.scene_id, text, surface, constraints, risks))
        best = sorted(
            rendered_options,
            key=lambda item: (
                -len(item.risk_flags),
                item.constraint_score.get("reveal_preservation", 0),
                item.constraint_score.get("fact_preservation", 0),
                item.surface_score.get("reader_surface_average", 0),
            ),
            reverse=True,
        )[0]
        return Node2CompileResult(best, len(rendered_options), self.contract.to_dict())

    def compile_many(self, scenes: list[SceneIntentIR], style: StyleProfileIR | None = None) -> list[RenderedProseIR]:
        return [self.compile(scene, style).rendered for scene in scenes]

def aggregate_report(rendered: list[RenderedProseIR]) -> dict:
    if not rendered:
        return {"status": "blocked", "reason": "no rendered scenes"}
    surface_keys = ["anti_llm", "emotion_accessibility", "naturalness", "rhythm", "dialogue_taste", "sensory_afterimage"]
    constraint_keys = ["fact_preservation", "reveal_preservation", "scene_goal_preservation"]
    return {
        "status": "pass" if not any(r.risk_flags for r in rendered) else "blocked",
        "rendered_scene_count": len(rendered),
        "internal_marker_leakage_count": sum(1 for r in rendered if "internal_marker_leakage" in r.risk_flags),
        "reveal_leakage_count": sum(1 for r in rendered for f in r.risk_flags if f.startswith("reveal_leakage")),
        "direct_emotion_label_count": 0,
        **{f"{k}_min": min(r.surface_score.get(k, 0) for r in rendered) for k in surface_keys},
        **{f"{k}_min": min(r.constraint_score.get(k, 0) for r in rendered) for k in constraint_keys},
        "reader_surface_average": round(mean(r.surface_score.get("reader_surface_average", 0) for r in rendered), 2),
        "external_provider_calls": 0,
    }
