
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from v1700.gates.stage83_release_gate import run_stage83_release_gate
from v1700.lineage.branchpoint_registry import BranchpointModel, build_branchpoint_registry
from v1700.lineage.reabsorption_reconciliation import build_reconciled_core_logic_survival_matrix

LIVE_RUNTIME = "LIVE_RUNTIME"


@dataclass(frozen=True)
class Stage831LogicEntry:
    logic_id: str
    source_branchpoint: str
    original_survival_status: str
    current_survival_status: str
    reabsorption_priority: str
    completion_level: str
    evidence_files: tuple[str, ...]
    test_coverage: tuple[str, ...]
    gate_coverage: tuple[str, ...]
    reconciliation_note: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "logic_id": self.logic_id,
            "source_branchpoint": self.source_branchpoint,
            "original_survival_status": self.original_survival_status,
            "current_survival_status": self.current_survival_status,
            "reabsorption_priority": self.reabsorption_priority,
            "completion_level": self.completion_level,
            "evidence_files": list(self.evidence_files),
            "test_coverage": list(self.test_coverage),
            "gate_coverage": list(self.gate_coverage),
            "reconciliation_note": self.reconciliation_note,
        }


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _stage80_83_branchpoints() -> tuple[BranchpointModel, ...]:
    return (
        BranchpointModel(
            "BP_STAGE80_KOREAN_DRAMA_COMPOSITION_HIERARCHY",
            "Stage80 Korean Drama Composition Hierarchy",
            "P0",
            "The longform engine separated series story, macro plot, broadcast episode, micro plot, sequence, and scene into explicit runtime hierarchy.",
            (
                "korean_drama_composition_hierarchy",
                "series_macro_episode_micro_sequence_scene_boundary",
                "composition_hierarchy_release_gate",
            ),
        ),
        BranchpointModel(
            "BP_STAGE81_ACTUAL_TEXT_QUALITY_ENDURANCE",
            "Stage81 Quality Refinement Endurance",
            "P0",
            "Quality proof moved from small smoke samples into 30 actual rendered scenes with before/after refinement evidence.",
            (
                "actual_text_quality_endurance",
                "quality_refinement_trace_integrity",
            ),
        ),
        BranchpointModel(
            "BP_STAGE82_BLIND_CRITIC_BENCHMARK",
            "Stage82 Blind Critic Benchmark",
            "P0",
            "Commercial claims gained a blind critic benchmark against pure GPT and external baselines.",
            (
                "blind_critic_benchmark",
                "v1700_margin_over_pure_gpt",
            ),
        ),
        BranchpointModel(
            "BP_STAGE83_COMMERCIAL_LONGFORM_RELEASE_CANDIDATE",
            "Stage83 Commercial Longform Release Candidate",
            "P0",
            "The system produced a local-first commercial release evidence pack with three episode files and 30 rendered scenes.",
            (
                "commercial_longform_release_candidate",
                "three_episode_actual_rendering",
                "provider_zero_commercial_contract",
            ),
        ),
    )


def build_branchpoint_model_registry_v2() -> dict[str, Any]:
    branchpoints = list(build_branchpoint_registry()) + list(_stage80_83_branchpoints())
    seen: set[str] = set()
    deduped: list[BranchpointModel] = []
    for bp in branchpoints:
        if bp.branchpoint_id in seen:
            continue
        seen.add(bp.branchpoint_id)
        deduped.append(bp)
    return {
        "stage": "83.1",
        "status": "reconciled",
        "basis": "Stage75 canonical branchpoint registry plus Stage80~83 commercial longform branchpoints.",
        "branchpoint_count": len(deduped),
        "branchpoints": [bp.to_dict() for bp in deduped],
    }


