#!/usr/bin/env python3
"""Block-Atomic V2 guard for THICK authoring.

No narrative meaning is generated here. The guard only enforces ordered atomic
commits, an at-most-eight-episode execution block, durable block gates, and
phase ordering.
"""
import argparse, hashlib, json, os, re, tempfile
from datetime import datetime, timezone
from pathlib import Path

MAX_BLOCK_EPISODES = 8
PHASE_ORDER = [
    "THICK_BLOCK_AUTHORING", "WHOLE_WORK_GATE", "R5_BUILD", "R8_BUILD",
    "DB_INTEGRATION", "CHECKSUM_BUILD", "ZIP_BUILD", "FRESH_EXTRACTION",
    "HUB_PROMOTION", "DONE",
]

def now(): return datetime.now(timezone.utc).isoformat()
def fail(msg, code=2):
    print(json.dumps({"status":"FAIL","error":msg}, ensure_ascii=False)); raise SystemExit(code)
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def atomic_write(path, data):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2,sort_keys=True); f.write("\n"); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
        dfd=os.open(str(path.parent),os.O_DIRECTORY)
        try: os.fsync(dfd)
        finally: os.close(dfd)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
def seq_ep(seq_id):
    m=re.match(r"^.+_(\d{2})_S\d+$",seq_id)
    if not m: fail(f"invalid seq_id: {seq_id}")
    return int(m.group(1))

def init_block(a):
    expected=json.loads(Path(a.expected).read_text(encoding="utf-8"))
    if not isinstance(expected,list) or not expected: fail("expected must be non-empty JSON list")
    eps=sorted(set(seq_ep(x) for x in expected))
    if len(eps)>MAX_BLOCK_EPISODES: fail("block exceeds 8 episodes")
    if eps!=list(range(min(eps),max(eps)+1)): fail("block episodes must be contiguous")
    if not 0<=a.committed<=len(expected): fail("invalid committed count")
    data={
      "schema":"DRAMA_ANALYSIS_BLOCK_GUARD_V2","work_id":a.work_id,
      "block_episode_start":min(eps),"block_episode_end":max(eps),"max_block_episodes":MAX_BLOCK_EPISODES,
      "expected_seq_ids":expected,"block_expected_sequences":len(expected),"block_committed_sequences":a.committed,
      "locked_sequences_total":a.locked_total,"sequences_total":a.sequences_total,
      "last_locked_seq_id":expected[a.committed-1] if a.committed else a.last_before,
      "next_seq_id":expected[a.committed] if a.committed<len(expected) else None,
      "phase":"THICK_BLOCK_AUTHORING","block_status":"IN_PROGRESS" if a.committed<len(expected) else "READY_FOR_BLOCK_GATE",
      "source_read_without_checkpoint_is_progress":False,"sequence_atomic_commit_required":True,
      "episode_checkpoint_required":True,"cross_phase_requires_durable_pass":True,"updated_at":now()}
    atomic_write(a.state,data); print(json.dumps({"status":"PASS","state":data},ensure_ascii=False))

def commit(a):
    d=load(a.state)
    if d["phase"]!="THICK_BLOCK_AUTHORING": fail("not in THICK_BLOCK_AUTHORING")
    i=d["block_committed_sequences"]
    if i>=len(d["expected_seq_ids"]): fail("block already complete")
    expected=d["expected_seq_ids"][i]
    if a.seq_id!=expected: fail(f"expected {expected}, got {a.seq_id}")
    for p in (a.spec,a.record,a.audit):
        fp=Path(p)
        if not fp.is_file(): fail(f"missing durable artifact: {p}")
        json.loads(fp.read_text(encoding="utf-8"))
    if load(a.audit).get("status")!="PASS": fail("audit is not PASS")
    d["block_committed_sequences"]+=1; d["locked_sequences_total"]+=1; d["last_locked_seq_id"]=a.seq_id
    j=d["block_committed_sequences"]; d["next_seq_id"]=d["expected_seq_ids"][j] if j<len(d["expected_seq_ids"]) else None
    d["block_status"]="IN_PROGRESS" if d["next_seq_id"] else "READY_FOR_BLOCK_GATE"; d["updated_at"]=now(); atomic_write(a.state,d)
    print(json.dumps({"status":"PASS","committed":a.seq_id,"block_committed":j,"locked_total":d["locked_sequences_total"],"next_seq_id":d["next_seq_id"]},ensure_ascii=False))

def block_pass(a):
    d=load(a.state)
    if d["block_committed_sequences"]!=d["block_expected_sequences"]: fail("block THICK incomplete")
    ev=Path(a.evidence)
    if not ev.is_file(): fail("block gate evidence missing")
    report=load(ev)
    if report.get("status")!="PASS": fail("block gate evidence is not PASS")
    d["block_status"]="PASS"
    d["phase"]="WHOLE_WORK_GATE" if d["locked_sequences_total"]==d["sequences_total"] else "THICK_BLOCK_AUTHORING"
    d["block_gate"]={"evidence":str(ev),"sha256":hashlib.sha256(ev.read_bytes()).hexdigest(),"passed_at":now()}; d["updated_at"]=now(); atomic_write(a.state,d)
    print(json.dumps({"status":"PASS","block_status":"PASS","next_phase":d["phase"]},ensure_ascii=False))

def phase_pass(a):
    d=load(a.state)
    if a.phase not in PHASE_ORDER or d["phase"]!=a.phase: fail(f"current phase is {d['phase']}")
    ev=Path(a.evidence)
    if not ev.is_file() or load(ev).get("status")!="PASS": fail("durable PASS evidence required")
    i=PHASE_ORDER.index(a.phase)
    if i==len(PHASE_ORDER)-1: fail("cannot advance past DONE")
    d.setdefault("phase_passes",{})[a.phase]={"status":"PASS","evidence":str(ev),"sha256":hashlib.sha256(ev.read_bytes()).hexdigest(),"passed_at":now()}
    d["phase"]=PHASE_ORDER[i+1]; d["updated_at"]=now(); atomic_write(a.state,d)
    print(json.dumps({"status":"PASS","passed_phase":a.phase,"next_phase":d["phase"]},ensure_ascii=False))

def status(a): print(json.dumps({"status":"PASS","state":load(a.state)},ensure_ascii=False,indent=2))

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest="cmd",required=True)
    p=sp.add_parser("init-block"); p.add_argument("--state",required=True); p.add_argument("--work-id",required=True); p.add_argument("--expected",required=True); p.add_argument("--committed",type=int,required=True); p.add_argument("--locked-total",type=int,required=True); p.add_argument("--sequences-total",type=int,required=True); p.add_argument("--last-before"); p.set_defaults(fn=init_block)
    p=sp.add_parser("commit"); p.add_argument("--state",required=True); p.add_argument("--seq-id",required=True); p.add_argument("--spec",required=True); p.add_argument("--record",required=True); p.add_argument("--audit",required=True); p.set_defaults(fn=commit)
    p=sp.add_parser("block-pass"); p.add_argument("--state",required=True); p.add_argument("--evidence",required=True); p.set_defaults(fn=block_pass)
    p=sp.add_parser("phase-pass"); p.add_argument("--state",required=True); p.add_argument("--phase",required=True); p.add_argument("--evidence",required=True); p.set_defaults(fn=phase_pass)
    p=sp.add_parser("status"); p.add_argument("--state",required=True); p.set_defaults(fn=status)
    a=ap.parse_args(); a.fn(a)
if __name__=="__main__": main()
