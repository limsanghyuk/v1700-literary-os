from __future__ import annotations

from pathlib import Path

REQUIRED_INTEGRATION_PATHS = [
    "src/v1700/gates/stage112_release_gate.py",
    "tools/run_stage112_release_gate.py",
    "tools/run_stage112_gitnexus_nie_preflight.py",
    "manifests/stage112_manifest.json",
    "docs/stages/stage112.md",
]


def check_release_gate_integration(root: Path) -> dict:
    paths = {rel: (root / rel).exists() for rel in REQUIRED_INTEGRATION_PATHS}
    missing = [rel for rel, ok in paths.items() if not ok]
    live_text = (root / "manifests/live_core_manifest.json").read_text(encoding="utf-8", errors="ignore") if (root / "manifests/live_core_manifest.json").exists() else ""
    gate_registered = "stage112_release_gate" in live_text and "stage112_gitnexus_nie_preflight" in live_text
    if not gate_registered:
        missing.append("live_core_manifest.stage112_gates")
    return {"status": "pass" if not missing else "blocked", "paths": paths, "gate_registered": gate_registered, "missing": missing}

