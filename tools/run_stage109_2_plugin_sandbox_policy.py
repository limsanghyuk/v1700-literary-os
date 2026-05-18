from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from v1700.plugin_marketplace.plugin_catalog import builtin_plugin_manifests
from v1700.plugin_marketplace.sandbox_policy import sandbox_policy_matrix
if __name__ == '__main__':
    result = sandbox_policy_matrix(builtin_plugin_manifests())
    out = Path(__file__).resolve().parents[1] / 'release/current/stage109_plugin_pack/plugin_sandbox_policy_report.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=True, indent=2))
    raise SystemExit(0 if result.get('status') == 'pass' else 1)
