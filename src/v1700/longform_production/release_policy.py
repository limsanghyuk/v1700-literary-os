from __future__ import annotations

def build_longform_production_release_policy() -> dict:
    return {
        'stage':'107.5','title':'Longform Production Suite Release Policy','status':'pass',
        'provider_default_calls':0,'live_provider_call_count_in_release_gate':0,
        'raw_manuscript_provider_leakage':0,'node2_raw_reveal_access':0,'credential_leakage':0,
        'full_text_export_default':False,'local_only_production_workspace':True,
        'branchpoint_lineage_preserved':True,
        'policy':['production suite stores feature-level schedules and ledgers','raw manuscript text is never required for release evidence','longform export remains feature-only unless local explicit export is requested'],
    }
