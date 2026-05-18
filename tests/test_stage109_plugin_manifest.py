from pathlib import Path
from v1700.plugin_marketplace.plugin_catalog import builtin_plugin_manifests
from v1700.plugin_marketplace.plugin_validator import validate_plugin_manifest
from v1700.plugin_marketplace.marketplace_index import build_marketplace_index


def test_stage109_builtin_plugin_manifests_validate():
    plugins = builtin_plugin_manifests()
    assert len(plugins) >= 4
    for plugin in plugins:
        result = validate_plugin_manifest(plugin)
        assert result.status == "pass", result
        assert plugin.enabled_by_default is False
        assert plugin.requires_raw_manuscript is False


def test_stage109_marketplace_index(tmp_path: Path):
    result = build_marketplace_index(tmp_path)
    assert result["status"] == "pass"
    assert result["enabled_by_default_count"] == 0
    assert result["raw_manuscript_access_count"] == 0
    assert (tmp_path / "release/current/stage109_plugin_pack/plugin_marketplace_index.json").exists()
