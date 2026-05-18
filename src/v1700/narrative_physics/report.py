from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from v1700.narrative_physics.belief_state import CharacterBeliefStateVector
from v1700.narrative_physics.branchpoint_dynamics import BranchpointSurvivalReport
from v1700.narrative_physics.conflict_collision import ConflictCollisionReport
from v1700.narrative_physics.curiosity_gradient import AudienceCuriosityGradientReport
from v1700.narrative_physics.emotional_dynamics import EmotionalMomentumReport
from v1700.narrative_physics.motif_residue import MotifResidueReport
from v1700.narrative_physics.reveal_entropy import RevealEntropyReport
from v1700.narrative_physics.scene_energy import SceneEnergyReport
from v1700.narrative_physics.state_tensor import NarrativeStateTensor
from v1700.narrative_physics.surface_transform import SurfaceTransformGuardReport


@dataclass(frozen=True)
class Stage95NarrativePhysicsReport:
    stage: str
    status: str
    tensor: NarrativeStateTensor
    belief_vectors: tuple[CharacterBeliefStateVector, ...]
    reveal_entropy: RevealEntropyReport
    emotional_momentum: EmotionalMomentumReport
    conflict_collision: ConflictCollisionReport
    scene_energy: SceneEnergyReport
    motif_residue: MotifResidueReport
    curiosity_gradient: AudienceCuriosityGradientReport
    surface_guard: SurfaceTransformGuardReport
    branchpoint_survival: BranchpointSurvivalReport
    provider_default_calls: int
    live_provider_call_count: int
    node2_raw_reveal_access_count: int
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage,
            "status": self.status,
            "tensor": self.tensor.to_dict(),
            "belief_vectors": [vector.to_dict() for vector in self.belief_vectors],
            "reveal_entropy": self.reveal_entropy.to_dict(),
            "emotional_momentum": self.emotional_momentum.to_dict(),
            "conflict_collision": self.conflict_collision.to_dict(),
            "scene_energy": self.scene_energy.to_dict(),
            "motif_residue": self.motif_residue.to_dict(),
            "curiosity_gradient": self.curiosity_gradient.to_dict(),
            "surface_guard": self.surface_guard.to_dict(),
            "branchpoint_survival": self.branchpoint_survival.to_dict(),
            "provider_default_calls": self.provider_default_calls,
            "live_provider_call_count": self.live_provider_call_count,
            "node2_raw_reveal_access_count": self.node2_raw_reveal_access_count,
            "issues": list(self.issues),
        }


def build_stage95_narrative_physics_manifest() -> dict[str, Any]:
    return {
        "stage": "95",
        "title": "V1700 Native Narrative Physics Engine",
        "status": "pass_pending_export",
        "modules": [
            "Narrative State Tensor",
            "Character Belief-State Vector",
            "Reveal Entropy Budget",
            "Emotional Momentum Dynamics",
            "Conflict Collision Calculus",
            "Scene Energy Conservation",
            "Motif Residue Graph",
            "Audience Curiosity Gradient",
            "Node2 Surface Transform Guard",
            "Branchpoint Survival Dynamics",
        ],
        "provider_default_calls": 0,
        "live_provider_call_count": 0,
        "node2_raw_reveal_access_count": 0,
    }
