from __future__ import annotations

from pathlib import Path

from v1700.traceability.index_quality import build_gitnexus_index_quality_report


def run_gitnexus_index_quality_gate(root: Path | None = None) -> dict:
    report = build_gitnexus_index_quality_report(root)
    return report

