from __future__ import annotations

import re
from pathlib import Path

MARKER_PATTERNS = (
    re.compile(r"READER_ONLY"),
    re.compile(r"INTERNAL_MARKER"),
    re.compile(r"RAW_REVEAL"),
)


def scan_internal_marker_leakage(root: Path) -> dict:
    hits: list[str] = []
    release_root = root / "release" / "current" / "stage98_studio_pack"
    if release_root.exists():
        for path in release_root.rglob("*"):
            if path.is_file() and path.suffix not in {".zip", ".pyc"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                if any(pattern.search(text) for pattern in MARKER_PATTERNS):
                    hits.append(path.relative_to(root).as_posix())
    return {
        "status": "pass" if not hits else "blocked",
        "reader_only_leakage": sum(1 for hit in hits if "READER_ONLY" in hit),
        "internal_marker_leakage": len(hits),
        "hits": hits,
    }
