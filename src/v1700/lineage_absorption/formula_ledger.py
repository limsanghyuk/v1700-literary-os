from __future__ import annotations

from typing import Any

from v1700.stage121.fixtures import FORMULA_LEDGER


def build_formula_ledger() -> dict[str, Any]:
    entries = [entry.to_dict() for entry in FORMULA_LEDGER]
    by_status: dict[str, int] = {}
    for entry in entries:
        by_status[entry["absorption_status"]] = by_status.get(entry["absorption_status"], 0) + 1
    return {
        "status": "pass",
        "entry_count": len(entries),
        "entries": entries,
        "by_absorption_status": by_status,
        "formula_sources": sorted({entry["source_lineage"] for entry in entries}),
        "stage120_formulas_preserved": all(
            entry["absorption_status"] == "KEEP"
            for entry in entries
            if entry["source_lineage"] == "stage120_trunk"
        ),
    }
