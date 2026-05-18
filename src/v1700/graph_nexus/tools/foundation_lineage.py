from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


EVIDENCE_LEVELS = ("E1_DOCUMENT", "E2_ARTIFACT", "E3_EXECUTABLE", "E4_TESTED", "E5_LIVE_CURRENT")
SURVIVAL_STATUSES = (
    "LIVE_RUNTIME",
    "LIVE_GATE_ONLY",
    "PARTIAL",
    "DOCUMENTED_ONLY",
    "DEFERRED",
    "REJECTED_WITH_REASON",
    "UNKNOWN_NEEDS_REVIEW",
)

_STAGE_RE = re.compile(r"stage[_-]?([0-3]?\d)(?:[_\.-]|$)", re.IGNORECASE)
_EVIDENCE_SUFFIXES = {
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
    ".ts",
    ".tsx",
    ".zip",
    ".tar",
    ".gz",
}
_KEYWORDS = (
    "series_arc",
    "style_evolution",
    "temporal_delta",
    "pressure",
    "commit_rollback",
    "longform_scene_sequence",
    "provider_trace",
    "multi_provider",
    "boundary",
    "review",
    "concept_validation",
    "episode_draft",
    "memory_conflict",
    "literary_depth",
)


@dataclass(frozen=True)
class ConceptCard:
    concept_id: str
    stage_origins: tuple[str, ...]
    title: str
    problem_solved: str
    source_evidence: tuple[str, ...]
    evidence_level: str
    survival_status: str
    current_runtime_anchor: tuple[str, ...] = ()
    current_test_anchor: tuple[str, ...] = ()
    current_gate_anchor: tuple[str, ...] = ()
    current_doc_anchor: tuple[str, ...] = ()
    missing_runtime_work: tuple[str, ...] = ()
    promotion_priority: str = "MEDIUM"
    review_notes: str = ""

    def to_dict(self) -> dict:
        return {
            "concept_id": self.concept_id,
            "stage_origins": list(self.stage_origins),
            "title": self.title,
            "problem_solved": self.problem_solved,
            "source_evidence": list(self.source_evidence),
            "evidence_level": self.evidence_level,
            "current_runtime_anchor": list(self.current_runtime_anchor),
            "current_test_anchor": list(self.current_test_anchor),
            "current_gate_anchor": list(self.current_gate_anchor),
            "current_doc_anchor": list(self.current_doc_anchor),
            "survival_status": self.survival_status,
            "missing_runtime_work": list(self.missing_runtime_work),
            "promotion_priority": self.promotion_priority,
            "review_notes": self.review_notes,
        }


def find_gpt_workspace_root(root: Path) -> Path:
    for parent in (root, *root.parents):
        if parent.name.lower() == "gpt":
            return parent
    return root


def find_knowledge_base_root(root: Path) -> Path:
    workspace = find_gpt_workspace_root(root)
    return workspace / "knowledge_base" / "v1650_stage35_critic_comparison_gate"


def scan_pre_stage40_evidence(root: Path, limit: int = 500) -> dict:
    kb = find_knowledge_base_root(root)
    artifacts = []
    if not kb.exists():
        return {
            "status": "blocked",
            "source_root": str(kb),
            "reason": "knowledge_base_missing",
            "artifacts": [],
        }

    for path in sorted(p for p in kb.rglob("*") if p.is_file()):
        if "__pycache__" in path.parts:
            continue
        if path.suffix.lower() not in _EVIDENCE_SUFFIXES:
            continue
        rel = path.relative_to(kb).as_posix()
        lowered = rel.lower()
        stage = _stage_id_from_path(rel)
        keyword_hit = any(keyword in lowered for keyword in _KEYWORDS)
        if stage is None and not keyword_hit:
            continue
        artifacts.append(
            {
                "path": rel,
                "stage_id": stage,
                "artifact_type": _artifact_type(path),
                "bytes": path.stat().st_size,
            }
        )
        if len(artifacts) >= limit:
            break

    return {
        "status": "pass" if artifacts else "blocked",
        "generated_at": _now(),
        "source_root": str(kb),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }


