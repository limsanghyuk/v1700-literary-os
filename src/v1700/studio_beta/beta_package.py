from __future__ import annotations

from pathlib import Path

from .import_export import build_studio_beta_export


def build_beta_package(root: Path) -> dict:
    export = build_studio_beta_export(root)
    return {
        "status": export.get("status"),
        "package_type": "feature_only_studio_beta_package",
        "includes_full_text": export.get("includes_full_text"),
        "includes_release_evidence": export.get("includes_release_evidence"),
        "export_manifest": export,
    }
