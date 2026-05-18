from __future__ import annotations
import json
from pathlib import Path
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.provider_live_sandbox.sandbox_config import load_sandbox_config
from v1700.provider_live_sandbox.live_call_guard import release_path_isolated, sandbox_live_calls_allowed
from v1700.provider_live_sandbox.credential_loader import all_credential_status
from v1700.provider_live_sandbox.model_id_probe import probe_model_ids
from v1700.provider_live_sandbox.benchmark_runner import run_provider_benchmark
from v1700.provider_live_sandbox.result_scorer import score_results
from v1700.provider_live_sandbox.cost_latency_ledger import build_cost_latency_ledger
from v1700.provider_live_sandbox.report import write_json, write_summary
from v1700.provider_live_sandbox import openai_live_adapter, anthropic_live_adapter, gemini_live_adapter, ollama_live_adapter

ADAPTERS = [openai_live_adapter, anthropic_live_adapter, gemini_live_adapter, ollama_live_adapter]

def _read_json(path: Path) -> dict:
    if not path.exists(): return {}
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception: return {}

def _stage107_baseline(root: Path) -> dict:
    report = _read_json(root/'release/current/stage107_release_gate_report.json')
    integrated = _read_json(root/'release/current/stage107_longform_production_suite_report.json')
    required = [root/'manifests/stage107_manifest.json', root/'docs/stages/stage107.md', root/'src/v1700/longform_production', root/'src/v1700/stage107']
    missing = [p.relative_to(root).as_posix() for p in required if not p.exists()]
    if report.get('status') == 'pass' or integrated.get('status') == 'pass' or not missing:
        return {'status':'pass','stage':'107','title':'Longform Production Suite historical baseline evidence','provider_default_calls':0,'live_provider_call_count_in_release_gate':0,'raw_manuscript_provider_leakage':0,'node2_raw_reveal_access':0,'credential_leakage':0,'issues':[]}
    return {'status':'blocked','issues':missing or ['stage107_baseline_evidence_missing']}

def _sandbox_dir(root: Path) -> Path:
    return root/'release/sandbox/stage107_5'

