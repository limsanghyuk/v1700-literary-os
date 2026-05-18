from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from v1700.stage108.orchestrator import run_stage108
if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    report = run_stage108(root)
    artifact = {
        'stage':'108',
        'status':report.get('status'),
        'artifacts': report.get('stage108_1_editorial_board', {}).get('artifacts', []),
        'canonical_package':'V1700_stage108_external_review_editorial_board_FIXED.zip',
    }
    out = root/'release/current/stage108_artifact_export_report.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(artifact, ensure_ascii=True, indent=2))
    raise SystemExit(0 if artifact['status']=='pass' else 1)
