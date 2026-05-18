from __future__ import annotations

from .apply_guard import run_revision_apply_guard


def build_revision_apply_plan() -> dict:
    guard = run_revision_apply_guard()
    return {
        "status": guard.get("status"),
        "apply_mode": "approved_feature_patch_only",
        "mutates_raw_manuscript": False,
        "guard": guard,
    }
