from __future__ import annotations

from pathlib import Path

from v1700.cross_lineage.v430_candidate_probe import probe_v430_sources
from v1700.stage101.report import stage101_pack, write_json, write_summary


def run_stage101_v430_source_probe(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    report = probe_v430_sources(root)
    write_json(root / "release" / "current" / "stage101_v430_source_probe_report.json", report)
    pack = stage101_pack(root, "stage101_cross_lineage_pack")
    write_json(pack / "v430_source_probe_report.json", report)
    write_summary(
        pack / "v430_source_probe_summary.md",
        "Stage101 V430 Source Probe",
        [
            f"source status: {report['source_status']}",
            f"absorption mode: {report['absorption_mode']}",
            f"untraced merge: {report['v430_untraced_merge']}",
        ],
    )
    return report

