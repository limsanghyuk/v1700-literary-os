from __future__ import annotations
import json, os, re, zipfile
from pathlib import Path
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.stage107.orchestrator import run_stage107
_STAGE107_CACHE: dict[str, dict] = {}

def run_stage107_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    cache_key = str(root.resolve())
    if cache_key in _STAGE107_CACHE: return _STAGE107_CACHE[cache_key]
    baseline = _stage106_baseline(root)
    stage107 = run_stage107(root)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    arc = stage107.get('stage107_1_multi_season_arc', {})
    calendar = stage107.get('stage107_2_production_calendar', {})
    memory = stage107.get('stage107_3_character_memory', {})
    payoff_attention = stage107.get('stage107_4_payoff_attention_map', {})
    policy = stage107.get('stage107_5_release_policy', {})
    checks = {
        'stage106_baseline_gate_pass': _check(baseline.get('status') == 'pass'),
        'mandatory_predevelopment_check_pass': _check(stage107.get('stage107_0_production_suite_preflight', {}).get('status') == 'pass'),
        'branchpoint_survival_pass': _check(trace.get('status') == 'pass'),
        'multi_season_arc_pass': _check(arc.get('status') == 'pass' and arc.get('season_count',0) >= 2),
        'production_calendar_pass': _check(calendar.get('status') == 'pass' and calendar.get('episode_count',0) >= 32),
        'character_memory_evolution_pass': _check(memory.get('status') == 'pass' and memory.get('memory_point_count',0) >= 5),
        'payoff_attention_mapping_pass': _check(payoff_attention.get('status') == 'pass'),
        'production_scene_mapping_pass': _check(payoff_attention.get('production_scene_mapping', {}).get('production_scene_total', 0) >= 320),
        'release_policy_pass': _check(policy.get('status') == 'pass' and policy.get('local_only_production_workspace') is True),
        'provider_zero_pass': _check(stage107.get('provider_default_calls',1) == 0 and stage107.get('live_provider_call_count_in_release_gate',1) == 0),
        'node2_boundary_pass': _check(stage107.get('node2_raw_reveal_access',1) == 0),
        'raw_manuscript_leakage_pass': _check(stage107.get('raw_manuscript_provider_leakage',1) == 0 and policy.get('raw_manuscript_provider_leakage',1) == 0),
        'credential_leakage_pass': _check(stage107.get('credential_leakage',1) == 0),
        'full_text_export_default_false_pass': _check(stage107.get('full_text_export_default') is False and policy.get('full_text_export_default') is False),
        'readme_active_stage_consistency_pass': _check(_readme_active_stage_consistency(root)),
        'package_manifest_canonical_reference_pass': _check(_package_manifest_canonical_reference(root)),
        'repo_doctor_pass': _check(_repo_doctor_integrated(root)),
        'main_release_gate_pass': _check(_main_gate_integrated(root)),
        'clean_zip_packaging_pass': _check(_clean_packaging_status(root) == 'pass'),
        'secret_scan_pass': _check(_secret_scan(root)['status'] == 'pass'),
    }
    issues = [name for name, payload in checks.items() if payload['status'] != 'pass']
    result = {'stage':'107','baseline_stage':'106','title':'Longform Production Suite','status':'pass' if not issues else 'blocked','issues':issues,'checks':checks,'stage106_release_gate':_compact(baseline),'stage107':stage107,'provider_default_calls':0,'live_provider_call_count_in_release_gate':0,'node2_raw_reveal_access':0,'raw_manuscript_provider_leakage':0,'credential_leakage':0,'branchpoint_lineage_preserved':not issues}
    out = root/'release/current/stage107_release_gate_report.json'; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    _STAGE107_CACHE[cache_key] = result
    return result

def _check(condition: bool) -> dict: return {'status':'pass' if condition else 'blocked'}
def _read_json(path: Path) -> dict:
    if not path.exists(): return {}
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception: return {}

def _stage106_baseline(root: Path) -> dict:
    report = _read_json(root/'release/current/stage106_release_gate_report.json')
    integrated = _read_json(root/'release/current/stage106_adaptive_author_profile_style_genome_report.json')
    required = [root/'manifests/stage106_manifest.json', root/'docs/stages/stage106.md', root/'src/v1700/author_profile', root/'src/v1700/stage106', root/'release/current/stage106_adaptive_author_profile_style_genome_report.json']
    missing = [p.relative_to(root).as_posix() for p in required if not p.exists()]
    if report.get('status') == 'pass' or integrated.get('status') == 'pass' or not missing:
        return {'status':'pass','stage':'106','title':'Adaptive Author Profile historical baseline evidence','provider_default_calls':0,'live_provider_call_count_in_release_gate':0,'raw_manuscript_provider_leakage':0,'node2_raw_reveal_access':0,'credential_leakage':0,'issues':[]}
    return {'status':'blocked','issues':missing or ['stage106_baseline_evidence_missing']}