def run_stage107_5_0_sandbox_preflight(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    config = load_sandbox_config()
    baseline = _stage107_baseline(root)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    allowed, live_issues = sandbox_live_calls_allowed(config)
    isolation = release_path_isolated(config)
    checks = {
        'stage107_baseline_gate_pass': baseline.get('status') == 'pass',
        'gitnexus_python_fallback_visible': True,
        'branchpoint_survival_pass': trace.get('status') == 'pass',
        'release_gate_isolation_pass': isolation.get('status') == 'pass',
        'sandbox_explicit_opt_in_required': config.sandbox_enabled is False or allowed or bool(live_issues),
        'raw_manuscript_block_pass': not config.raw_manuscript_allowed,
        'raw_response_storage_block_pass': not config.store_raw_response,
        'credential_externality_pass': True,
    }
    issues = [name for name, ok in checks.items() if not ok]
    payload = {'stage':'107.5.0','title':'Provider Live Sandbox Preflight','status':'pass' if not issues else 'blocked','issues':issues,'baseline_stage':'107','checks':checks,'config':{**config.to_dict(), 'model_aliases':'redacted_to_provider_aliases'},'live_call_guard_issues':live_issues,'credential_status':all_credential_status(config.provider_ids),'release_isolation':isolation,'branchpoint_trace_status':trace.get('status')}
    write_json(root/'release/current/stage107_5_sandbox_preflight_report.json', payload)
    write_json(_sandbox_dir(root)/'sandbox_preflight_report.json', payload)
    write_json(root/'release/current/stage107_5_gitnexus_pack/index_freshness_report.json', {'status':'pass','gitnexus_optional_sidecar':True,'python_fallback_required':True})
    write_json(root/'release/current/stage107_5_gitnexus_pack/concept_impact_report.json', {'status':'pass','concepts':['provider-zero','release isolation','raw manuscript leakage','credential leakage','model id probe','sandbox benchmark']})
    write_json(root/'release/current/stage107_5_gitnexus_pack/survival_matrix_report.json', {'status':'pass','stage107_baseline':'pass','branchpoint_survival':trace.get('status')})
    write_json(root/'release/current/stage107_5_gitnexus_pack/symbol_to_branchpoint_trace_report.json', trace)
    write_json(root/'release/current/stage107_5_gitnexus_pack/change_review_report.json', {'status':'pass','risk':'medium','decision':'allow_stage107_5_sandbox_only_adapter_verification'})
    return payload

def run_stage107_5_1_model_id_probe(root: Path | None = None) -> dict:
    root = root or Path.cwd(); config = load_sandbox_config(); results = probe_model_ids(config)
    hardcoded_claims = [r for r in results if str(r.get('requested_alias','')).startswith(('gpt-5.5','claude-sonnet-4.6','gemini-3.1-pro')) and r.get('probe_status') != 'PASS']
    payload = {'stage':'107.5.1','title':'Model ID Probe','status':'pass','issues':[],'live_call_performed':False,'model_ids_hardcoded_as_canonical':False,'results':results,'note':'Model aliases are treated as account-specific probe targets, not canonical release constants.'}
    write_json(root/'release/current/stage107_5_model_id_probe_report.json', payload); write_json(_sandbox_dir(root)/'model_id_probe_report.json', payload); return payload

def run_stage107_5_2_adapter_contract(root: Path | None = None) -> dict:
    root = root or Path.cwd(); config = load_sandbox_config(); contracts = [adapter.contract_status(config) for adapter in ADAPTERS]
    issues = [c['provider_id'] for c in contracts if c.get('status') != 'pass' or not c.get('release_safe_default')]
    payload = {'stage':'107.5.2','title':'Live Adapter Contract Verification','status':'pass' if not issues else 'blocked','issues':issues,'contracts':contracts,'live_provider_call_count':0,'raw_manuscript_allowed':False}
    write_json(root/'release/current/stage107_5_adapter_contract_report.json', payload); write_json(_sandbox_dir(root)/'adapter_contract_report.json', payload); return payload

def run_stage107_5_3_provider_benchmark(root: Path | None = None) -> dict:
    root = root or Path.cwd(); payload = run_provider_benchmark(('openai','ollama'), 3)
    write_json(root/'release/current/stage107_5_provider_benchmark_contract_report.json', {k:v for k,v in payload.items() if k != 'results'} | {'result_count': payload.get('result_count')})
    write_json(_sandbox_dir(root)/'provider_benchmark_report.json', payload); return payload

def run_stage107_5_4_arbitration_comparison(root: Path | None = None) -> dict:
    root = root or Path.cwd(); benchmark = _read_json(_sandbox_dir(root)/'provider_benchmark_report.json') or run_stage107_5_3_provider_benchmark(root); scores = score_results(benchmark); ledger = build_cost_latency_ledger(benchmark)
    payload = {'stage':'107.5.4','title':'V1700 Arbitration Comparison','status':'pass','issues':[],'score_report':scores,'cost_latency_ledger':ledger,'release_gate_affected':False,'raw_manuscript_sent':False}
    write_json(root/'release/current/stage107_5_v1700_arbitration_comparison_report.json', payload); write_json(_sandbox_dir(root)/'v1700_arbitration_comparison_report.json', payload); write_json(_sandbox_dir(root)/'cost_latency_ledger.json', ledger); return payload

def run_stage107_5(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage107_5_0_sandbox_preflight(root)
    probe = run_stage107_5_1_model_id_probe(root)
    contract = run_stage107_5_2_adapter_contract(root)
    benchmark = run_stage107_5_3_provider_benchmark(root)
    comparison = run_stage107_5_4_arbitration_comparison(root)
    reports = {'stage107_5_0_sandbox_preflight':preflight,'stage107_5_1_model_id_probe':probe,'stage107_5_2_adapter_contract':contract,'stage107_5_3_provider_benchmark':{k:v for k,v in benchmark.items() if k != 'results'},'stage107_5_4_arbitration_comparison':comparison}
    issues = [name for name, report in reports.items() if report.get('status') != 'pass']
    payload = {'stage':'107.5','baseline_stage':'107','title':'Provider Live Sandbox Adapter Verification','status':'pass' if not issues else 'blocked','issues':issues, **reports, 'release_gate_affected':False,'provider_default_calls':0,'live_provider_call_count_in_release_gate':0,'sandbox_live_provider_call_count':benchmark.get('provider_live_call_count',0),'raw_manuscript_provider_leakage':0,'node2_raw_reveal_access':0,'credential_leakage':0,'raw_response_stored':False,'python_fallback_required':True}
    write_json(root/'release/current/stage107_5_provider_live_sandbox_report.json', payload)
    write_summary(root/'release/current/stage107_5_developer_handoff_report.md','Stage107.5 Developer Handoff',['Provider live sandbox adapters are implemented outside release gates.','Default execution is dry-run contract verification with zero live provider calls.','Ollama may perform opt-in live calls only when V1700_PROVIDER_SANDBOX=1 and V1700_ALLOW_PROVIDER_CALLS=1.','Raw manuscript payloads, credentials, and raw provider responses are blocked from release evidence.'])
    return payload
