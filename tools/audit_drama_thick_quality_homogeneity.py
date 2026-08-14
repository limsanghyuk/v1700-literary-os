#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

FLOOR = {
    'avg_event_chars': 114.35,
    'avg_cast_function_chars': 54.85,
    'info_shift_per_seq': 0.98,
    'plant_payoff_per_seq': 1.17,
}

def load_jsonl(path):
    out=[]
    with open(path,encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line: out.append(json.loads(line))
    return out

def mean(v): return sum(v)/len(v) if v else 0.0

def norm_cast(s):
    s=(s or '').strip()
    if ':' in s[:20]: s=s.split(':',1)[1].strip()
    s=re.sub(r'^[가-힣A-Za-z0-9·\s]{1,12}(?:은|는|이|가)\s+','',s)
    return re.sub(r'\s+',' ',s)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',required=True,help='Extracted DB root containing seqcard_ko')
    ap.add_argument('--out',required=True)
    a=ap.parse_args()
    root=Path(a.root)
    rf=root/'seqcard_ko'/'reinforcement_v1'
    manifests=sorted(rf.glob('FINAL_THICK_*WORK_AUTHORITY_*CANONICAL.json'))
    if not manifests: raise SystemExit('No FINAL_THICK authority manifest')
    auth=json.loads(manifests[-1].read_text(encoding='utf-8'))
    works=auth['works']
    sem_path=next((rf/'validation').rglob(f'THICK_{len(works)}WORK_SEMANTIC_INDEPENDENCE_AUDIT_V3_*.json'))
    exact_path=next((rf/'validation').rglob(f'THICK_{len(works)}WORK_EXACT_SCHEMA_PROVENANCE_SOURCE_VALIDATION_*.json'))
    sem=json.loads(sem_path.read_text(encoding='utf-8'))
    exact=json.loads(exact_path.read_text(encoding='utf-8'))
    rows=[]
    for w in works:
        recs=[]
        for fp in sorted((rf/'thick_sequence'/w).glob('*.jsonl')): recs += load_jsonl(fp)
        scenes=[]
        for fp in sorted((root/'seqcard_ko'/'authored').glob(f'{w}_*.seqcard.jsonl')): scenes += load_jsonl(fp)
        s2=[]
        for fp in sorted((root/'seqcard_ko'/'authored_seq').glob(f'{w}_*.seqblueprint.jsonl')): s2 += load_jsonl(fp)
        ev=[x.get('event','') for x in recs]
        cf=[c.get('desire_or_function','') for x in recs for c in x.get('cast',[])]
        body=[norm_cast(x) for x in cf]
        info=[len(x.get('info_shift',[])) for x in recs]
        pp=[len(x.get('plant_payoff',[])) for x in recs]
        skins=[x.get('skin','') for x in scenes]
        same_dup=0; same_total=0
        for x in recs:
            b=[norm_cast(c.get('desire_or_function','')) for c in x.get('cast',[])]
            same_dup += len(b)-len(set(b)); same_total += len(b)
        s2chars=mean([len(x.get('sequence_intent',''))+len(x.get('goal',''))+len(x.get('obstacle','')) for x in s2])
        vals={
            'avg_event_chars':mean([len(x) for x in ev]),
            'avg_cast_function_chars':mean([len(x) for x in cf]),
            'info_shift_per_seq':mean(info),
            'plant_payoff_per_seq':mean(pp),
        }
        floor_pass=sum(vals[k]>=v for k,v in FLOOR.items())
        sl_candidates=list((root/'seqcard_ko'/'source_lock'/'current').glob(f'{w}*'))
        sl={}
        if sl_candidates:
            try: sl=json.loads(sl_candidates[0].read_text(encoding='utf-8'))
            except Exception: pass
        rows.append({
            'work':w,'sequences':len(recs),'stage01_scenes':len(scenes),
            **{k:round(v,3) for k,v in vals.items()},'q25_floor_pass_count':floor_pass,
            'stage01_skin_exact_repeat_pct':round((1-len(set(skins))/len(skins))*100,2) if skins else 0,
            'thick_cast_body_exact_repeat_pct':round((1-len(set(body))/len(body))*100,2) if body else 0,
            'same_seq_cast_body_repeat_pct':round(same_dup/max(1,same_total)*100,2),
            'stage02_semantic_chars_avg':round(s2chars,2),
            'semantic_independence':sem['works'][w]['status'],
            'exact_provenance':exact['works'][w]['status'],
            'direct_reading_attested':sl.get('direct_reading_attested'),
            'source_provenance_class':sl.get('source_provenance_class'),
        })
    out={
        'schema':'DRAMA_THICK_QUALITY_HOMOGENEITY_DIAGNOSTIC_V1',
        'authority_id':auth.get('authority_id'),
        'works_total':len(works),
        'q25_floor':FLOOR,
        'works':rows,
        'note':'Diagnostics do not replace direct-source semantic review. Prefix-stripped cast duplication and Stage01 skin repetition close gaps not covered by the older strict gate.'
    }
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':'PASS','works':len(rows),'out':a.out},ensure_ascii=False))
if __name__=='__main__': main()
