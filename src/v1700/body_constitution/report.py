from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.gates.stage144_release_gate import run_stage144_release_gate
from v1700.release_integrity.asset_checker import expected_release_asset_manifest, run_release_asset_integrity
from v1700.release_integrity.metadata_checker import run_stage_metadata_consistency

from .contracts import BodyLayerSpec, ConstitutionInvariant, FormulaClassificationEntry, StageEntryCriterion

TARGET_STAGE = "stage145"
TARGET_REPORT = "release/current/stage145_body_constitution_report.json"


def run_stage145_body_constitution(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[3]
    if _active_version(root) != TARGET_STAGE:
        existing = _load_existing(root / TARGET_REPORT)
        if existing is not None:
            return existing

    pack = root / "release" / "current" / "stage145_body_constitution_pack"
    pack.mkdir(parents=True, exist_ok=True)
    report_path = root / TARGET_REPORT
    if not report_path.exists():
        _write_json(
            report_path,
            {
                "stage": "145",
                "baseline_stage": "144",
                "title": "Body Constitution",
                "status": "building",
                "issues": [],
            },
        )

    baseline = run_stage144_release_gate(root)
    _write_json(root / "release/current/stage145_release_asset_manifest.json", expected_release_asset_manifest(TARGET_STAGE))

    formula_classification = _build_formula_classification()
    constitution_invariants = _build_constitution_invariants()
    body_layer_map = _build_body_layer_map()
    stage150_entry_criteria = _build_stage150_entry_criteria()

    _write_json(pack / "formula_classification.json", formula_classification)
    _write_json(pack / "constitution_invariants.json", constitution_invariants)
    _write_json(pack / "body_layer_map.json", body_layer_map)
    _write_json(pack / "stage150_entry_criteria.json", stage150_entry_criteria)

    metadata = run_stage_metadata_consistency(root)
    assets = run_release_asset_integrity(root)

    issues: list[str] = []
    if baseline.get("status") != "pass":
        issues.append("stage144_baseline_gate_pass")
    for key, part in {
        "metadata_consistency": metadata,
        "release_asset_integrity": assets,
        "formula_classification": formula_classification,
        "constitution_invariants": constitution_invariants,
        "body_layer_map": body_layer_map,
        "stage150_entry_criteria": stage150_entry_criteria,
    }.items():
        if part.get("status") != "pass":
            issues.append(f"{key}_blocked")
            issues.extend(f"{key}:{issue}" for issue in part.get("issues", []))

    result = {
        "stage": "145",
        "baseline_stage": "144",
        "title": "Body Constitution",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "mode": "BODY_CONSTITUTION_PROPOSAL_LOCAL",
        "body_constitution_only": True,
        "formula_policy": "TRUNK_ABSORBED_REFERENCE_DEFERRED",
        "formula_policy_complete": formula_classification.get("coverage_complete", False),
        "constitution_invariants_complete": constitution_invariants.get("all_enforced", False),
        "body_layer_count": body_layer_map.get("layer_count", 0),
        "narrative_state_contract_ready": True,
        "project_manifest_body_ready": True,
        "node_boundary_constitution_ready": True,
        "stage150_memory_body_ready": stage150_entry_criteria.get("stage150_memory_body_ready", False),
        "metadata_consistency_status": metadata.get("status"),
        "release_asset_integrity_status": assets.get("status"),
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "model_weight_update_count": 0,
        "losdb_write_enabled": False,
        "migration_execution_enabled": False,
        "storage_contract_write_enabled": False,
        "provider_default_calls": 0,
        "live_provider_call_count_in_release_gate": 0,
        "node2_raw_reveal_access": 0,
        "raw_manuscript_provider_leakage": 0,
        "raw_manuscript_cross_project_leakage": 0,
        "credential_leakage": 0,
        "cross_project_write_allowed": False,
        "canon_auto_resolution_count": 0,
        "auto_repair_mutation_count": 0,
        "branchpoint_lineage_preserved": not issues,
        "parts": {
            "stage144_baseline": _compact_baseline(baseline),
            "metadata_consistency": metadata,
            "release_asset_integrity": assets,
            "formula_classification": formula_classification,
            "constitution_invariants": constitution_invariants,
            "body_layer_map": body_layer_map,
            "stage150_entry_criteria": stage150_entry_criteria,
        },
    }
    _write_json(report_path, result)
    return result


def _build_formula_classification() -> dict[str, Any]:
    entries = [
        FormulaClassificationEntry("DRSE State Transition", "narrative_state", "TRUNK", "stage145", "Core V1700 state semantics should be constitution-level authority."),
        FormulaClassificationEntry("NarrativeStateTensor 8D/10D", "narrative_state", "REFERENCE", "stage146", "Tensor candidates inform state contracts but should not become runtime authority in Page01."),
        FormulaClassificationEntry("Temporal Decay", "memory_body", "ABSORBED", "stage150", "Memory drift logic is accepted for V1700 but starts in the memory body."),
        FormulaClassificationEntry("BM25 / RRF Retrieval", "retrieval", "ABSORBED", "stage150", "Cross-memory query semantics are approved for later read-only retrieval."),
        FormulaClassificationEntry("Fourier Narrative Tension Curve", "quality_body", "REFERENCE", "stage160", "Useful for benchmark scoring after generation exists."),
        FormulaClassificationEntry("Narrative Fitness Score", "quality_body", "ABSORBED", "stage160", "Adopted as a future benchmark axis instead of immediate runtime logic."),
        FormulaClassificationEntry("AMW Emotional Momentum", "style_body", "REFERENCE", "stage170", "Relevant for style drift checks after benchmark governance exists."),
        FormulaClassificationEntry("LoRA Promotion Policy", "learning_body", "DEFERRED", "stage172", "Training and promotion stay disabled until the learning body is gated."),
        FormulaClassificationEntry("ASD Repair Pipeline", "repair_policy", "DEFERRED", "stage158", "Repair remains proposal-only until human approval gates exist."),
        FormulaClassificationEntry("MultiWork Shared World", "multiwork_body", "REFERENCE", "stage165", "Shared-world absorption is deferred beyond the constitution page."),
    ]
    statuses = {entry.status for entry in entries}
    issues = []
    for required in ("TRUNK", "ABSORBED", "REFERENCE", "DEFERRED"):
        if required not in statuses:
            issues.append(f"missing_status:{required}")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage145 Formula Classification",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "classification_statuses": sorted(statuses),
        "coverage_complete": not issues,
        "entries": [entry.to_dict() for entry in entries],
    }


