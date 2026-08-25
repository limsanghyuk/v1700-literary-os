#!/usr/bin/env python3
"""Drama close-reading release gate.

Validates metadata-only drama close-reading packages. This script checks
anti-template signals and structural contracts; it must not read or export raw
source scripts.
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable, Any

STAGE1_REQUIRED = {
    "work_id", "episode_no", "scene_ordinal", "source_marker_no", "source_span",
    "source_sha16", "heading", "title", "scene_action", "spoken_or_unspoken_move",
    "information_delta", "character_decision", "dramatic_function", "forward_hook",
    "stage2_hint", "evidence_control",
}

STAGE2_REQUIRED = {
    "seq_id", "work_id", "episode_no", "seq_index", "member_scene_nos", "scene_span",
    "scene_budget", "sequence_intent", "goal", "obstacle", "value_shift", "turn_type",
    "turn_class", "core_mix", "pov_char", "place_cluster", "runtime_share", "by",
}

TAXONOMY = {
    "ESTABLISH", "ORACLE", "INTRO", "BOND", "CONFLICT", "REVERSAL", "LOSS", "PUNISH",
    "REVELATION", "REUNION", "RELIEF", "ROMANCE", "PERIL", "RESCUE", "DESIRE", "HOOK",
}

SEMANTIC_FIELDS = [
    "scene_action", "spoken_or_unspoken_move", "information_delta",
    "character_decision", "dramatic_function", "forward_hook",
]

VISIBLE_REF_RE = re.compile(r"EP\d{2}[-_]\d{3}")
TEMPLATE_RE = re.compile(r"상황에서.+처리하고.+방향으로 장면을 이동시킨다")
BROKEN_PARTICLE_RE = re.compile(r"[가-힣]+(이은|가은|을를|를을|이을|가을|은는|는은)")


def _read_text(z: zipfile.ZipFile, name: str) -> str:
    return z.read(name).decode("utf-8")


def iter_jsonl(text: str) -> Iterable[dict[str, Any]]:
    for line_no, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if not isinstance(obj, dict):
            raise ValueError(f"jsonl line {line_no} is not an object")
        yield obj


def ngrams(text: str, n: int = 5) -> list[str]:
    toks = re.findall(r"[A-Za-z0-9가-힣]+", text)
    return [" ".join(toks[i:i+n]) for i in range(max(0, len(toks)-n+1))]


def validate_package(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"package": str(path), "errors": [], "warnings": [], "metrics": {}}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        stage1_names = [n for n in names if "stage1" in n and n.endswith(".jsonl") and "integrated" in n]
        stage2_names = [n for n in names if "stage2" in n and n.endswith(".json") and "integrated" in n]
        validation_names = [n for n in names if "validation" in n and n.endswith(".json")]
        raw_like = [n for n in names if ("original_extracted" in n.lower()) or ("raw" in n.lower() and "no_raw" not in n.lower())]
        if not stage1_names:
            result["errors"].append("missing integrated Stage1 jsonl")
        if not stage2_names:
            result["errors"].append("missing integrated Stage2 json")
        if raw_like:
            result["errors"].append({"raw_source_like_paths": raw_like[:20]})

        all_semantic_values: list[str] = []
        visible_refs = template_hits = broken_particles = 0
        if stage1_names:
            cards = list(iter_jsonl(_read_text(z, stage1_names[0])))
            result["metrics"]["scene_count"] = len(cards)
            ords = [c.get("scene_ordinal") for c in cards]
            if sorted(ords) != list(range(1, len(cards)+1)):
                result["errors"].append("scene ordinals are not continuous 1..N")
            for i, card in enumerate(cards, 1):
                missing = STAGE1_REQUIRED - set(card)
                if missing:
                    result["errors"].append({"scene": i, "missing_stage1_fields": sorted(missing)})
                scene_action = str(card.get("scene_action", ""))
                for f in SEMANTIC_FIELDS:
                    val = str(card.get(f, ""))
                    all_semantic_values.append(val)
                    if VISIBLE_REF_RE.search(val):
                        visible_refs += 1
                    if TEMPLATE_RE.search(val):
                        template_hits += 1
                    if BROKEN_PARTICLE_RE.search(val):
                        broken_particles += 1
                    if f != "scene_action" and scene_action and val == scene_action:
                        result["errors"].append({"scene": i, "scene_action_copied_to": f})

        exact_dups = sum(1 for _, c in Counter(v for v in all_semantic_values if v).items() if c > 1)
        ng = Counter()
        for v in all_semantic_values:
            ng.update(ngrams(v, 5))
        repeated_5gram_ge4 = sum(1 for _, c in ng.items() if c >= 4)
        result["metrics"].update({
            "visible_ep_ref_hits": visible_refs,
            "template_process_hits": template_hits,
            "broken_particle_hits": broken_particles,
            "exact_duplicate_semantic_values": exact_dups,
            "repeated_5gram_ge4": repeated_5gram_ge4,
        })
        if visible_refs:
            result["errors"].append({"visible_ep_ref_hits": visible_refs})
        if template_hits:
            result["errors"].append({"template_process_hits": template_hits})
        if broken_particles:
            result["errors"].append({"broken_particle_hits": broken_particles})
        if exact_dups:
            result["errors"].append({"exact_duplicate_semantic_values": exact_dups})
        if repeated_5gram_ge4:
            result["errors"].append({"repeated_5gram_ge4": repeated_5gram_ge4})

        if stage2_names:
            data = json.loads(_read_text(z, stage2_names[0]))
            seqs = data if isinstance(data, list) else data.get("sequences", []) if isinstance(data, dict) else []
            result["metrics"]["sequence_count"] = len(seqs)
            covered: list[int] = []
            for seq in seqs:
                missing = STAGE2_REQUIRED - set(seq)
                if missing:
                    result["errors"].append({"seq": seq.get("seq_id"), "missing_stage2_fields": sorted(missing)})
                for core in seq.get("core_mix", []) or []:
                    if core not in TAXONOMY:
                        result["errors"].append({"seq": seq.get("seq_id"), "bad_core_mix": core})
                covered.extend(seq.get("member_scene_nos", []) or [])
            if stage1_names and covered:
                n = result["metrics"].get("scene_count", 0)
                if sorted(covered) != list(range(1, n+1)):
                    result["errors"].append("Stage2 coverage is not exact 1..N")

        for vn in validation_names:
            try:
                val = json.loads(_read_text(z, vn))
            except Exception:
                continue
            raw = val.get("raw_script_exported")
            if raw is None and isinstance(val.get("metrics"), dict):
                raw = val["metrics"].get("raw_script_exported")
            if raw is True:
                result["errors"].append({"validation_claims_raw_script_exported": vn})

    result["decision"] = "PASS" if not result["errors"] else "FAIL"
    return result


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: drama_close_reading_release_gate.py <package.zip> [<package.zip> ...]", file=sys.stderr)
        return 2
    reports = [validate_package(Path(a)) for a in argv[1:]]
    print(json.dumps({"reports": reports}, ensure_ascii=False, indent=2))
    return 0 if all(r["decision"] == "PASS" for r in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
