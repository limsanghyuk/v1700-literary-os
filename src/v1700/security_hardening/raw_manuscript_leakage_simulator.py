from __future__ import annotations

import json
from pathlib import Path


def simulate_raw_manuscript_leakage(root: Path) -> dict:
    manifest = root / "release" / "current" / "stage98_studio_pack" / "publishing_package_manifest.json"
    payload = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else {}
    includes_full_text = bool(payload.get("includes_full_text", False))
    provider_export = bool(payload.get("provider_export", False))
    leakage = 1 if includes_full_text or provider_export else 0
    return {
        "status": "pass" if leakage == 0 else "blocked",
        "raw_manuscript_provider_leakage": leakage,
        "full_text_exported_by_default": includes_full_text,
        "provider_export": provider_export,
    }
