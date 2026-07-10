from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.corpus_formula_bridge import run_local_corpus_formula_bridge

from .contracts import FormulaSignalIndexEntry, FormulaSignalStoreSpec, WriterIdeAdvisoryCard
from .loader import (
    load_formula_signal_registry,
    query_formula_signals,
    stable_signal_checksum,
    validate_formula_signal_records,
    work_id_from_signal,
)

FORMULA_SIGNAL_STORE_MODE = "DETERMINISTIC_FORMULA_SIGNAL_STORE"


def run_formula_signal_store(
    repo_root: Path | None = None,
    bridge_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repo_root = repo_root or Path(__file__).resolve().parents[3]
    bridge_report = bridge_report or run_local_corpus_formula_bridge(repo_root=repo_root)
    output_dir = repo_root / "release/current/formula_signal_store_pack"
    output_dir.mkdir(parents=True, exist_ok=True)

    registry_path = repo_root / "release/current/corpus_formula_bridge_pack/formula_signal_registry.json"
    source_records = bridge_report.get("parts", {}).get("formula_signal_registry")
    records = [record for record in source_records if isinstance(record, dict)] if isinstance(source_records, list) else load_formula_signal_registry(registry_path)

    validation = validate_formula_signal_records(records)
    spec = _build_store_spec(repo_root)
    index = _build_signal_index(records)
    query_surface = _build_query_surface(records)
    writer_cards = _build_writer_ide_cards(records)

    parts = {
        "formula_signal_store_spec": spec,
        "formula_signal_validation_report": validation,
        "formula_signal_index": index,
        "formula_signal_query_surface": query_surface,
        "writer_ide_advisory_cards": writer_cards,
    }

    issues: list[str] = []
    if bridge_report.get("status") != "pass":
        issues.append("corpus_formula_bridge_not_pass")
    for name, payload in parts.items():
        if payload.get("status") != "pass":
            issues.append(f"{name}_blocked")
            issues.extend(f"{name}:{issue}" for issue in payload.get("issues", []))

    result = {
        "title": "Formula Signal Store",
        "status": "pass" if not issues else "blocked",
        "mode": FORMULA_SIGNAL_STORE_MODE,
        "issues": issues,
        "provider_default_calls": 0,
        "runtime_training_enabled": False,
        "node2_raw_reveal_access": 0,
        "canonical_mutation_allowed": False,
        "advisory_only": True,
        "raw_vectors_exported": False,
        "verbatim_text_exported": False,
        "paths": {
            "repo_root": str(repo_root),
            "source_registry": str(registry_path),
            "source_bridge_report": str(repo_root / "release/current/corpus_formula_bridge_pack/corpus_formula_bridge_report.json"),
        },
        "counters": {
            "signal_count": len(records),
            "group_count": len({str(record.get("formula_group", "")) for record in records}),
            "work_count": len({work_id_from_signal(record) for record in records if work_id_from_signal(record)}),
            "writer_panel_count": len({str(record.get("writer_ide_panel_ref", "")) for record in records}),
            "value_proof_ready_count": sum(
                1 for record in records if str(record.get("review_status")) == "VALID_FOR_VALUE_PROOF_PREREGISTRATION"
            ),
            "critic_ready_count": sum(
                1
                for record in records
                if str(record.get("review_status")) in {"VALID_FOR_VALUE_PROOF_PREREGISTRATION", "VALID_FOR_LEARNABLE_CRITIC_AUDIT"}
            ),
        },
        "parts": parts,
    }
    _write_outputs(output_dir, result)
    return result


def _build_store_spec(repo_root: Path) -> dict[str, Any]:
    spec = FormulaSignalStoreSpec(
        name="FormulaSignalRegistryJsonStore",
        path="release/current/corpus_formula_bridge_pack/formula_signal_registry.json",
        source_report="release/current/corpus_formula_bridge_pack/corpus_formula_bridge_report.json",
        mode="read_only_queryable",
        advisory_only=True,
        canonical_mutation_allowed=False,
    )
    return {
        "status": "pass",
        "issues": [],
        "spec": spec.to_dict(),
        "repo_root": str(repo_root),
    }


def _build_signal_index(records: list[dict[str, Any]]) -> dict[str, Any]:
    entries = [
        FormulaSignalIndexEntry(
            formula_signal_id=str(record["formula_signal_id"]),
            work_id=work_id_from_signal(record),
            formula_id=str(record["formula_id"]),
            formula_group=str(record["formula_group"]),
            output_signal_type=str(record["output_signal_type"]),
            review_status=str(record["review_status"]),
            writer_ide_panel_ref=str(record["writer_ide_panel_ref"]),
            confidence=round(float(record["confidence"]), 6),
            checksum=stable_signal_checksum(record),
        )
        for record in records
    ]
    return {
        "status": "pass" if entries else "blocked",
        "issues": [] if entries else ["signal_index_empty"],
        "entry_count": len(entries),
        "entries": [entry.to_dict() for entry in entries],
    }


def _build_query_surface(records: list[dict[str, Any]]) -> dict[str, Any]:
    work_ids = sorted({work_id_from_signal(record) for record in records if work_id_from_signal(record)})
    formula_groups = sorted({str(record.get("formula_group", "")) for record in records})
    panels = sorted({str(record.get("writer_ide_panel_ref", "")) for record in records})
    sample_work = work_ids[0] if work_ids else None
    sample_group = formula_groups[0] if formula_groups else None
    sample_panel = panels[0] if panels else None

    examples = {
        "by_work": query_formula_signals(records, work_id=sample_work)[:5] if sample_work else [],
        "by_group": query_formula_signals(records, formula_group=sample_group)[:5] if sample_group else [],
        "by_panel": query_formula_signals(records, writer_ide_panel_ref=sample_panel)[:5] if sample_panel else [],
        "high_confidence": query_formula_signals(records, min_confidence=0.75)[:5],
    }
    return {
        "status": "pass" if records else "blocked",
        "issues": [] if records else ["query_surface_empty"],
        "supported_filters": ["work_id", "formula_group", "review_status", "writer_ide_panel_ref", "min_confidence"],
        "work_ids": work_ids[:25],
        "formula_groups": formula_groups,
        "writer_panels": panels,
        "example_queries": examples,
    }


def _build_writer_ide_cards(records: list[dict[str, Any]]) -> dict[str, Any]:
    cards: list[WriterIdeAdvisoryCard] = []
    buckets: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for record in records:
        panel = str(record.get("writer_ide_panel_ref", ""))
        work_id = work_id_from_signal(record)
        if not panel or not work_id:
            continue
        buckets.setdefault((panel, work_id), []).append(record)

    for (panel, work_id), bucket in sorted(buckets.items()):
        bucket = sorted(bucket, key=lambda item: float(item.get("confidence") or 0.0), reverse=True)
        top_records = bucket[:3]
        headline = _headline_for(panel, work_id)
        summary = " | ".join(str(record.get("output_signal_value_or_label", "")) for record in top_records)
        severity = "review" if any("WARNING" in str(record.get("output_signal_type", "")) for record in top_records) else "advisory"
        cards.append(
            WriterIdeAdvisoryCard(
                card_id=f"writer-card:{panel}:{work_id}",
                panel_ref=panel,
                work_id=work_id,
                headline=headline,
                summary=summary,
                severity=severity,
                signal_refs=tuple(str(record["formula_signal_id"]) for record in top_records),
                badges=tuple(sorted({str(record.get("formula_group", "")) for record in top_records})),
                advisory_only=True,
                canonical_mutation_allowed=False,
            )
        )
    return {
        "status": "pass" if cards else "blocked",
        "issues": [] if cards else ["writer_ide_cards_empty"],
        "card_count": len(cards),
        "cards": [card.to_dict() for card in cards],
    }


def _headline_for(panel: str, work_id: str) -> str:
    if "narrative_state_tensor" in panel:
        return f"{work_id} narrative tensor advisory"
    if "emotional_momentum" in panel:
        return f"{work_id} emotional momentum advisory"
    if "corpus_reference" in panel:
        return f"{work_id} corpus grounding advisory"
    return f"{work_id} formula signal advisory"


def _write_outputs(output_dir: Path, payload: dict[str, Any]) -> None:
    parts = payload["parts"]
    _write_json(output_dir / "formula_signal_store_spec.json", parts["formula_signal_store_spec"])
    _write_json(output_dir / "formula_signal_validation_report.json", parts["formula_signal_validation_report"])
    _write_json(output_dir / "formula_signal_index.json", parts["formula_signal_index"])
    _write_json(output_dir / "formula_signal_query_surface.json", parts["formula_signal_query_surface"])
    _write_json(output_dir / "writer_ide_advisory_cards.json", parts["writer_ide_advisory_cards"])
    _write_json(output_dir / "formula_signal_store_report.json", payload)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
