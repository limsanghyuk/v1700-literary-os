#!/usr/bin/env python3
"""Mechanical guard for long drama-analysis THICK runs.

This tool does not generate narrative meaning. It only enforces durable progress,
response leases, and phase ordering.
"""
import argparse, hashlib, json, os, tempfile
from datetime import datetime, timezone
from pathlib import Path

MAX_NEW_SEQUENCES = 3
PHASE_ORDER = [
    "THICK_AUTHORING",
    "WHOLE_WORK_GATE",
    "R5_BUILD",
    "R8_BUILD",
    "DB_INTEGRATION",
    "CHECKSUM_BUILD",
    "ZIP_BUILD",
    "FRESH_EXTRACTION",
    "HUB_PROMOTION",
    "DONE",
]


def now():
    return datetime.now(timezone.utc).isoformat()


def fail(message, code=2):
    print(json.dumps({"status": "FAIL", "error": message}, ensure_ascii=False))
    raise SystemExit(code)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
        dfd = os.open(str(path.parent), os.O_DIRECTORY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def init_state(a):
    p = Path(a.state)
    if p.exists() and not a.force:
        fail("state already exists")
    data = {
        "schema": "DRAMA_ANALYSIS_EXECUTION_GUARD_V1",
        "work_id": a.work_id,
        "episodes_total": a.episodes_total,
        "sequences_total": a.sequences_total,
        "locked_sequences": a.locked_sequences,
        "last_locked_seq_id": a.last_locked_seq_id,
        "next_seq_id": a.next_seq_id,
        "phase": "THICK_AUTHORING",
        "phase_passes": {},
        "active_lease": None,
        "max_new_sequences_per_response": MAX_NEW_SEQUENCES,
        "source_read_without_commit_is_progress": False,
        "forbid_cross_phase_same_response": True,
        "updated_at": now(),
    }
    atomic_write(p, data)
    print(json.dumps({"status": "PASS", "state": data}, ensure_ascii=False))


def status(a):
    print(json.dumps({"status": "PASS", "state": load(a.state)}, ensure_ascii=False, indent=2))


def open_lease(a):
    p = Path(a.state)
    d = load(p)
    if d["phase"] != "THICK_AUTHORING":
        fail("semantic lease allowed only in THICK_AUTHORING")
    if d.get("active_lease"):
        fail("lease already OPEN")
    if d["locked_sequences"] >= d["sequences_total"]:
        fail("THICK already complete")
    d["active_lease"] = {
        "lease_id": a.lease_id,
        "state": "OPEN",
        "start_locked_count": d["locked_sequences"],
        "start_seq_id": d["next_seq_id"],
        "max_new_sequences": MAX_NEW_SEQUENCES,
        "committed_count": 0,
        "accepted_seq_ids": [],
        "opened_at": now(),
    }
    d["updated_at"] = now()
    atomic_write(p, d)
    print(json.dumps({"status": "PASS", "lease": d["active_lease"]}, ensure_ascii=False))


def commit(a):
    p = Path(a.state)
    d = load(p)
    lease = d.get("active_lease")
    if not lease or lease.get("state") != "OPEN":
        fail("no OPEN lease")
    if lease["committed_count"] >= lease["max_new_sequences"]:
        fail("LEASE_LIMIT_REACHED: fourth semantic sequence is mechanically forbidden", 3)
    if a.seq_id != d["next_seq_id"]:
        fail(f"seq_id must equal durable next_seq_id {d['next_seq_id']}")
    lease["accepted_seq_ids"].append(a.seq_id)
    lease["committed_count"] += 1
    d["locked_sequences"] += 1
    d["last_locked_seq_id"] = a.seq_id
    if d["locked_sequences"] == d["sequences_total"]:
        d["next_seq_id"] = None
    elif a.next_seq_id:
        d["next_seq_id"] = a.next_seq_id
    else:
        fail("--next-seq-id is required until the final sequence")
    d["updated_at"] = now()
    atomic_write(p, d)
    print(json.dumps({"status": "PASS", "committed_count": lease["committed_count"], "locked_sequences": d["locked_sequences"], "next_seq_id": d["next_seq_id"]}, ensure_ascii=False))


def close_lease(a):
    p = Path(a.state)
    d = load(p)
    lease = d.get("active_lease")
    if not lease:
        fail("no active lease")
    lease["state"] = "CLOSED"
    lease["closed_at"] = now()
    d["last_closed_lease"] = lease
    d["active_lease"] = None
    d["updated_at"] = now()
    atomic_write(p, d)
    print(json.dumps({"status": "PASS", "closed_lease": lease, "next_seq_id": d["next_seq_id"]}, ensure_ascii=False))


def phase_pass(a):
    p = Path(a.state)
    d = load(p)
    if a.phase not in PHASE_ORDER:
        fail("unknown phase")
    if d["phase"] != a.phase:
        fail(f"can only PASS current phase {d['phase']}")
    if d.get("active_lease"):
        fail("close semantic lease before phase transition")
    if a.phase == "THICK_AUTHORING" and d["locked_sequences"] != d["sequences_total"]:
        fail(f"cannot pass THICK_AUTHORING: {d['locked_sequences']}/{d['sequences_total']}")
    evidence = Path(a.evidence)
    if not evidence.is_file():
        fail("durable evidence file missing")
    idx = PHASE_ORDER.index(a.phase)
    if idx >= len(PHASE_ORDER) - 1:
        fail("cannot advance past DONE")
    digest = hashlib.sha256(evidence.read_bytes()).hexdigest()
    d["phase_passes"][a.phase] = {
        "status": "PASS",
        "evidence": str(evidence),
        "sha256": digest,
        "passed_at": now(),
    }
    d["phase"] = PHASE_ORDER[idx + 1]
    d["updated_at"] = now()
    atomic_write(p, d)
    print(json.dumps({"status": "PASS", "passed_phase": a.phase, "next_phase": d["phase"], "evidence_sha256": digest}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    x = sp.add_parser("init")
    x.add_argument("--state", required=True); x.add_argument("--work-id", required=True)
    x.add_argument("--episodes-total", type=int, required=True); x.add_argument("--sequences-total", type=int, required=True)
    x.add_argument("--locked-sequences", type=int, required=True); x.add_argument("--last-locked-seq-id", required=True)
    x.add_argument("--next-seq-id", required=True); x.add_argument("--force", action="store_true"); x.set_defaults(fn=init_state)
    x = sp.add_parser("status"); x.add_argument("--state", required=True); x.set_defaults(fn=status)
    x = sp.add_parser("open-lease"); x.add_argument("--state", required=True); x.add_argument("--lease-id", required=True); x.set_defaults(fn=open_lease)
    x = sp.add_parser("commit"); x.add_argument("--state", required=True); x.add_argument("--seq-id", required=True); x.add_argument("--next-seq-id"); x.set_defaults(fn=commit)
    x = sp.add_parser("close-lease"); x.add_argument("--state", required=True); x.set_defaults(fn=close_lease)
    x = sp.add_parser("phase-pass"); x.add_argument("--state", required=True); x.add_argument("--phase", required=True); x.add_argument("--evidence", required=True); x.set_defaults(fn=phase_pass)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