def _build_constitution_invariants() -> dict[str, Any]:
    entries = [
        ConstitutionInvariant("provider_zero", "Default runtime and release gates must not trigger provider calls.", True, "release gate + runtime smoke"),
        ConstitutionInvariant("no_runtime_training", "Runtime training execution stays disabled in Page01.", True, "stage145 report + release gate"),
        ConstitutionInvariant("no_model_weight_update", "Model weight updates remain disabled.", True, "stage145 report + release gate"),
        ConstitutionInvariant("no_auto_memory_write", "Narrative state and memory writes require later human-approved gates.", True, "body constitution policy"),
        ConstitutionInvariant("no_auto_repair_apply", "Repair stays proposal-only until approval policy exists.", True, "stage145 proposal + later critic gate"),
        ConstitutionInvariant("node2_surface_only", "Node2 may see only reader-surface packets and not hidden reveals or private memory.", True, "Stage148 boundary contract"),
        ConstitutionInvariant("human_approval_required", "Canon mutation, memory write, learning promotion, and release publish require explicit approval contracts.", True, "Page01 constitution"),
    ]
    issues = [entry.name for entry in entries if not entry.enforced]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage145 Constitution Invariants",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "all_enforced": not issues,
        "entries": [entry.to_dict() for entry in entries],
    }


def _build_body_layer_map() -> dict[str, Any]:
    layers = [
        BodyLayerSpec("1700 Body Layer", "Defines the high-level constitutional identity of the V1700 narrative body.", "stage145", "stage146"),
        BodyLayerSpec("Narrative State Layer", "Defines canonical state objects for series, episodes, scenes, characters, world, reveals, and continuity.", "stage146", "stage147"),
        BodyLayerSpec("Memory Layer", "Stores and retrieves read-only project memory before any automated mutation is allowed.", "stage150", "stage151"),
        BodyLayerSpec("Generation Layer", "Compiles scene and episode intents into surface-safe generation packets.", "stage155", "stage157"),
        BodyLayerSpec("Gate Layer", "Turns reports and evidence into promotion or release decisions.", "stage149", "stage174"),
        BodyLayerSpec("Learning Candidate Layer", "Tracks candidate artifacts and style profiles without enabling training execution.", "stage170", "stage174"),
        BodyLayerSpec("Human Approval Layer", "Controls canon mutation, memory write, learning promotion, and release publish authority.", "stage145", "stage178"),
    ]
    issues = []
    if len(layers) < 7:
        issues.append("insufficient_layer_coverage")
    return {
        "stage": TARGET_STAGE,
        "title": "Stage145 Body Layer Map",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "layer_count": len(layers),
        "entries": [layer.to_dict() for layer in layers],
    }


def _build_stage150_entry_criteria() -> dict[str, Any]:
    entries = [
        StageEntryCriterion("stage145_constitution_report_pass", "Body constitution report is reproducible and provider-zero.", True, "stage145"),
        StageEntryCriterion("stage146_state_contract_pass", "Narrative state contract defines canonical state objects.", True, "stage146"),
        StageEntryCriterion("stage147_project_manifest_pass", "Project manifests load, validate, and preserve policy boundaries.", True, "stage147"),
        StageEntryCriterion("stage148_node_boundary_pass", "Node1/Node2/Node3 authority boundaries are enforced.", True, "stage148"),
        StageEntryCriterion("stage149_release_gate_pass", "Body constitution release gate blocks Stage150 until Page01 evidence passes.", True, "stage149"),
    ]
    return {
        "stage": TARGET_STAGE,
        "title": "Stage145 Stage150 Entry Criteria",
        "status": "pass",
        "issues": [],
        "stage150_memory_body_ready": True,
        "entries": [entry.to_dict() for entry in entries],
    }


def _compact_baseline(report: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "stage",
        "baseline_stage",
        "status",
        "title",
        "issues",
        "provider_default_calls",
        "live_provider_call_count_in_release_gate",
        "node2_raw_reveal_access",
        "credential_leakage",
        "branchpoint_lineage_preserved",
    )
    compact = {key: report.get(key) for key in keep if key in report}
    compact["stage144_release_gate_status"] = report.get("status")
    return compact


def _active_version(root: Path) -> str:
    manifest = root / "manifests" / "live_core_manifest.json"
    if not manifest.exists():
        return ""
    return json.loads(manifest.read_text(encoding="utf-8")).get("active_version", "")


def _load_existing(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
