from __future__ import annotations

from pathlib import Path

from .report import write_summary


def write_beta_handoff(root: Path) -> dict:
    path = root / "release" / "current" / "stage104_developer_handoff_report.md"
    write_summary(path, "Stage104 Developer Handoff", [
        "Stage104 opens the Commercial Writer Studio Beta layer.",
        "Studio Beta is local-first and feature-only by default.",
        "Prose and scenario boards are kept distinct to avoid metric conflation.",
        "Writer decision guard blocks unauthorized revision application.",
        "Release mode keeps provider live calls at zero.",
    ])
    return {"status": "pass", "path": path.relative_to(root).as_posix()}
