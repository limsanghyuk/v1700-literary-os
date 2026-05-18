from __future__ import annotations
import json
from pathlib import Path

def write_stage108_summary(root: Path, report: dict) -> Path:
    out = root / "release/current/stage108_editorial_board_pack/stage108_summary.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "# Stage108 External Review & Editorial Board Mode\n\n"
        f"- status: {report.get('status')}\n"
        f"- reviewers: {report.get('stage108_1_editorial_board', {}).get('reviewer_count')}\n"
        f"- scorecards: {report.get('stage108_1_editorial_board', {}).get('scorecard_count')}\n"
        "- release path: provider-zero / fixture-only\n",
        encoding="utf-8",
    )
    return out