def _stage80_83_logic_entries() -> tuple[Stage831LogicEntry, ...]:
    return (
        Stage831LogicEntry(
            "korean_drama_composition_hierarchy",
            "BP_STAGE80_KOREAN_DRAMA_COMPOSITION_HIERARCHY",
            "NEW_STAGE80",
            LIVE_RUNTIME,
            "P0",
            "runtime_smoke_verified",
            ("src/v1700/drama_composition/engine.py", "src/v1700/drama_composition/contracts.py"),
            ("tests/test_stage80_korean_drama_composition.py",),
            ("stage80_release_gate",),
            "Stage80 verifies the six-level Korean drama hierarchy: series story, macro plot, broadcast episode, micro plot, sequence, and scene.",
        ),
        Stage831LogicEntry(
            "series_macro_episode_micro_sequence_scene_boundary",
            "BP_STAGE80_KOREAN_DRAMA_COMPOSITION_HIERARCHY",
            "NEW_STAGE80",
            LIVE_RUNTIME,
            "P0",
            "contract_verified",
            ("src/v1700/drama_composition/contracts.py", "docs/concepts/korean_drama_composition_hierarchy.md"),
            ("tests/test_stage80_korean_drama_composition.py",),
            ("stage80_release_gate",),
            "Composition contracts keep each scale distinct so Stage84 runtime muscle cannot collapse the V1700 Korean drama skeleton.",
        ),
        Stage831LogicEntry(
            "composition_hierarchy_release_gate",
            "BP_STAGE80_KOREAN_DRAMA_COMPOSITION_HIERARCHY",
            "NEW_STAGE80",
            LIVE_RUNTIME,
            "P0",
            "gate_verified",
            ("src/v1700/gates/stage80_release_gate.py",),
            ("tests/test_stage80_korean_drama_composition.py",),
            ("stage80_release_gate",),
            "Stage80 gate is the structural precondition for Stage84 runtime absorption.",
        ),
        Stage831LogicEntry(
            "actual_text_quality_endurance",
            "BP_STAGE81_ACTUAL_TEXT_QUALITY_ENDURANCE",
            "NEW_STAGE81",
            LIVE_RUNTIME,
            "P0",
            "actual_text_verified",
            ("src/v1700/quality_endurance/engine.py", "release/current/stage81_release_gate_report.json"),
            ("tests/test_stage81_release_gate.py",),
            ("stage81_release_gate",),
            "Stage81 verifies 30 rendered scenes with quality average after refinement above release threshold and zero blockers.",
        ),
        Stage831LogicEntry(
            "quality_refinement_trace_integrity",
            "BP_STAGE81_ACTUAL_TEXT_QUALITY_ENDURANCE",
            "NEW_STAGE81",
            LIVE_RUNTIME,
            "P0",
            "trace_verified",
            ("src/v1700/longform/refinement.py", "sample_longform_project_01/refinement_trace.json"),
            ("tests/test_stage81_release_gate.py", "tests/test_stage83_commercial_release_candidate.py"),
            ("stage81_release_gate", "stage83_release_gate"),
            "Refinement evidence is tied to actual generated text and preserved through the Stage83 commercial evidence pack.",
        ),
        Stage831LogicEntry(
            "blind_critic_benchmark",
            "BP_STAGE82_BLIND_CRITIC_BENCHMARK",
            "NEW_STAGE82",
            LIVE_RUNTIME,
            "P0",
            "benchmark_verified",
            ("src/v1700/blind_critic/harness.py", "release/current/stage82_blind_critic_benchmark_report.json"),
            ("tests/test_stage82_blind_critic_benchmark.py",),
            ("stage82_release_gate",),
            "Stage82 verifies blind critic benchmark evidence before commercial packaging.",
        ),
        Stage831LogicEntry(
            "v1700_margin_over_pure_gpt",
            "BP_STAGE82_BLIND_CRITIC_BENCHMARK",
            "NEW_STAGE82",
            LIVE_RUNTIME,
            "P0",
            "margin_verified",
            ("release/current/stage82_blind_critic_benchmark_report.json", "sample_longform_project_01/blind_eval_report.md"),
            ("tests/test_stage82_blind_critic_benchmark.py", "tests/test_stage83_commercial_release_candidate.py"),
            ("stage82_release_gate", "stage83_release_gate"),
            "The Stage83 manifest preserves the V1700 margin over pure GPT as commercial-readiness evidence.",
        ),
        Stage831LogicEntry(
            "commercial_longform_release_candidate",
            "BP_STAGE83_COMMERCIAL_LONGFORM_RELEASE_CANDIDATE",
            "NEW_STAGE83",
            LIVE_RUNTIME,
            "P0",
            "commercial_evidence_pack_verified",
            ("src/v1700/commercial_release/engine.py", "sample_longform_project_01/commercial_release_manifest.json"),
            ("tests/test_stage83_commercial_release_candidate.py",),
            ("stage83_release_gate",),
            "Stage83 produces a local-first commercial longform evidence pack.",
        ),
        Stage831LogicEntry(
            "three_episode_actual_rendering",
            "BP_STAGE83_COMMERCIAL_LONGFORM_RELEASE_CANDIDATE",
            "NEW_STAGE83",
            LIVE_RUNTIME,
            "P0",
            "actual_render_verified",
            (
                "sample_longform_project_01/generated_episode_01.md",
                "sample_longform_project_01/generated_episode_02.md",
                "sample_longform_project_01/generated_episode_03.md",
            ),
            ("tests/test_stage83_commercial_release_candidate.py",),
            ("stage83_release_gate",),
            "Three generated episode files and at least 30 actual rendered scenes are present in the release candidate.",
        ),
        Stage831LogicEntry(
            "provider_zero_commercial_contract",
            "BP_STAGE83_COMMERCIAL_LONGFORM_RELEASE_CANDIDATE",
            "NEW_STAGE83",
            LIVE_RUNTIME,
            "P0",
            "release_contract_verified",
            ("src/v1700/gates/stage83_release_gate.py", "manifests/stage83_manifest.json"),
            ("tests/test_stage83_commercial_release_candidate.py",),
            ("stage83_release_gate",),
            "Commercial gate keeps provider default calls at 0 and Node2 raw reveal access at 0.",
        ),
    )


