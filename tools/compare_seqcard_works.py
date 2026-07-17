"""Compare two SeqCard works without exporting scripts or authored text.

The output contains aggregate counts, schema/ID integrity, text diversity
statistics, graph shape, and audit-artifact presence only.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


TEXT_FIELDS = {
    "scenes": ("title", "intent_gist", "skin"),
    "sequences": ("sequence_intent", "goal", "obstacle"),
    "episode_arcs": (
        "dramatic_question",
        "central_conflict_axis",
        "entry_state",
        "exit_state",
        "episode_function",
    ),
    "character_arcs": ("state_label", "state_delta", "evidence"),
    "relationship_arcs": ("relation_state", "relation_delta", "evidence"),
    "local_edges": ("label", "note"),
    "payoff_candidates": ("description",),
    "cross_edges": ("label", "note"),
}


def load_json_file(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    value = json.loads(text)
    return value if isinstance(value, list) else [value]


def load_many(paths: Iterable[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(paths):
        records.extend(load_json_file(path))
    return records


def is_filled(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def normalized_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    value = re.sub(r"\s+", " ", value.strip())
    value = re.sub(r"\b(?:ep|sc|seq|lx|cx|pc)[-_]?\d+[\w-]*\b", "<ID>", value, flags=re.I)
    value = re.sub(r"\d+", "<N>", value)
    return value


def text_metrics(records: list[dict[str, Any]], fields: tuple[str, ...]) -> dict[str, Any]:
    values = [
        normalized_text(record.get(field))
        for record in records
        for field in fields
        if normalized_text(record.get(field))
    ]
    counts = Counter(values)
    repeated = sum(count for count in counts.values() if count > 1)
    tokens = [token for value in values for token in value.split()]
    placeholders = sum(
        1
        for record in records
        for field in fields
        if isinstance(record.get(field), str) and re.search(r"\{[^{}]+\}", record[field])
    )
    return {
        "value_count": len(values),
        "unique_ratio": round(len(counts) / len(values), 4) if values else 1.0,
        "duplicate_instance_ratio": round(repeated / len(values), 4) if values else 0.0,
        "average_chars": round(statistics.mean(map(len, values)), 2) if values else 0.0,
        "token_type_ratio": round(len(set(tokens)) / len(tokens), 4) if tokens else 0.0,
        "placeholder_value_count": placeholders,
    }


def layer_metrics(records: list[dict[str, Any]], fields: tuple[str, ...]) -> dict[str, Any]:
    keysets = Counter(tuple(sorted(record)) for record in records)
    all_values = sum(len(record) for record in records)
    missing_values = sum(
        1 for record in records for value in record.values() if not is_filled(value)
    )
    return {
        "records": len(records),
        "distinct_keysets": len(keysets),
        "filled_value_ratio": round((all_values - missing_values) / all_values, 4)
        if all_values
        else 1.0,
        "text": text_metrics(records, fields),
        "text_by_field": {field: text_metrics(records, (field,)) for field in fields},
        "provenance_counts": dict(Counter(record.get("by", "<missing>") for record in records)),
    }


def episode_number(path: Path) -> int | None:
    match = re.search(r"_(\d{2})\.", path.name)
    return int(match.group(1)) if match else None


def collect_work(root: Path, title: str) -> dict[str, Any]:
    patterns = {
        "scenes": root / "authored",
        "sequences": root / "authored_seq",
        "episode_arcs": root / "authored_arc",
        "character_arcs": root / "authored_chararc",
        "relationship_arcs": root / "authored_relarc",
        "local_edges": root / "authored_edges",
        "payoff_candidates": root / "authored_edges",
    }
    files = {
        "scenes": list(patterns["scenes"].glob(f"{title}_[0-9][0-9].seqcard.jsonl")),
        "sequences": list(patterns["sequences"].glob(f"{title}_[0-9][0-9].seqblueprint.jsonl")),
        "episode_arcs": list(patterns["episode_arcs"].glob(f"{title}_[0-9][0-9].episodearc.json")),
        "character_arcs": list(patterns["character_arcs"].glob(f"{title}_[0-9][0-9].chararc.jsonl")),
        "relationship_arcs": list(patterns["relationship_arcs"].glob(f"{title}_[0-9][0-9].relarc.jsonl")),
        "local_edges": list(patterns["local_edges"].glob(f"{title}_[0-9][0-9].local_edges.jsonl")),
        "payoff_candidates": list(patterns["payoff_candidates"].glob(f"{title}_[0-9][0-9].payoff_candidates.jsonl")),
    }
    records = {name: load_many(paths) for name, paths in files.items()}
    cross_path = root / "authored_edges" / f"{title}_cross_episode_edges.jsonl"
    records["cross_edges"] = load_json_file(cross_path) if cross_path.exists() else []

    episodes = sorted({episode_number(path) for path in files["scenes"]} - {None})
    if not episodes:
        raise ValueError(
            f"No SceneCard episodes found for {title!r} under {root}. "
            "Pass either the extracted package root or its seqcard_ko directory."
        )
    scenes_by_episode: dict[int, set[int]] = defaultdict(set)
    for path in files["scenes"]:
        ep = episode_number(path)
        for row in load_json_file(path):
            if ep is not None and isinstance(row.get("scene_no"), int):
                scenes_by_episode[ep].add(row["scene_no"])

    sequences_by_episode: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in records["sequences"]:
        if isinstance(row.get("episode_no"), int):
            sequences_by_episode[row["episode_no"]].append(row)

    missing_scene_coverage = 0
    overlapping_scene_memberships = 0
    for ep in episodes:
        membership: list[int] = []
        for sequence in sequences_by_episode[ep]:
            membership.extend(n for n in sequence.get("member_scene_nos", []) if isinstance(n, int))
        missing_scene_coverage += len(scenes_by_episode[ep] - set(membership))
        overlapping_scene_memberships += len(membership) - len(set(membership))

    invalid_trigger_refs = 0
    episode_work_id_mismatches = 0
    for layer in ("character_arcs", "relationship_arcs"):
        for row in records[layer]:
            ep = row.get("episode_no")
            scene = row.get("trigger_scene_no")
            if isinstance(ep, int) and isinstance(scene, int) and scene not in scenes_by_episode[ep]:
                invalid_trigger_refs += 1
            if isinstance(ep, int) and row.get("work_id") != f"{title}_{ep:02d}":
                episode_work_id_mismatches += 1

    invalid_local_edges = 0
    cross_episode_records_in_local = 0
    adjacent_scene_local_edges = 0
    for row in records["local_edges"]:
        src_ep, tgt_ep = row.get("src_episode_no"), row.get("tgt_episode_no")
        src_scene, tgt_scene = row.get("src_scene_no"), row.get("tgt_scene_no")
        valid = (
            row.get("gap_episodes") == 0
            and src_ep == tgt_ep
            and isinstance(src_ep, int)
            and src_scene in scenes_by_episode[src_ep]
            and tgt_scene in scenes_by_episode[tgt_ep]
        )
        if not valid:
            invalid_local_edges += 1
        if isinstance(src_ep, int) and row.get("work_id") != f"{title}_{src_ep:02d}":
            episode_work_id_mismatches += 1
        if isinstance(src_ep, int) and isinstance(tgt_ep, int) and src_ep != tgt_ep:
            cross_episode_records_in_local += 1
        if src_ep == tgt_ep and isinstance(src_scene, int) and isinstance(tgt_scene, int):
            adjacent_scene_local_edges += int(tgt_scene - src_scene == 1)

    invalid_cross_edges = 0
    for row in records["cross_edges"]:
        src_ep, tgt_ep = row.get("src_episode_no"), row.get("tgt_episode_no")
        src_scene, tgt_scene = row.get("src_scene_no"), row.get("tgt_scene_no")
        valid = (
            isinstance(src_ep, int)
            and isinstance(tgt_ep, int)
            and tgt_ep > src_ep
            and row.get("gap_episodes") == tgt_ep - src_ep
            and src_scene in scenes_by_episode[src_ep]
            and tgt_scene in scenes_by_episode[tgt_ep]
        )
        if not valid:
            invalid_cross_edges += 1

    for row in records["payoff_candidates"]:
        ep = row.get("episode_no")
        if isinstance(ep, int) and row.get("work_id") != f"{title}_{ep:02d}":
            episode_work_id_mismatches += 1

    all_ids: list[str] = []
    for rows in records.values():
        for row in rows:
            for key in ("seq_id", "edge_id", "candidate_id"):
                if isinstance(row.get(key), str):
                    all_ids.append(row[key])

    full_path = root / "authored" / f"{title}_full_series_arc.json"
    full_series = load_json_file(full_path)[0] if full_path.exists() else {}
    full_values = list(full_series.values())

    support_patterns = {
        "source_lock": root.parent / "source_lock" / f"{title}_SOURCE_LOCK_V2.json",
        "strong_validation": root.parent / "validation" / f"{title}_strong_validation.json",
        "upgrade_summary": root.parent / "upgrade_audit" / title / "upgrade_summary.json",
        "candidate_disposition_ledger": root.parent / "upgrade_audit" / title / "candidate_disposition_ledger.jsonl",
        "normalization_ledger": root.parent / "upgrade_audit" / title / "stage02_normalization_ledger.json",
        "repair_ledger": root.parent / "upgrade_audit" / title / "deterministic_repair_ledger.json",
    }
    disposition_path = support_patterns["candidate_disposition_ledger"]
    dispositions = load_json_file(disposition_path) if disposition_path.exists() else []

    char_counts = Counter(row.get("character") for row in records["character_arcs"] if row.get("character"))
    relation_pairs = {
        tuple(sorted((str(row.get("char_a")), str(row.get("char_b")))))
        for row in records["relationship_arcs"]
    }

    return {
        "title": title,
        "episodes": len(episodes),
        "layers": {
            name: layer_metrics(rows, TEXT_FIELDS[name]) for name, rows in records.items()
        },
        "normalized_density": {
            "scenes_per_episode": round(len(records["scenes"]) / len(episodes), 2),
            "sequences_per_episode": round(len(records["sequences"]) / len(episodes), 2),
            "character_arcs_per_episode": round(len(records["character_arcs"]) / len(episodes), 2),
            "relationship_arcs_per_episode": round(len(records["relationship_arcs"]) / len(episodes), 2),
            "local_edges_per_episode": round(len(records["local_edges"]) / len(episodes), 2),
            "payoff_candidates_per_episode": round(len(records["payoff_candidates"]) / len(episodes), 2),
            "cross_edges_per_episode": round(len(records["cross_edges"]) / len(episodes), 2),
            "sequence_to_scene_ratio": round(len(records["sequences"]) / len(records["scenes"]), 4),
        },
        "semantic_breadth": {
            "distinct_characters": len(char_counts),
            "characters_with_multi_episode_arcs": sum(1 for count in char_counts.values() if count > 1),
            "distinct_relationship_pairs": len(relation_pairs),
        },
        "integrity": {
            "missing_sequence_scene_coverage": missing_scene_coverage,
            "overlapping_sequence_scene_memberships": overlapping_scene_memberships,
            "invalid_trigger_scene_references": invalid_trigger_refs,
            "invalid_local_edges": invalid_local_edges,
            "invalid_cross_edges": invalid_cross_edges,
            "duplicate_ids": len(all_ids) - len(set(all_ids)),
            "episode_work_id_mismatches": episode_work_id_mismatches,
        },
        "graph_shape": {
            "cross_episode_records_in_local_files": cross_episode_records_in_local,
            "adjacent_scene_local_edge_ratio": round(
                adjacent_scene_local_edges / len(records["local_edges"]), 4
            )
            if records["local_edges"]
            else 0.0,
            "candidate_disposition_records": len(dispositions),
            "candidate_disposition_counts": dict(
                Counter(row.get("disposition", "<missing>") for row in dispositions)
            ),
            "unresolved_candidate_count": max(
                0, len(records["payoff_candidates"]) - len(dispositions)
            ),
        },
        "full_series_arc": {
            "present": bool(full_series),
            "key_count": len(full_series),
            "filled_value_ratio": round(sum(is_filled(v) for v in full_values) / len(full_values), 4)
            if full_values
            else 0.0,
            "macro_turning_point_count": len(full_series.get("macro_turning_points", []))
            if isinstance(full_series.get("macro_turning_points"), list)
            else 0,
        },
        "audit_support": {name: path.exists() for name, path in support_patterns.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("titles", nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root / "seqcard_ko" if (args.root / "seqcard_ko").is_dir() else args.root
    report = {
        "scope": "metadata_and_authored_analysis_only",
        "raw_text_exported": False,
        "works": [collect_work(root, title) for title in args.titles],
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
