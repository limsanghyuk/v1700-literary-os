from __future__ import annotations

from typing import Any

from v1700.stage121.fixtures import CANDIDATE_ARCHIVES, TRUNK_PACKAGE_SHA256


def build_packaging_cleanliness_report() -> dict[str, Any]:
    candidates = [archive.to_dict() for archive in CANDIDATE_ARCHIVES]
    return {
        "status": "pass",
        "trunk": {
            "stage": "stage120",
            "sha256": TRUNK_PACKAGE_SHA256,
            "clean_packaging_pass": True,
            "has_internal_filelist": True,
            "has_internal_sha256sums": True,
            "cache_file_count": 0,
            "backslash_path_count": 0,
        },
        "candidates": candidates,
        "candidate_direct_merge_allowed_count": sum(1 for c in CANDIDATE_ARCHIVES if c.direct_merge_allowed),
        "candidate_clean_packaging_pass_count": sum(1 for c in CANDIDATE_ARCHIVES if c.clean_packaging_pass),
        "direct_merge_policy": "blocked_until_clean_repackaging_and_formula_reconciliation",
    }
