from __future__ import annotations

from v1700.episode_scaleup.evidence import EpisodeScaleupEvidenceEngine
from v1700.narrative_physics.belief_state import BeliefStateEngine
from v1700.narrative_physics.branchpoint_dynamics import BranchpointSurvivalDynamics
from v1700.narrative_physics.conflict_collision import ConflictCollisionCalculus
from v1700.narrative_physics.curiosity_gradient import AudienceCuriosityGradientEngine
from v1700.narrative_physics.emotional_dynamics import EmotionalMomentumDynamicsEngine
from v1700.narrative_physics.motif_residue import MotifResidueGraphBuilder
from v1700.narrative_physics.report import Stage95NarrativePhysicsReport
from v1700.narrative_physics.reveal_entropy import RevealEntropyBudgetEngine
from v1700.narrative_physics.scene_energy import SceneEnergyConservationAudit
from v1700.narrative_physics.state_tensor import NarrativeStateTensorBuilder
from v1700.narrative_physics.surface_transform import Node2SurfaceTransformGuard


class NativeNarrativePhysicsEngine:
    """Stage95 deterministic local narrative physics layer."""

    def run(self, *, episode_count: int = 16, scenes_per_episode: int = 10) -> Stage95NarrativePhysicsReport:
        season = EpisodeScaleupEvidenceEngine().build(episode_count=episode_count, scenes_per_episode=scenes_per_episode).to_dict()
        tensor = NarrativeStateTensorBuilder().build(season)
        belief = BeliefStateEngine().build(season)
        reveal = RevealEntropyBudgetEngine().calculate(season)
        emotional = EmotionalMomentumDynamicsEngine().evaluate(season)
        conflict = ConflictCollisionCalculus().evaluate(season)
        energy = SceneEnergyConservationAudit().audit(season)
        motif = MotifResidueGraphBuilder().build(season)
        curiosity = AudienceCuriosityGradientEngine().calculate(season)
        surface = Node2SurfaceTransformGuard().audit(season)
        branchpoints = BranchpointSurvivalDynamics().evaluate({})

        checks = {
            "season_evidence": season.get("status", "blocked"),
            "reveal_entropy": reveal.status,
            "emotional_momentum": emotional.status,
            "conflict_collision": conflict.status,
            "scene_energy": energy.status,
            "motif_residue": motif.status,
            "curiosity_gradient": curiosity.status,
            "surface_guard": surface.status,
            "branchpoint_survival": branchpoints.status,
        }
        issues = [name for name, status in checks.items() if status != "pass"]
        if len(tensor.vectors) < episode_count * scenes_per_episode:
            issues.append("narrative_state_tensor_scene_matrix_incomplete")
        if any(vector.leakage_count for vector in belief):
            issues.append("belief_state_leakage")
        if season.get("provider_default_calls") != 0:
            issues.append("provider_default_calls_not_zero")
        if season.get("node2_raw_reveal_access_count") != 0:
            issues.append("node2_raw_reveal_access_not_zero")

        return Stage95NarrativePhysicsReport(
            stage="95",
            status="pass" if not issues else "blocked",
            tensor=tensor,
            belief_vectors=belief,
            reveal_entropy=reveal,
            emotional_momentum=emotional,
            conflict_collision=conflict,
            scene_energy=energy,
            motif_residue=motif,
            curiosity_gradient=curiosity,
            surface_guard=surface,
            branchpoint_survival=branchpoints,
            provider_default_calls=0,
            live_provider_call_count=0,
            node2_raw_reveal_access_count=surface.node2_raw_reveal_access_count,
            issues=tuple(issues),
        )


def run_stage95_narrative_physics_smoke() -> dict:
    return NativeNarrativePhysicsEngine().run().to_dict()
