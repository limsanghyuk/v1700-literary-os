from __future__ import annotations

import json
from pathlib import Path


def check_index_status(root: Path) -> dict:
    live = _read_json(root / "manifests/live_core_manifest.json")
    graph_manifest = root / "manifests/graph_nexus_manifest.json"
    sidecar_dirs = [root / ".gitnexus", root / "release/current/gitnexus_index"]
    sidecar_available = any(p.exists() for p in sidecar_dirs)
    active = live.get("active_version")
    index_fresh = bool(active) and graph_manifest.exists()
    return {
        "status": "pass" if index_fresh else "warn",
        "repo_id": "v1700-literary-os-stage112",
        "active_version": active,
        "graph_manifest_exists": graph_manifest.exists(),
        "gitnexus_sidecar_available": sidecar_available,
        "python_fallback_required": not sidecar_available,
        "index_fresh": index_fresh,
    }


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