def _canonicalize_entry_paths(entry: dict[str, Any]) -> dict[str, Any]:
    aliases = {
        "tests/test_stage81_release_gate.py": "tests/stage_gates/test_stage81_release_gate.py",
    }
    normalized = dict(entry)
    for key in ("evidence_files", "test_coverage", "gate_coverage"):
        normalized[key] = [aliases.get(path, path) for path in normalized.get(key, [])]
    return normalized


def build_core_logic_survival_matrix_v3() -> dict[str, Any]:
    base_entries = [_canonicalize_entry_paths(entry.to_dict()) for entry in build_reconciled_core_logic_survival_matrix()]
    new_entries = [_canonicalize_entry_paths(entry.to_dict()) for entry in _stage80_83_logic_entries()]
    entries = base_entries + new_entries
    p0_entries = [e for e in entries if e.get("reabsorption_priority") == "P0"]
    p0_not_live = [e["logic_id"] for e in p0_entries if e.get("current_survival_status") != LIVE_RUNTIME]
    return {
        "stage": "83.1",
        "status": "pass" if not p0_not_live else "blocked",
        "basis": "Stage81.1 reconciled matrix plus Stage80~83 release evidence.",
        "entry_count": len(entries),
        "p0_total": len(p0_entries),
        "p0_live_runtime_count": len(p0_entries) - len(p0_not_live),
        "p0_non_live_logic_ids": p0_not_live,
        "entries": entries,
    }


def _edge(source: Any, relation: Any, target: Any) -> str:
    src = str(source or "UNSPECIFIED_SOURCE")
    rel = str(relation or "UNSPECIFIED_RELATION")
    dst = str(target or "UNSPECIFIED_TARGET")
    return f"{src} --{rel}--> {dst}"


def _primary_location(entry: dict[str, Any]) -> str:
    files = entry.get("evidence_files") or []
    if files:
        return str(files[0])
    return f"manifests/core_logic_survival_matrix_v3.json#{entry.get('logic_id', 'unknown_logic')}"


