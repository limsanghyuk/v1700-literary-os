from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from v1700.stage110.orchestrator import run_stage110
from v1700.gates.stage110_release_gate import run_stage110_release_gate

ROOT = Path(__file__).resolve().parents[1]

def test_stage110_orchestrator_passes():
    result = run_stage110(ROOT)
    assert result['status'] == 'pass'
    assert result['stable_lineage_frozen'] is True

def test_stage110_release_gate_passes():
    result = run_stage110_release_gate(ROOT)
    assert result['status'] == 'pass'
    assert result['live_provider_call_count_in_release_gate'] == 0

def test_stage110_provider_privacy_invariants():
    result = run_stage110(ROOT)
    assert result['raw_manuscript_provider_leakage'] == 0
    assert result['node2_raw_reveal_access'] == 0
    assert result['credential_leakage'] == 0

def test_stage110_stable_readiness_matrix_all_true():
    result = run_stage110(ROOT)
    assert all(result['stable_readiness_matrix'].values())

def test_stage110_docs_and_manifest_exist():
    assert (ROOT / 'docs/stages/stage110.md').exists()
    assert (ROOT / 'manifests/stage110_manifest.json').exists()
    assert 'Stage110' in (ROOT / 'README.md').read_text(encoding='utf-8')

def test_stage110_no_live_provider_in_release_gate():
    result = run_stage110_release_gate(ROOT)
    assert result['checks']['provider_zero_pass']['status'] == 'pass'
    assert result['checks']['sandbox_release_isolation_pass']['status'] == 'pass'
