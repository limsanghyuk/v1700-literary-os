from __future__ import annotations


def build_cross_lineage_trace_report(absorption_matrix: dict) -> dict:
    candidates = absorption_matrix.get("candidates", [])
    traced = [
        {
            "candidate_id": item["candidate_id"],
            "proposed_action": item["proposed_action"],
            "branchpoints": item["required_branchpoints"],
            "tests": item["required_tests"],
            "traced": bool(item["required_branchpoints"] and item["required_tests"]),
        }
        for item in candidates
    ]
    issues = [item["candidate_id"] for item in traced if not item["traced"]]
    return {
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "trace_entries": traced,
        "v430_untraced_merge": absorption_matrix.get("v430_untraced_merge", False),
    }

