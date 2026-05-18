from pathlib import Path
from v1700.provider_live_sandbox.benchmark_runner import run_provider_benchmark
from v1700.provider_live_sandbox.result_scorer import score_results
from v1700.gates.stage107_5_sandbox_gate import run_stage107_5_sandbox_gate

def test_benchmark_default_dry_run_no_live_calls():
    result = run_provider_benchmark(('openai','ollama'), 1)
    assert result['status'] == 'pass'
    assert result['provider_live_call_count'] == 0
    assert result['raw_manuscript_sent'] is False
    assert score_results(result)['status'] == 'pass'

def test_stage107_5_sandbox_gate_passes():
    result = run_stage107_5_sandbox_gate(Path.cwd())
    assert result['status'] == 'pass'
    assert result['live_provider_call_count_in_release_gate'] == 0
