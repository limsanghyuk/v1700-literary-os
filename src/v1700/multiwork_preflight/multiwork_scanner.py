from __future__ import annotations

from pathlib import Path
from typing import Any

MULTIWORK_TERMS = (
    "V571", "MultiWork", "SharedCharacterDB", "SharedWorldDB",
    "ProjectIsolationManager", "MultiWorkCIM", "AuthorLicenseAPI",
    "MultiWorkOrchestrator", "CrossWork", "shared character", "shared world",
)

DIRECT_MERGE_PATHS = (
    "src/v1700/multiwork",
    "src/v1700/shared_character_db",
    "src/v1700/shared_world_db",
    "src/v1700/author_license",
    "src/v1700/multiwork_cim",
)


def scan_multiwork_sources(root: Path) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    search_roots = [root / "docs", root / "manifests", root / "archive", root / "release/current"]
    for base in search_roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if len(candidates) >= 80:
                break
            if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".json"}:
                continue
            try:
                if path.stat().st_size > 500_000:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            low = text.lower()
            hits = [term for term in MULTIWORK_TERMS if term.lower() in low]
            if hits:
                candidates.append({
                    "path": path.relative_to(root).as_posix(),
                    "terms": sorted(set(hits)),
                })
    direct_merge_paths_present = [rel for rel in DIRECT_MERGE_PATHS if (root / rel).exists()]
    return {
        "status": "pass" if not direct_merge_paths_present else "blocked",
        "multiwork_candidate_references": candidates[:80],
        "candidate_reference_count": len(candidates),
        "direct_v571_merge_detected": bool(direct_merge_paths_present),
        "direct_merge_paths_present": direct_merge_paths_present,
        "scan_terms": list(MULTIWORK_TERMS),
    }
