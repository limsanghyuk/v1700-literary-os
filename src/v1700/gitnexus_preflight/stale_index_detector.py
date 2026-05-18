from __future__ import annotations

from pathlib import Path


def detect_stale_index(root: Path, index_status: dict | None = None) -> dict:
    index_status = index_status or {}
    # A missing optional GitNexus sidecar is not a stale index. It means the
    # required Python fallback must be used. A stale index only blocks if a
    # sidecar claims authority but cannot be tied to current manifests.
    sidecar_available = bool(index_status.get("gitnexus_sidecar_available"))
    active_manifest = root / "manifests/live_core_manifest.json"
    stale = sidecar_available and not active_manifest.exists()
    return {
        "status": "blocked" if stale else "pass",
        "stale_index_detected": stale,
        "sidecar_available": sidecar_available,
        "fallback_allowed": not sidecar_available,
        "reason": "optional_sidecar_absent_python_fallback_required" if not sidecar_available else "sidecar_bound_to_live_manifest",
    }