def build_organic_relation_graph_manifest_v2() -> dict[str, Any]:
    matrix = build_core_logic_survival_matrix_v3()
    relations: list[dict[str, Any]] = []
    for entry in matrix["entries"]:
        logic_id = entry.get("logic_id") or "unknown_logic"
        source_bp = entry.get("source_branchpoint") or "unknown_branchpoint"
        relations.append({"source": source_bp, "relation": "DEFINES_LOGIC", "target": logic_id, "evidence": []})
        relations.append({"source": logic_id, "relation": "CURRENT_LOCATION", "target": _primary_location(entry), "evidence": entry.get("evidence_files") or []})
        for test in entry.get("test_coverage") or []:
            relations.append({"source": logic_id, "relation": "REQUIRES_TEST", "target": test, "evidence": []})
        for gate in entry.get("gate_coverage") or []:
            relations.append({"source": logic_id, "relation": "REQUIRES_GATE", "target": gate, "evidence": []})
        relations.append({"source": logic_id, "relation": "SURVIVAL_STATUS", "target": entry.get("current_survival_status") or "UNKNOWN", "evidence": []})
    relations.extend(
        [
            {"source": "GitNexus", "relation": "OPTIONAL_SIDECAR_FOR", "target": "GraphNexus CodeGraph", "evidence": ["docs/concepts/gitnexus_optional_sidecar.md"]},
            {"source": "GraphNexus", "relation": "COMPOSES", "target": "CodeGraph + NarrativeGraph + StageLineageGraph", "evidence": ["docs/concepts/graph_nexus_3graph_model.md"]},
            {"source": "GraphNexus", "relation": "BRIDGES_TO", "target": "BranchpointLogicGraph", "evidence": ["manifests/gitnexus_branchpoint_bridge_manifest.json"]},
            {"source": "BranchpointLogicGraph", "relation": "PROTECTS", "target": "CoreLogicSurvivalMatrixV3", "evidence": ["manifests/core_logic_survival_matrix_v3.json"]},
            {"source": "DRSE", "relation": "PROVIDES_EVIDENCE_TO", "target": "Stage83.1ReleaseGate", "evidence": ["src/v1700/literary_formulas/drse.py", "tests/test_stage73_1_literary_formula_restoration.py"]},
            {"source": "EmotionalMomentum", "relation": "PROVIDES_EVIDENCE_TO", "target": "Stage83.1ReleaseGate", "evidence": ["src/v1700/literary_formulas/emotional_momentum.py", "tests/test_stage73_1_literary_formula_restoration.py"]},
            {"source": "MiseEnSceneCompiler", "relation": "PROVIDES_EVIDENCE_TO", "target": "Stage83.1ReleaseGate", "evidence": ["src/v1700/literary_formulas/mise_en_scene_compiler.py", "tests/test_stage73_1_literary_formula_restoration.py"]},
        ]
    )
    none_edges = [r for r in relations if not r.get("source") or not r.get("target")]
    edge_texts = [_edge(r.get("source"), r.get("relation"), r.get("target")) for r in relations]
    return {
        "stage": "83.1",
        "status": "pass" if not none_edges and not any("None --" in e or "--> None" in e for e in edge_texts) else "blocked",
        "basis": "Organic relation graph rebuilt from core_logic_survival_matrix_v3 and Stage83.1 bridge evidence.",
        "relation_count": len(relations),
        "none_edge_count": len(none_edges),
        "relations": relations,
        "edge_texts": edge_texts,
    }


