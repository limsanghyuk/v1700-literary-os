from __future__ import annotations


def build_stage96_provider_ensemble_manifest() -> dict:
    return {
        "stage": "96C",
        "title": "Provider Ensemble Arbitration",
        "status": "pass_pending_export",
        "release_gate_mode": "dry_run_fixture_candidates",
        "live_provider_call_count": 0,
        "decision_types": ["SELECT", "REJECT", "MERGE", "REQUEST_REFINEMENT", "BLOCK"],
    }
