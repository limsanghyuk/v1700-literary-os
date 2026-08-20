#!/usr/bin/env python3
"""Freeze E11-C4 predictions from E10 pre-unblind controller decisions only."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


MATERIAL_ACTIONS = {
    "PATCH_SECONDARY",
    "ADD_CONFIRMED_BRANCH",
    "CLOSE_SECONDARY_BRANCH",
    "PROMOTE_DUAL_CARRIER",
    "SWITCH_CARRIER_MINIMAL_DELTA",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def explicit_episode_axis_evidence(reason: str) -> bool:
    normalized = " ".join(reason.lower().split())
    episode_axis = "회차" in normalized and ("axis" in normalized or "carrier" in normalized)
    terminal = any(token in normalized for token in ("완료", "전환", "확정"))
    next_carrier_fixed = "다음 carrier" in normalized and "확정" in normalized
    explicit_negation = "episode carrier" in normalized and "아님" in normalized
    return (episode_axis and terminal or next_carrier_fixed) and not explicit_negation


def baseline_scope(row: dict) -> str:
    if row.get("completion") and row.get("phase"):
        return "L3"
    if row.get("phase"):
        return "L2"
    return "L1"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.decisions.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    maxima = defaultdict(int)
    for row in rows:
        maxima[row["work"]] = max(maxima[row["work"]], int(row["checkpoint"]))

    frozen = []
    for row in rows:
        scope = baseline_scope(row)
        c4_scope = scope if scope != "L3" or explicit_episode_axis_evidence(row["reason"]) else "L2"
        final = int(row["checkpoint"]) == maxima[row["work"]]
        material = row["action"] in MATERIAL_ACTIONS
        frozen.append(
            {
                "work": row["work"],
                "episode": 15,
                "seq": f"S{int(row['checkpoint']):02d}",
                "checkpoint": int(row["checkpoint"]),
                "sequence_count": maxima[row["work"]],
                "is_final_sequence": final,
                "completion_signal": bool(row.get("completion")),
                "phase_signal": bool(row.get("phase")),
                "controller_action": row["action"],
                "controller_reason": row["reason"],
                "c2_scope_pred": scope,
                "c4_scope_pred": c4_scope,
                "a1_explicit_episode_axis_evidence": explicit_episode_axis_evidence(row["reason"]),
                "c2_material": material,
                "c4_material": material and not final,
                "c4_terminal_policy": "EXIT_STATE_ONLY" if final else "NORMAL",
            }
        )

    ledger = output / "PREUNBLIND_C2_C4_PREDICTIONS.jsonl"
    with ledger.open("w", encoding="utf-8", newline="\n") as handle:
        for row in frozen:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    metadata = {
        "schema": "E11_C4_ARCHIVAL_HOLDOUT_PREUNBLIND_FREEZE_R1",
        "date": "2026-08-20",
        "experiment_type": "archival holdout; E10 decisions were frozen before E10 target unblinding",
        "source_decisions": str(source),
        "source_decisions_sha256": sha256(source),
        "excluded_e11_works": ["국희", "궁", "녹두꽃", "대물", "대장금", "뉴하트"],
        "targets": dict(sorted(maxima.items())),
        "observations": len(frozen),
        "scope_mapping": {
            "L3": "completion=true and phase=true",
            "L2": "phase=true without joint completion",
            "L1": "otherwise",
        },
        "a1_rule": (
            "retain L3 only for explicit episode-axis completion/transition/fixation language; "
            "otherwise downgrade L3 to L2"
        ),
        "a2_rule": "suppress material replanning at each work's final Sequence; exit-state only",
        "material_actions": sorted(MATERIAL_ACTIONS),
        "holdout_episode_plan_read_by_this_program": False,
        "holdout_episode_arc_read_by_this_program": False,
        "ledger": ledger.name,
        "ledger_sha256": sha256(ledger),
        "provider_call_count": 0,
        "promotion_claim": False,
    }
    freeze = output / "PREUNBLIND_FREEZE_MANIFEST.json"
    freeze.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "PREUNBLIND_FREEZE_SHA256.txt").write_text(
        f"{sha256(freeze)}  {freeze.name}\n{sha256(ledger)}  {ledger.name}\n", encoding="ascii"
    )
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