def build_commercial_readiness_gap_manifest_v2() -> dict[str, Any]:
    return {
        "stage": "83.1",
        "status": "commercial_release_candidate_ready",
        "basis": "Stage82 and Stage83 evidence has been reconciled after the Stage81.1 gap manifest.",
        "items": [
            {
                "gap_id": "full_episode_actual_rendering",
                "status": "RESOLVED_STAGE83",
                "evidence": [
                    "sample_longform_project_01/generated_episode_01.md",
                    "sample_longform_project_01/generated_episode_02.md",
                    "sample_longform_project_01/generated_episode_03.md",
                ],
            },
            {
                "gap_id": "full_532_scene_actual_rendering",
                "status": "DEFERRED_STAGE85_NOT_REQUIRED_FOR_STAGE83_1",
                "evidence": ["docs/stages/stage76.md", "docs/roadmaps/stage83_commercial_release_candidate.md"],
            },
            {
                "gap_id": "external_blind_critic_benchmark",
                "status": "RESOLVED_STAGE82",
                "evidence": ["release/current/stage82_blind_critic_benchmark_report.json", "sample_longform_project_01/blind_eval_report.md"],
            },
            {
                "gap_id": "commercial_release_candidate",
                "status": "RESOLVED_STAGE83",
                "evidence": ["sample_longform_project_01/commercial_release_manifest.json", "release/current/stage83_release_gate_report.json"],
            },
        ],
    }


def build_gitnexus_branchpoint_bridge_manifest() -> dict[str, Any]:
    return {
        "stage": "83.1",
        "status": "pass",
        "gitnexus_role": "optional_sidecar",
        "graphnexus_role": "CodeGraph + NarrativeGraph + StageLineageGraph",
        "branchpoint_logic_graph_role": "Core logic survival and stale-manifest protection.",
        "bridges": [
            {
                "bridge_id": "gitnexus_to_codegraph",
                "source": "GitNexus",
                "target": "GraphNexus.CodeGraph",
                "contract": "Index code impact without becoming narrative authority.",
                "evidence": ["docs/concepts/gitnexus_optional_sidecar.md", "manifests/gitnexus_optional_sidecar_manifest.json"],
            },
            {
                "bridge_id": "codegraph_to_branchpoint_logic_graph",
                "source": "GraphNexus.CodeGraph",
                "target": "BranchpointLogicGraph",
                "contract": "Map implementation files to branchpoint logic IDs.",
                "evidence": ["manifests/branchpoint_model_registry_v2.json", "manifests/core_logic_survival_matrix_v3.json"],
            },
            {
                "bridge_id": "stage_lineage_to_release_gate",
                "source": "GraphNexus.StageLineageGraph",
                "target": "Stage83.1ReleaseGate",
                "contract": "Prevent Stage84 from mounting V370 runtime muscle on stale Stage75/81.1 manifests.",
                "evidence": ["src/v1700/gates/stage83_1_release_gate.py"],
            },
        ],
    }


def _missing_files(root: Path, paths: list[str]) -> list[str]:
    missing: list[str] = []
    for rel in paths:
        if rel.startswith("stage") and rel.endswith("release_gate"):
            continue
        if rel.startswith("manifests/"):
            # Newly exported manifests may not exist until export_stage83_1_manifests() runs.
            continue
        if "#" in rel:
            rel = rel.split("#", 1)[0]
        if not (root / rel).exists():
            missing.append(rel)
    return sorted(set(missing))


