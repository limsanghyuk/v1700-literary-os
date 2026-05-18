from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from v1700.stage111.orchestrator import run_stage111
ROOT = Path(__file__).resolve().parents[1]
if __name__ == '__main__':
    result = run_stage111(ROOT)
    out = ROOT / 'release/current/stage111_artifact_export_report.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {'stage': '111', 'status': result.get('status'), 'included_reports': [
        'stage111_v485_absorption_bridge_report.json', 'stage111_v485_version_drift_report.json',
        'stage111_adapter_bridge_probe_report.json', 'stage111_scene_pipeline_bridge_report.json',
        'stage111_drama_episode_bridge_report.json', 'stage111_v485_absorption_candidate_matrix.json',
        'stage111_release_gate_report.json'], 'raw_v485_source_included': False}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    raise SystemExit(0 if payload['status'] == 'pass' else 1)
