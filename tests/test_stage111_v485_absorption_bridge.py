from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from v1700.stage111.orchestrator import run_stage111
from v1700.gates.stage111_release_gate import run_stage111_release_gate
from v1700.v485_bridge.v485_manifest_probe import probe_v485_version_profile
from v1700.stage111.absorption_candidate_matrix import build_absorption_candidate_matrix

ROOT = Path(__file__).resolve().parents[1]

def test_stage111_orchestrator_passes():
    result = run_stage111(ROOT)
    assert result['status'] == 'pass'
    assert result['release_gate_affected_by_v485'] is False

def test_stage111_version_drift_contained():
    report = probe_v485_version_profile()
    assert report['drift_detected'] is True
    assert report['direct_metadata_import_allowed'] is False
    assert report['status'] == 'pass'

def test_stage111_absorption_matrix_blocks_direct_gate_and_metadata():
    matrix = build_absorption_candidate_matrix()
    statuses = {c['candidate_id']: c['absorption_status'] for c in matrix['candidates']}
    assert statuses['v485_release_gate'] == 'REJECT'
    assert statuses['v485_metadata'] == 'REJECT'
    assert statuses['v485_raw_live_call_path'] == 'BLOCK'
    assert statuses['drama_episode_generator'] == 'WRAP_ONLY'

def test_stage111_release_gate_passes():
    result = run_stage111_release_gate(ROOT)
    assert result['status'] == 'pass'
    assert result['live_provider_call_count_in_release_gate'] == 0

def test_stage111_privacy_invariants():
    result = run_stage111(ROOT)
    assert result['raw_manuscript_provider_leakage'] == 0
    assert result['credential_leakage'] == 0
    assert result['raw_response_stored'] is False

def test_stage111_docs_manifest_exist():
    assert (ROOT / 'docs/stages/stage111.md').exists()
    assert (ROOT / 'manifests/stage111_manifest.json').exists()
    assert 'Stage111' in (ROOT / 'README.md').read_text(encoding='utf-8')
