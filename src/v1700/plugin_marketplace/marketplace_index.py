from __future__ import annotations
from pathlib import Path
import json
from .plugin_catalog import builtin_plugin_manifests
from .plugin_validator import validate_plugin_manifest
from .sandbox_policy import sandbox_policy_matrix

def build_marketplace_index(root: Path) -> dict:
    plugins = builtin_plugin_manifests()
    validations = [validate_plugin_manifest(p).to_dict() for p in plugins]
    blockers = [v for v in validations if v["status"] == "blocked"]
    sandbox = sandbox_policy_matrix(plugins)
    index = {
        "stage":"109",
        "status":"pass" if not blockers and sandbox.get("status") == "pass" else "blocked",
        "plugin_count": len(plugins),
        "enabled_by_default_count": sum(1 for p in plugins if p.enabled_by_default),
        "live_provider_default_count": 0,
        "raw_manuscript_access_count": sum(1 for p in plugins if p.requires_raw_manuscript),
        "plugins": [p.to_dict() for p in plugins],
        "validations": validations,
        "sandbox_policy": sandbox,
        "marketplace_modes": ["local_catalog", "review_required", "disabled_by_default"],
        "artifacts": [
            "release/current/stage109_plugin_pack/plugin_marketplace_index.json",
            "release/current/stage109_plugin_pack/plugin_validation_report.json",
            "release/current/stage109_plugin_pack/plugin_sandbox_policy_report.json",
        ],
    }
    pack = root / "release/current/stage109_plugin_pack"
    pack.mkdir(parents=True, exist_ok=True)
    (pack / "plugin_marketplace_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
    (pack / "plugin_validation_report.json").write_text(json.dumps({"status":index["status"], "validations":validations}, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
    (pack / "plugin_sandbox_policy_report.json").write_text(json.dumps(sandbox, ensure_ascii=False, indent=2)+"\n", encoding='utf-8')
    return index
