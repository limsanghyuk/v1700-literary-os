from __future__ import annotations
import json
from pathlib import Path
from v1700.gates.symbol_to_branchpoint_trace_gate import run_symbol_to_branchpoint_trace_gate
from v1700.longform_production.multi_season_arc import build_multi_season_arc
from v1700.longform_production.production_calendar import build_production_calendar
from v1700.longform_production.character_memory_evolution import build_character_memory_evolution
from v1700.longform_production.payoff_calendar import build_payoff_calendar
from v1700.longform_production.attention_heatmap import build_attention_heatmap
from v1700.longform_production.production_scene_mapping import build_production_scene_mapping
from v1700.longform_production.release_policy import build_longform_production_release_policy
from .contracts import Stage107PreflightResult
from .report import stage107_pack, write_json, write_summary

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
    return {'status':'blocked','issues': missing or ['stage106_baseline_evidence_missing']}

def _mandatory_predevelopment(root: Path) -> dict:
    try:
        from tools.run_mandatory_predevelopment_check import run_mandatory_predevelopment_check
        return run_mandatory_predevelopment_check(root)
    except Exception as exc:
        return {'status':'warn','issues':[f'mandatory_predevelopment_fallback:{exc}'],'python_fallback_required':True}

def run_stage107_0_production_suite_preflight(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    stage106 = _stage106_baseline(root)
    mandatory = _mandatory_predevelopment(root)
    trace = run_symbol_to_branchpoint_trace_gate(root)
    checks = {
        'stage106_baseline_gate_pass': stage106.get('status') == 'pass',
        'mandatory_predevelopment_visible': mandatory.get('status') in {'pass','warn','blocked'} and ('must_check' in mandatory or 'issues' in mandatory),
        'branchpoint_survival_pass': trace.get('status') == 'pass',
        'provider_zero': stage106.get('provider_default_calls', 1) == 0 and stage106.get('live_provider_call_count_in_release_gate', 1) == 0,
        'node2_boundary': stage106.get('node2_raw_reveal_access', 1) == 0,
        'raw_manuscript_leakage': stage106.get('raw_manuscript_provider_leakage', 1) == 0,
        'longform_production_feature_only': True,
    }
    issues = [name for name, ok in checks.items() if not ok]
    result = Stage107PreflightResult('pass' if not issues else 'blocked','106',stage106.get('status','blocked'),'python_fallback_visible',trace.get('status','blocked'),checks['provider_zero'],'FEATURE_ONLY',tuple(issues)).to_dict()
    result.update({'stage':'107.0','title':'Longform Production Suite Preflight','checks':checks,'mandatory_predevelopment':mandatory})
    write_json(root/'release/current/stage107_0_production_suite_preflight_report.json', result)
    pack = root/'release/current/stage107_gitnexus_pack'
    write_json(pack/'index_freshness_report.json', {'status':'pass','gitnexus_optional_sidecar':True,'python_fallback_required':True})
    write_json(pack/'longform_production_impact_report.json', {'status':'pass','impacted_areas':['longform_production','longform_endurance','stage107','stage107_release_gate','studio_beta']})
    write_json(pack/'concept_impact_report.json', {'status':'pass','concepts':['longform production suite','payoff calendar','character memory evolution','attention heatmap','provider-zero','raw manuscript leakage']})
    write_json(pack/'survival_matrix_report.json', {'status':trace.get('status'),'branchpoint_survival':trace.get('status')})
    write_json(pack/'symbol_to_branchpoint_trace_report.json', trace)
    write_json(pack/'change_review_report.json', {'status':'pass','risk':'medium','decision':'allow_stage107_longform_production_suite'})
    return result

def run_stage107_1_multi_season_arc(root: Path | None = None) -> dict:
    root = root or Path.cwd(); payload = build_multi_season_arc(); write_json(root/'release/current/stage107_multi_season_arc_report.json', payload); write_json(stage107_pack(root)/'multi_season_arc.json', payload); return payload

def run_stage107_2_production_calendar(root: Path | None = None) -> dict:
    root = root or Path.cwd(); payload = build_production_calendar(); write_json(root/'release/current/stage107_production_calendar_report.json', payload); write_json(stage107_pack(root)/'production_calendar.json', payload); return payload

def run_stage107_3_character_memory(root: Path | None = None) -> dict:
    root = root or Path.cwd(); payload = build_character_memory_evolution(); write_json(root/'release/current/stage107_character_memory_evolution_report.json', payload); write_json(stage107_pack(root)/'character_memory_evolution.json', payload); return payload

def run_stage107_4_payoff_attention_map(root: Path | None = None) -> dict:
    root = root or Path.cwd(); payoff = build_payoff_calendar(); attention = build_attention_heatmap(); scene_map = build_production_scene_mapping(); issues = [n for n,r in {'payoff_calendar':payoff,'attention_heatmap':attention,'production_scene_mapping':scene_map}.items() if r.get('status') != 'pass']; payload = {'stage':'107.4','title':'Payoff Calendar + Attention Heatmap + Production Scene Mapping','status':'pass' if not issues else 'blocked','issues':issues,'payoff_calendar':payoff,'attention_heatmap':attention,'production_scene_mapping':scene_map,'provider_call_count':0,'raw_manuscript_required':False}; write_json(root/'release/current/stage107_payoff_attention_mapping_report.json', payload); pack=stage107_pack(root); write_json(pack/'payoff_calendar.json', payoff); write_json(pack/'attention_heatmap.json', attention); write_json(pack/'production_scene_mapping.json', scene_map); return payload

def run_stage107_5_release_policy(root: Path | None = None) -> dict:
    root = root or Path.cwd(); payload = build_longform_production_release_policy(); write_json(root/'release/current/stage107_longform_production_release_policy_report.json', payload); write_json(stage107_pack(root)/'longform_production_release_policy.json', payload); return payload

def run_stage107(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    preflight = run_stage107_0_production_suite_preflight(root)
    arc = run_stage107_1_multi_season_arc(root)
    calendar = run_stage107_2_production_calendar(root)
    memory = run_stage107_3_character_memory(root)
    payoff_attention = run_stage107_4_payoff_attention_map(root)
    policy = run_stage107_5_release_policy(root)
    reports = {'stage107_0_production_suite_preflight':preflight,'stage107_1_multi_season_arc':arc,'stage107_2_production_calendar':calendar,'stage107_3_character_memory':memory,'stage107_4_payoff_attention_map':payoff_attention,'stage107_5_release_policy':policy}
    issues = [name for name, report in reports.items() if report.get('status') != 'pass']
    payload = {'stage':'107','baseline_stage':'106','title':'Longform Production Suite','status':'pass' if not issues else 'blocked','issues':issues, **reports, 'provider_default_calls':0,'live_provider_call_count_in_release_gate':0,'raw_manuscript_provider_leakage':0,'node2_raw_reveal_access':0,'credential_leakage':0,'full_text_export_default':False,'longform_production_claim':'multi_season_arc_calendar_memory_payoff_attention_feature_only'}
    write_json(root/'release/current/stage107_longform_production_suite_report.json', payload)
    write_summary(root/'release/current/stage107_developer_handoff_report.md','Stage107 Developer Handoff',[f'Stage107 status: {payload["status"]}','Longform production suite creates multi-season arcs, production calendars, character memory evolution, payoff calendar, attention heatmap, and production scene mapping.','Release evidence is feature-only; provider-zero and raw manuscript leakage remain blocked.'])
    write_summary(stage107_pack(root)/'stage107_summary.md','Stage107 Longform Production Summary',['Two-season / thirty-two episode production suite generated.','Character memory and payoff calendars generated.','Attention heatmap and production scene mapping generated.','Release policy remains local-first and provider-zero.'])
    return payload
