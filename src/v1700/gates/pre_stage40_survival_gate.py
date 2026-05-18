from __future__ import annotations

import json
from pathlib import Path

from v1700.graph_nexus.tools.foundation_lineage import find_knowledge_base_root, required_concept_ids


def run_pre_stage40_survival_gate(root: Path) -> dict:
    manifest_path = root / "manifests" / "pre_stage40_lineage_manifest.json"
    raw_index_path = root / "manifests" / "pre_stage40_raw_evidence_index.json"
    issues: list[str] = []

    if not raw_index_path.exists():
        issues.append("pre_stage40_raw_evidence_index_missing")
    if not manifest_path.exists():
        return {
            "stage": "72.3",
            "status": "blocked",
            "issues": [*issues, "pre_stage40_lineage_manifest_missing"],
        }

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    concepts = manifest.get("concepts", [])
    concept_by_id = {concept.get("concept_id"): concept for concept in concepts}
    kb = find_knowledge_base_root(root)

    missing_required = [concept_id for concept_id in required_concept_ids() if concept_id not in concept_by_id]
    if missing_required:
        issues.append("required_concepts_missing")

    high_priority_unknown = []
    missing_source_evidence = []
    missing_current_anchor = []
    missing_evidence_files = []

    for concept in concepts:
        concept_id = concept.get("concept_id", "")
        evidence = concept.get("source_evidence", [])
        if not evidence:
            missing_source_evidence.append(concept_id)
        for rel_path in evidence:
            if not (kb / rel_path).exists():
                missing_evidence_files.append(f"{concept_id}:{rel_path}")
        if concept.get("promotion_priority") == "HIGH" and concept.get("survival_status") == "UNKNOWN_NEEDS_REVIEW":
            high_priority_unknown.append(concept_id)
        if concept.get("survival_status") in {"LIVE_RUNTIME", "LIVE_GATE_ONLY", "PARTIAL"}:
            anchors = (
                concept.get("current_runtime_anchor", [])
                + concept.get("current_test_anchor", [])
                + concept.get("current_gate_anchor", [])
                + concept.get("current_doc_anchor", [])
            )
            if not anchors:
                missing_current_anchor.append(concept_id)
            for anchor in anchors:
                if not (root / anchor).exists():
                    missing_current_anchor.append(f"{concept_id}:{anchor}")

    if missing_source_evidence:
        issues.append("concept_source_evidence_missing")
    if missing_evidence_files:
        issues.append("concept_source_evidence_files_missing")
    if missing_current_anchor:
        issues.append("live_or_partial_current_anchor_missing")
    if high_priority_unknown:
        issues.append("high_priority_unknown_concepts")

    return {
        "stage": "72.3",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "concept_count": len(concepts),
        "required_concept_count": len(required_concept_ids()),
        "missing_required": missing_required,
        "missing_source_evidence": missing_source_evidence,
        "missing_evidence_files": missing_evidence_files,
        "missing_current_anchor": missing_current_anchor,
        "high_priority_unknown": high_priority_unknown,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