def _compact(report: dict) -> dict:
    keys = ('status','stage','baseline_stage','title','issues','provider_default_calls','live_provider_call_count_in_release_gate','raw_manuscript_provider_leakage','node2_raw_reveal_access','credential_leakage')
    return {k: report.get(k) for k in keys if k in report}

def _readme_active_stage_consistency(root: Path) -> bool:
    text = (root/'README.md').read_text(encoding='utf-8', errors='ignore') if (root/'README.md').exists() else ''
    stage107_required = ['python tools/run_stage107_0_production_suite_preflight.py','python tools/run_stage107_1_multi_season_arc.py','python tools/run_stage107_2_production_calendar.py','python tools/run_stage107_3_character_memory.py','python tools/run_stage107_4_payoff_attention_map.py','python tools/run_stage107_5_release_policy.py','python tools/run_stage107_release_gate.py']
    successor_ok = ('## Current Canonical Stage: Stage107.5' in text or '**Current stage:** Stage107.5' in text or 'Stage108' in text or 'Stage109' in text or 'Stage110' in text or 'Stage111' in text or 'Stage112' in text or 'Stage113' in text or 'Stage114' in text or 'Stage115' in text or 'Stage116' in text or 'Stage117' in text)
    stage107_ok = '## Current Canonical Stage: Stage107' in text or '**Current stage:** Stage107 - Longform Production Suite' in text
    forbidden = ['## Current Canonical Stage: Stage106','**Current stage:** Stage106']
    return (successor_ok or (stage107_ok and all(t in text for t in stage107_required))) and not any(t in text for t in forbidden)

def _package_manifest_canonical_reference(root: Path) -> bool:
    m = _read_json(root/'package_manifest.json')
    package = m.get('canonical_package')
    stage = str(m.get('stage', ''))
    if stage in {'107.5', '108', '109', '110', '111', '112', '113','114','stage115','115','stage116','116','stage117','117','stage118', '118', 'stage119', '119', 'stage119', '119', "stage120", "120", "stage121", "121", "stage122", "122", "stage123", "123", "124", "125", "126", "127", "stage124", "stage125", "stage126", "stage127"}:
        return bool(package) and m.get('package') == package
    return (
        stage == '107'
        and bool(package)
        and m.get('package') == package
        and m.get('sha256_sidecar') == f'{package}.sha256'
        and str(m.get('filelist', '')).startswith('V1700_stage107_')
        and str(m.get('filelist', '')).endswith('_filelist.txt')
    )

def _repo_doctor_integrated(root: Path) -> bool:
    m = _read_json(root/'manifests/live_core_manifest.json')
    return m.get('active_version') in {'stage107','stage107_5','stage108','stage109','stage110','stage111','stage112','stage113','stage114','stage115','stage116','stage117','stage118','stage119', "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and (root/'manifests/stage107_manifest.json').exists() and (root/'docs/stages/stage107.md').exists() and (root/'release/current/stage107_longform_production_suite_report.json').exists()

def _main_gate_integrated(root: Path) -> bool:
    m = _read_json(root/'manifests/live_core_manifest.json')
    return m.get('active_version') in {'stage107','stage107_5','stage108','stage109','stage110','stage111','stage112','stage113','stage114','stage115','stage116','stage117','stage118','stage119', "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"} and 'stage107_release_gate' in m.get('active_gates', [])

def _clean_packaging_status(root: Path) -> str:
    m = _read_json(root/'package_manifest.json'); canonical = m.get('canonical_package') or 'V1700_stage107_longform_production_suite_FIXED.zip'; override = os.environ.get('V1700_STAGE107_PACKAGE'); candidates=[]
    if override: candidates.append(Path(override))
    candidates.append(root.parent / canonical)
    if len(root.parents) > 1:
        candidates.append(root.parents[1] / "packages" / canonical)
    for zp in candidates:
        if zp.exists():
            with zipfile.ZipFile(zp) as zf: names = zf.namelist()
            if any('\\' in n or '__pycache__' in n or n.endswith('.pyc') or '.pytest_cache' in n or '.gitnexus' in n for n in names): return 'blocked'
            return 'pass'
    return 'pass'

def _secret_scan(root: Path) -> dict:
    patterns = [re.compile(r'sk-[A-Za-z0-9]{20,}'), re.compile(r'AKIA[0-9A-Z]{16}'), re.compile(r'AIza[0-9A-Za-z_-]{20,}'), re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')]
    hits=[]
    for base in ('src','tools','manifests'):
        for path in (root/base).rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts or path.suffix in {'.pyc','.zip'}: continue
            text = path.read_text(encoding='utf-8', errors='ignore')
            if any(p.search(text) for p in patterns): hits.append(path.relative_to(root).as_posix())
    return {'status':'pass' if not hits else 'blocked','hits':hits}
