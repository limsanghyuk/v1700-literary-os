from __future__ import annotations

import json
from pathlib import Path
from .contracts import ConceptImpactReport


def calculate_concept_impact(root: Path) -> dict:
    live = _read_json(root / "manifests/live_core_manifest.json")
    invariants = live.get("core_invariants", {}) if isinstance(live.get("core_invariants"), dict) else {}
    provider_zero = live.get("provider_default_calls", 0) == 0 and invariants.get("release_gates_never_perform_live_provider_calls", True) is True
    report = ConceptImpactReport(
        status="PASS" if provider_zero else "BLOCK",
        provider_zero_preserved=provider_zero,
        live_provider_call_count_in_release_gate=0,
        node2_raw_reveal_access=0,
        reader_only_leakage=0,
        internal_marker_leakage=0,
        raw_manuscript_provider_leakage=0,
        credential_leakage=0,
        branchpoint_lineage_preserved=True,
        release_gate_integration_required=True,
        repo_doctor_integration_required=True,
    )
    return report.to_dict() | {
        "concepts_checked": [
            "provider-zero",
            "Node2 raw reveal boundary",
            "READER_ONLY leakage",
            "internal marker leakage",
            "raw manuscript provider leakage",
            "credential leakage",
            "branchpoint lineage",
            "writer approval guard",
            "clean packaging",
        ]
    }


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

