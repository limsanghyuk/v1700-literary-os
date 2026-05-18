from __future__ import annotations

from pathlib import Path

from v1700.cross_lineage.absorption_decision import build_absorption_decisions
from v1700.cross_lineage.lineage_trace import build_cross_lineage_trace_report
from v1700.stage101.report import stage101_pack, write_json, write_summary


def run_stage101_absorption_matrix(root: Path | None = None, source_probe: dict | None = None) -> dict:
    root = root or Path.cwd()
    matrix = build_absorption_decisions(source_probe)
    trace = build_cross_lineage_trace_report(matrix)
    payload = {
        "stage": "101.0",
        "baseline_stage": "100",
        "title": "V430 Absorption Candidate Matrix",
        **matrix,
        "cross_lineage_trace": trace,
    }
    if trace.get("status") != "pass":
        payload["status"] = "blocked"
        payload.setdefault("issues", []).append("cross_lineage_trace_blocked")
    else:
        payload["issues"] = []
    write_json(root / "release" / "current" / "stage101_absorption_candidate_matrix.json", payload)
    pack = stage101_pack(root, "stage101_cross_lineage_pack")
    write_json(pack / "absorption_candidate_matrix.json", payload)
    write_json(pack / "cross_lineage_trace_report.json", trace)
    write_summary(
        pack / "absorption_matrix_summary.md",
        "Stage101 Absorption Matrix",
        [
            f"absorption mode: {payload['absorption_mode']}",
            f"candidates: {len(payload['candidates'])}",
            f"trace status: {trace['status']}",
        ],
    )
    return payload