def build_pre_stage40_lineage_manifest(root: Path) -> dict:
    concepts = [concept.to_dict() for concept in _foundation_concepts()]
    return {
        "stage": "72.3",
        "name": "Pre-Stage40 Foundation Lineage Manifest",
        "generated_at": _now(),
        "knowledge_base_root": str(find_knowledge_base_root(root)),
        "evidence_levels": list(EVIDENCE_LEVELS),
        "survival_statuses": list(SURVIVAL_STATUSES),
        "concept_count": len(concepts),
        "concepts": concepts,
    }


def write_foundation_lineage_artifacts(root: Path) -> dict:
    raw_index = scan_pre_stage40_evidence(root)
    lineage = build_pre_stage40_lineage_manifest(root)

    outputs = {
        "raw_evidence_index": root / "manifests" / "pre_stage40_raw_evidence_index.json",
        "lineage_manifest": root / "manifests" / "pre_stage40_lineage_manifest.json",
        "foundation_doc": root / "docs" / "stages" / "stage_001_039_foundation.md",
        "foundation_wiki": root / "docs" / "generated" / "wiki" / "foundation_lineage_wiki.md",
        "foundation_skill": root / "docs" / "generated" / "skills" / "foundation_lineage_skill.md",
    }
    for path in outputs.values():
        path.parent.mkdir(parents=True, exist_ok=True)

    outputs["raw_evidence_index"].write_text(
        json.dumps(raw_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    outputs["lineage_manifest"].write_text(
        json.dumps(lineage, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    outputs["foundation_doc"].write_text(_foundation_doc(lineage), encoding="utf-8")
    outputs["foundation_wiki"].write_text(_foundation_wiki(lineage), encoding="utf-8")
    outputs["foundation_skill"].write_text(_foundation_skill(lineage), encoding="utf-8")

    return {
        "status": "pass" if raw_index["status"] == "pass" else "blocked",
        "stage": "72.3",
        "outputs": {name: str(path) for name, path in outputs.items()},
        "artifact_count": raw_index.get("artifact_count", 0),
        "concept_count": lineage["concept_count"],
    }


def required_concept_ids() -> tuple[str, ...]:
    return tuple(concept.concept_id for concept in _foundation_concepts() if concept.promotion_priority == "HIGH")


def _stage_id_from_path(value: str) -> str | None:
    match = _STAGE_RE.search(value)
    if not match:
        return None
    number = int(match.group(1))
    if 1 <= number <= 39:
        return f"STAGE{number:02d}"
    return None


def _artifact_type(path: Path) -> str:
    name = path.name.lower()
    if "test_" in name or name.startswith("test"):
        return "test"
    if "manifest" in name:
        return "manifest"
    if "report" in name:
        return "report"
    if path.suffix.lower() == ".py":
        return "executable"
    if path.suffix.lower() in {".zip", ".tar", ".gz"}:
        return "package"
    return "document"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _foundation_concepts() -> tuple[ConceptCard, ...]:
    return (
        ConceptCard(
            concept_id="foundation.provider.multi_provider_creative_comparison",
            stage_origins=("STAGE10",),
            title="Multi-Provider Creative Comparison",
            problem_solved="Compare provider outputs without letting one provider silently define quality.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage10_multi_provider_creative_comparison_manifest.json",),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/runtime/provider_boundary.py",),
            current_test_anchor=("tests/test_stage72_2_release_gate.py",),
            missing_runtime_work=("provider quality score normalization",),
            promotion_priority="MEDIUM",
        ),
        ConceptCard(
            concept_id="foundation.provider.execution_trace",
            stage_origins=("STAGE11",),
            title="Provider Execution Trace",
            problem_solved="Make provider calls auditable and quarantine unsafe or unexpected execution.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage11_provider_execution_trace_harness_manifest.json",),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/runtime/cost_ledger.py", "src/v1700/runtime/provider_boundary.py"),
            current_gate_anchor=("src/v1700/gates/release_gate.py",),
            missing_runtime_work=("full provider trace persistence",),
            promotion_priority="MEDIUM",
        ),
        ConceptCard(
            concept_id="foundation.authoring.end_to_end_scenario_runner",
            stage_origins=("STAGE12",),
            title="End-to-End Authoring Scenario Runner",
            problem_solved="Keep authoring behavior testable as a whole workflow rather than isolated snippets.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage12_end_to_end_authoring_scenario_runner_manifest.json",),
            evidence_level="E3_EXECUTABLE",
            survival_status="DOCUMENTED_ONLY",
            current_doc_anchor=("docs/stages/stage_001_039_foundation.md",),
            missing_runtime_work=("modern authoring scenario runner",),
            promotion_priority="LOW",
        ),
        ConceptCard(
            concept_id="foundation.memory.conflict_resolver",
            stage_origins=("STAGE13",),
            title="Memory Conflict Resolver",
            problem_solved="Detect and resolve canon memory conflicts before they poison longform continuity.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage13_memory_conflict_resolver_manifest.json",),
            evidence_level="E3_EXECUTABLE",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/ledgers/character_event_time.py", "src/v1700/ledgers/reveal_budget.py"),
            missing_runtime_work=("explicit conflict resolver gate",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.node2.literary_quality_engine",
            stage_origins=("STAGE14",),
            title="Node2 Literary Quality Engine",
            problem_solved="Evaluate prose for rhythm, indirect emotion, cliche control, and reader-facing quality.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage14_node2_literary_quality_engine_manifest.json",),
            evidence_level="E5_LIVE_CURRENT",
            survival_status="LIVE_RUNTIME",
            current_runtime_anchor=("src/v1700/nodes/node2_prose_renderer/compiler.py", "src/v1700/nodes/node2_prose_renderer/scorer.py"),
            current_test_anchor=("tests/unit/node2_prose_renderer/test_compiler.py",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.node2.literary_depth_calibration",
            stage_origins=("STAGE15",),
            title="Literary Depth Calibration",
            problem_solved="Keep generated prose from being merely fluent by scoring depth and afterimage.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage15_literary_depth_calibration_manifest.json",),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/nodes/node2_prose_renderer/scorer.py", "src/v1700/ir/style_profile.py"),
            current_test_anchor=("tests/unit/node2_prose_renderer/test_marker_and_emotion.py",),
            missing_runtime_work=("dedicated literary depth benchmark",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.memory.long_horizon_drift_stress",
            stage_origins=("STAGE16",),
            title="Long-Horizon Memory Drift Stress",
            problem_solved="Stress longform memory so reveal budgets and invariants do not collapse over episodes.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage16_long_horizon_memory_drift_stress_manifest.json",),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/ledgers/reveal_budget.py", "src/v1700/ledgers/character_event_time.py"),
            current_doc_anchor=("docs/concepts/reveal_budget_memory_guard.md",),
            missing_runtime_work=("long horizon regression fixture",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.review.authoring_workflow",
            stage_origins=("STAGE17",),
            title="Authoring Review Workflow",
            problem_solved="Make review and rewrite decisions durable instead of conversational only.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage17_authoring_review_workflow_manifest.json",),
            evidence_level="E3_EXECUTABLE",
            survival_status="DOCUMENTED_ONLY",
            current_doc_anchor=("docs/runbooks/organic_impact_review_protocol.md",),
            missing_runtime_work=("modern review workflow runtime",),
            promotion_priority="MEDIUM",
        ),
        ConceptCard(
            concept_id="foundation.review.human_agent_console",
            stage_origins=("STAGE18",),
            title="Human/Agent Review Console",
            problem_solved="Separate review authority and make agent judgment visible before promotion.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage18_human_review_console_manifest.json",),
            evidence_level="E3_EXECUTABLE",
            survival_status="DOCUMENTED_ONLY",
            current_doc_anchor=("docs/reviews/stage72_3_principal_engineer_validation.md",),
            missing_runtime_work=("agent review console adapter",),
            promotion_priority="MEDIUM",
        ),
        ConceptCard(
            concept_id="foundation.longform.episode_draft_export",
            stage_origins=("STAGE21",),
            title="Episode Draft Export Harness",
            problem_solved="Export episode-scale drafts as reviewable artifacts instead of transient model text.",
            source_evidence=(
                "archive/_cleanup_20260511/legacy_root_stage_artifacts/stage21_episode_draft_export_harness_manifest.json",
                "archive/_cleanup_20260511/legacy_root_stage_artifacts/stage21_harness_result.json",
            ),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_doc_anchor=("docs/stages/stage_050_052_longform_state_guards.md",),
            missing_runtime_work=("episode draft export command",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.longform.series_arc_control",
            stage_origins=("STAGE22",),
            title="Series Arc Control",
            problem_solved="Keep season and episode progression coherent beyond isolated scene generation.",
            source_evidence=(
                "archive/_cleanup_20260511/legacy_root_stage_artifacts/stage22_node1_series_arc_control_manifest.json",
                "archive/_cleanup_20260511/legacy_root_stage_artifacts/stage22_series_arc_harness_result.json",
            ),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/ir/scene_intent.py", "src/v1700/nodes/node1_architect/__init__.py"),
            current_doc_anchor=("docs/stages/stage_050_052_longform_state_guards.md",),
            missing_runtime_work=("season arc planner", "episode arc planner"),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.node2.style_evolution_memory",
            stage_origins=("STAGE23",),
            title="Node2 Style Evolution Memory",
            problem_solved="Preserve authorial taste and anti-LLM preferences across revision cycles.",
            source_evidence=(
                "archive/_cleanup_20260511/legacy_root_stage_artifacts/stage23_node2_style_evolution_memory_manifest.json",
                "archive/_cleanup_20260511/legacy_root_stage_artifacts/stage23_node2_style_memory_harness_result.json",
            ),
            evidence_level="E5_LIVE_CURRENT",
            survival_status="LIVE_RUNTIME",
            current_runtime_anchor=("src/v1700/ledgers/style_memory.py", "src/v1700/nodes/node2_prose_renderer/authorial_profile.py"),
            current_test_anchor=("tests/unit/node2_prose_renderer/test_compiler.py",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.governance.boundary_registry",
            stage_origins=("STAGE24",),
            title="Boundary Registry",
            problem_solved="Prevent node authority drift and forbidden knowledge leakage.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage24_1_1_boundary_registry_manifest.json",),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/graph_nexus/projection.py", "src/v1700/graph_nexus/graph_nexus_packet.py"),
            current_gate_anchor=("src/v1700/gates/graph_nexus_release_gate.py",),
            current_doc_anchor=("docs/architecture/node_authority_boundaries.md",),
            missing_runtime_work=("central boundary registry manifest",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.governance.release_candidate_gate",
            stage_origins=("STAGE25",),
            title="Release Candidate Gate",
            problem_solved="Require promotion evidence before a stage becomes a developer handoff candidate.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage25_release_candidate_manifest.json",),
            evidence_level="E5_LIVE_CURRENT",
            survival_status="LIVE_RUNTIME",
            current_gate_anchor=("src/v1700/gates/release_gate.py", "src/v1700/gates/stage72_2_release_gate.py"),
            current_test_anchor=("tests/test_stage72_2_release_gate.py",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.governance.stage26_28_regression_stream",
            stage_origins=("STAGE26", "STAGE27", "STAGE28"),
            title="Stage26-28 Regression Stream",
            problem_solved="Keep feedback, graph, retrieval, and regression decisions connected across patches.",
            source_evidence=(
                "archive/_cleanup_20260511/legacy_root_stage_artifacts/stage26_27_28_regression.py",
                "archive/_cleanup_20260511/legacy_root_tests/test_stage28_phase28_10_stage26_27_28_regression.py",
            ),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_test_anchor=("tests/integration/test_node1_node2_node3_pipeline.py",),
            current_gate_anchor=("src/v1700/gates/release_gate.py",),
            missing_runtime_work=("cross-stage regression matrix",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.governance.concept_validation_workbench",
            stage_origins=("STAGE33",),
            title="Concept Validation Workbench",
            problem_solved="Validate whether a concept should be promoted, deferred, or rejected.",
            source_evidence=("archive/_cleanup_20260511/legacy_root_stage_artifacts/stage33_all_validation_report.json",),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_doc_anchor=("docs/reviews/stage72_3_principal_engineer_validation.md",),
            current_gate_anchor=("src/v1700/gates/pre_stage40_survival_gate.py",),
            missing_runtime_work=("interactive concept workbench revival",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.evidence_intake_foundation",
            stage_origins=("STAGE39",),
            title="Evidence Intake Foundation",
            problem_solved="Convert raw evidence into structured packets before generation uses it.",
            source_evidence=("run_stage39_phase39_1_foundation.py",),
            evidence_level="E3_EXECUTABLE",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/graph_nexus/tools/context.py",),
            missing_runtime_work=("evidence intake queue integration",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.analyzer_librarian_integration",
            stage_origins=("STAGE39",),
            title="Analyzer/Librarian Integration",
            problem_solved="Separate analysis, indexing, and retrieval authority before generation.",
            source_evidence=("run_stage39_phase39_2_analyzer_librarian_integration.py",),
            evidence_level="E3_EXECUTABLE",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/graph_nexus/tools/query.py", "src/v1700/graph_nexus/tools/context.py"),
            missing_runtime_work=("librarian role runtime adapter",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.graph_retrieval_bridge",
            stage_origins=("STAGE39",),
            title="Graph Retrieval Bridge",
            problem_solved="Use graph context as evidence rather than free-floating prompt memory.",
            source_evidence=("run_stage39_phase39_3_graph_retrieval_bridge.py",),
            evidence_level="E3_EXECUTABLE",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/graph_nexus/registry.py", "src/v1700/graph_nexus/tools/query.py"),
            current_test_anchor=("tests/test_stage72_2_graph_nexus_operational_tools.py",),
            missing_runtime_work=("narrative GraphRAG retriever",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.temporal_continuity",
            stage_origins=("STAGE39",),
            title="Temporal Continuity",
            problem_solved="Apply time deltas so character and event state cannot contradict elapsed story time.",
            source_evidence=("run_stage39_phase39_4_temporal_continuity.py", "temporal_delta_controller.py"),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/ledgers/character_event_time.py", "src/v1700/ir/scene_intent.py"),
            missing_runtime_work=("temporal delta controller in Node1 planning route",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.longform_scene_sequence_planner",
            stage_origins=("STAGE39",),
            title="Longform Scene-Sequence Planner",
            problem_solved="Let scenes and sequences be organically calculated from story pressure and episode needs.",
            source_evidence=("run_stage39_phase39_5_longform_scene_sequence_planner.py", "longform_scene_sequence_planner.py"),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/ir/scene_intent.py",),
            current_doc_anchor=("docs/architecture/stage72_3_foundation_lineage_recovery_blueprint.md",),
            missing_runtime_work=("runtime sequence planner", "scene count estimator"),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.branch_commit_rollback",
            stage_origins=("STAGE39",),
            title="Branch Commit/Rollback",
            problem_solved="Prevent rejected shadow runs from contaminating main canon memory.",
            source_evidence=("run_stage39_phase39_6_branch_commit_rollback.py", "commit_rollback_protocol.py"),
            evidence_level="E4_TESTED",
            survival_status="DOCUMENTED_ONLY",
            current_doc_anchor=("docs/proposals/stage72_3_pre_stage40_lineage_recovery_proposal.md",),
            missing_runtime_work=("branch isolation runtime", "what-if archive policy"),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.emotional_pressure_valve",
            stage_origins=("STAGE39",),
            title="Emotional Pressure Valve",
            problem_solved="Control suspense and relief so longform drama does not become monotonous pressure.",
            source_evidence=(
                "run_stage39_phase39_7_emotional_pressure_valve.py",
                "pressure_threshold_monitor.py",
                "pressure_relief_event_planner.py",
            ),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_runtime_anchor=("src/v1700/ir/scene_intent.py", "src/v1700/nodes/node2_prose_renderer/emotion_renderer.py"),
            missing_runtime_work=("series-level emotional wave controller",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.node2_candidate_rendering",
            stage_origins=("STAGE39",),
            title="Node2 Candidate Rendering",
            problem_solved="Render multiple safe prose candidates before selecting the strongest reader-facing surface.",
            source_evidence=("run_stage39_phase39_8_node2_candidate_rendering.py",),
            evidence_level="E5_LIVE_CURRENT",
            survival_status="LIVE_RUNTIME",
            current_runtime_anchor=("src/v1700/nodes/node2_prose_renderer/candidates.py", "src/v1700/nodes/node2_prose_renderer/compiler.py"),
            current_test_anchor=("tests/unit/node2_prose_renderer/test_compiler.py",),
            promotion_priority="HIGH",
        ),
        ConceptCard(
            concept_id="foundation.stage39.actual_replay_reconvergence",
            stage_origins=("STAGE39",),
            title="Actual Replay Reconvergence",
            problem_solved="Replay and reconverge execution evidence so decisions remain reproducible.",
            source_evidence=("run_stage39_phase39_9_actual_replay_reconvergence.py",),
            evidence_level="E4_TESTED",
            survival_status="PARTIAL",
            current_test_anchor=("tests/integration/test_node1_node2_node3_pipeline.py",),
            current_gate_anchor=("src/v1700/gates/release_gate.py",),
            missing_runtime_work=("deterministic replay ledger",),
            promotion_priority="HIGH",
        ),
    )


def _foundation_doc(lineage: dict) -> str:
    rows = [
        "# Stage001-039 Foundation Lineage",
        "",
        "This document maps the early V1650 foundation concepts into the current V1700 runtime.",
        "",
        "| Concept | Stage origin | Evidence | Survival | Current anchor | Missing work |",
        "|---|---|---|---|---|---|",
    ]
    for concept in lineage["concepts"]:
        anchors = concept["current_runtime_anchor"] or concept["current_gate_anchor"] or concept["current_test_anchor"] or concept["current_doc_anchor"]
        rows.append(
            "| {title} | {stages} | {evidence} | {survival} | {anchors} | {missing} |".format(
                title=concept["title"],
                stages=", ".join(concept["stage_origins"]),
                evidence=concept["evidence_level"],
                survival=concept["survival_status"],
                anchors="<br>".join(anchors) if anchors else "none",
                missing="<br>".join(concept["missing_runtime_work"]) if concept["missing_runtime_work"] else "none",
            )
        )
    rows.extend(
        [
            "",
            "## Operating Rule",
            "",
            "Pre-Stage40 material is not restored by blind file copy. It is restored by concept survival mapping, source evidence, current anchors, and release gates.",
            "",
        ]
    )
    return "\n".join(rows)


def _foundation_wiki(lineage: dict) -> str:
    live = _count_status(lineage["concepts"], "LIVE_RUNTIME")
    partial = _count_status(lineage["concepts"], "PARTIAL")
    documented = _count_status(lineage["concepts"], "DOCUMENTED_ONLY")
    return "\n".join(
        [
            "# Foundation Lineage Wiki",
            "",
            f"Concepts classified: {lineage['concept_count']}",
            f"LIVE_RUNTIME: {live}",
            f"PARTIAL: {partial}",
            f"DOCUMENTED_ONLY: {documented}",
            "",
            "## High-Priority Recovery Groups",
            "",
            "- Longform generation: series arc, temporal continuity, sequence planning, pressure valve.",
            "- Literary quality: Node2 quality engine, depth calibration, style memory.",
            "- Governance: boundary registry, release gates, regression stream, concept validation.",
            "- Provider safety: multi-provider comparison, provider trace, local-first execution.",
            "",
            "## Next Feature Dependency",
            "",
            "The next longform season execution engine must consume this lineage before adding runtime planners.",
            "",
        ]
    )


def _foundation_skill(lineage: dict) -> str:
    high_priority = [c for c in lineage["concepts"] if c["promotion_priority"] == "HIGH"]
    concept_lines = "\n".join(f"- `{concept['concept_id']}`: {concept['survival_status']}" for concept in high_priority)
    return "\n".join(
        [
            "# Foundation Lineage Skill",
            "",
            "Use this skill when a change may affect pre-Stage40 literary generator logic.",
            "",
            "## Required Checks",
            "",
            "- Identify related `concept_id` entries in `manifests/pre_stage40_lineage_manifest.json`.",
            "- Verify source evidence exists in the knowledge base.",
            "- Verify LIVE/PARTIAL concepts still have runtime, gate, test, or doc anchors.",
            "- Run `python tools/run_pre_stage40_survival_gate.py` before promotion.",
            "",
            "## High-Priority Concepts",
            "",
            concept_lines,
            "",
        ]
    )


def _count_status(concepts: Iterable[dict], status: str) -> int:
    return sum(1 for concept in concepts if concept["survival_status"] == status)