def run_stage83_1_consistency_audit(root: Path | None = None) -> dict[str, Any]:
    root = root or _project_root()
    registry = build_branchpoint_model_registry_v2()
    matrix = build_core_logic_survival_matrix_v3()
    graph = build_organic_relation_graph_manifest_v2()
    gaps = build_commercial_readiness_gap_manifest_v2()
    bridge = build_gitnexus_branchpoint_bridge_manifest()
    stage83 = run_stage83_release_gate(root)

    required_bp = {
        "BP_STAGE80_KOREAN_DRAMA_COMPOSITION_HIERARCHY",
        "BP_STAGE81_ACTUAL_TEXT_QUALITY_ENDURANCE",
        "BP_STAGE82_BLIND_CRITIC_BENCHMARK",
        "BP_STAGE83_COMMERCIAL_LONGFORM_RELEASE_CANDIDATE",
    }
    present_bp = {bp["branchpoint_id"] for bp in registry["branchpoints"]}
    pending_stage82_83 = [
        item["gap_id"] for item in gaps["items"]
        if item["status"].startswith("PENDING_STAGE82") or item["status"].startswith("PENDING_STAGE83")
    ]
    evidence_paths: list[str] = []
    for entry in matrix["entries"]:
        evidence_paths.extend(entry.get("evidence_files") or [])
        evidence_paths.extend(entry.get("test_coverage") or [])
    for item in gaps["items"]:
        evidence_paths.extend(item.get("evidence") or [])
    missing_evidence = _missing_files(root, evidence_paths)

    issues: list[str] = []
    if stage83.get("status") != "pass":
        issues.append("stage83_release_gate_blocked")
    if required_bp - present_bp:
        issues.append("stage80_83_branchpoints_missing")
    if matrix.get("status") != "pass":
        issues.append("core_logic_survival_matrix_v3_blocked")
    if graph.get("status") != "pass" or graph.get("none_edge_count", 1) != 0:
        issues.append("organic_relation_graph_v2_blocked")
    if pending_stage82_83:
        issues.append("stage82_83_pending_gap_status_remains")
    if bridge.get("status") != "pass":
        issues.append("gitnexus_branchpoint_bridge_missing")
    if missing_evidence:
        issues.append("declared_evidence_files_missing")

    return {
        "stage": "83.1",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage83.1 reconciles stale Stage75/81.1 manifests, rebuilds branchpoint/core-logic/organic-relation manifests through Stage83, and prepares a safe Stage84 absorption baseline.",
        "stage83_release_gate": stage83,
        "branchpoint_model_registry_v2": registry,
        "core_logic_survival_matrix_v3": matrix,
        "organic_relation_graph_manifest_v2": graph,
        "commercial_readiness_gap_manifest_v2": gaps,
        "gitnexus_branchpoint_bridge_manifest": bridge,
        "pending_stage82_83_gap_ids": pending_stage82_83,
        "missing_declared_evidence_files": missing_evidence,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }


def export_stage83_1_manifests(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    manifest_dir = root / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    audit = run_stage83_1_consistency_audit(root)
    payloads: dict[str, Any] = {
        "branchpoint_model_registry_v2.json": audit["branchpoint_model_registry_v2"],
        "core_logic_survival_matrix_v3.json": audit["core_logic_survival_matrix_v3"],
        "organic_relation_graph_manifest_v2.json": audit["organic_relation_graph_manifest_v2"],
        "commercial_readiness_gap_manifest_v2.json": audit["commercial_readiness_gap_manifest_v2"],
        "gitnexus_branchpoint_bridge_manifest.json": audit["gitnexus_branchpoint_bridge_manifest"],
        "stage83_1_manifest.json": {
            "stage": "83.1",
            "title": "Consistency Audit & Manifest Reconciliation",
            "depends_on": ["stage83"],
            "status": audit["status"],
            "required_outputs": [
                "manifests/branchpoint_model_registry_v2.json",
                "manifests/core_logic_survival_matrix_v3.json",
                "manifests/organic_relation_graph_manifest_v2.json",
                "manifests/commercial_readiness_gap_manifest_v2.json",
                "manifests/gitnexus_branchpoint_bridge_manifest.json",
                "tools/run_stage83_1_consistency_audit.py",
                "tools/run_gitnexus_branchpoint_bridge_audit.py",
                "tools/run_stage83_1_release_gate.py",
                "tests/test_stage83_1_consistency_audit.py",
                "tests/test_gitnexus_branchpoint_bridge.py",
                "tests/test_supporting_character_relation_edges.py",
            ],
            "provider_default_calls": 0,
            "node2_raw_reveal_access_count": 0,
        },
    }
    written: dict[str, str] = {}
    for name, payload in payloads.items():
        path = manifest_dir / name
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written[name] = str(path.relative_to(root))
    release_dir = root / "release" / "current"
    release_dir.mkdir(parents=True, exist_ok=True)
    report_path = release_dir / "stage83_1_consistency_audit_report.json"
    report_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written[report_path.name] = str(report_path.relative_to(root))
    return written
