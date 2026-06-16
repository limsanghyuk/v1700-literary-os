#!/usr/bin/env python3
"""Metadata-only local DB inventory tool.

Run locally against a developer-provided workspace path. The tool avoids exporting
full source text, drama scripts, dialogue, or raw vectors. It records file
metadata, hashes, and SQLite schema/row counts when readable.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Sequence

DB_EXTENSIONS = {".db", ".sqlite", ".sqlite3", ".duckdb"}
TEXT_RISK_EXTENSIONS = {".txt", ".hwp", ".hwpx", ".pdf", ".doc", ".docx"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_sqlite_candidate(path: Path) -> bool:
    name = path.name.lower()
    return path.suffix.lower() in DB_EXTENSIONS or name == "chroma.sqlite3"


def scan_sqlite(path: Path) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "path": str(path),
        "status": "UNKNOWN",
        "tables": [],
        "error": None,
    }
    try:
        uri = f"file:{path.as_posix()}?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        table_names = [row[0] for row in cur.fetchall()]
        tables = []
        for table in table_names:
            columns = []
            row_count = None
            try:
                cur.execute(f"PRAGMA table_info({table})")
                columns = [row[1] for row in cur.fetchall()]
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = int(cur.fetchone()[0])
            except Exception as exc:  # pragma: no cover - local corrupt DB handling
                columns = []
                row_count = None
                tables.append({"table": table, "status": "PARTIAL", "columns": columns, "row_count": row_count, "error": str(exc)})
                continue
            tables.append({"table": table, "status": "READABLE", "columns": columns, "row_count": row_count})
        conn.close()
        result["status"] = "READABLE"
        result["tables"] = tables
    except Exception as exc:
        result["status"] = "UNREADABLE"
        result["error"] = str(exc)
    return result


def build_inventory(root: Path) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = []
    sqlite_summaries: List[Dict[str, Any]] = []
    extension_counts: Dict[str, int] = {}
    db_count = 0
    text_risk_count = 0

    for current_root, _dirs, files in os.walk(root):
        for filename in files:
            path = Path(current_root) / filename
            rel = path.relative_to(root)
            suffix = path.suffix.lower() or "<none>"
            extension_counts[suffix] = extension_counts.get(suffix, 0) + 1
            try:
                stat = path.stat()
                file_hash = sha256_file(path)
            except Exception as exc:
                records.append({
                    "relative_path": str(rel),
                    "extension": suffix,
                    "size_bytes": None,
                    "sha256": None,
                    "risk_class": "UNREADABLE",
                    "error": str(exc),
                })
                continue
            risk = "METADATA_ONLY_SAFE"
            if suffix in TEXT_RISK_EXTENSIONS:
                risk = "TEXT_SOURCE_DO_NOT_EXPORT_CONTENT"
                text_risk_count += 1
            if is_sqlite_candidate(path):
                risk = "LOCAL_DB_SCHEMA_ONLY"
                db_count += 1
                sqlite_summaries.append(scan_sqlite(path))
            records.append({
                "relative_path": str(rel),
                "extension": suffix,
                "size_bytes": stat.st_size,
                "sha256": file_hash,
                "risk_class": risk,
                "error": None,
            })

    return {
        "survey_id": f"local_db_inventory_{utc_now()}",
        "root_name": root.name,
        "generated_at": utc_now(),
        "file_count": len(records),
        "db_candidate_count": db_count,
        "text_risk_file_count": text_risk_count,
        "extension_counts": dict(sorted(extension_counts.items())),
        "records": records,
        "sqlite_summaries": sqlite_summaries,
    }


def write_outputs(inventory: Dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = {key: value for key, value in inventory.items() if key not in {"records", "sqlite_summaries"}}
    (out_dir / "local_db_inventory_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "local_sqlite_schema_summary.json").write_text(json.dumps(inventory["sqlite_summaries"], ensure_ascii=False, indent=2), encoding="utf-8")
    with (out_dir / "local_db_file_inventory.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["relative_path", "extension", "size_bytes", "sha256", "risk_class", "error"])
        writer.writeheader()
        writer.writerows(inventory["records"])
    report = [
        "# Local DB Survey Report",
        "",
        f"Generated: {inventory['generated_at']}",
        f"Root name: {inventory['root_name']}",
        f"File count: {inventory['file_count']}",
        f"DB candidate count: {inventory['db_candidate_count']}",
        f"Text risk file count: {inventory['text_risk_file_count']}",
        "",
        "## Boundary",
        "",
        "This report is metadata-only. It does not export source text, dialogue, scripts, or raw vectors.",
    ]
    (out_dir / "local_db_survey_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create metadata-only local DB inventory outputs.")
    parser.add_argument("--root", required=True, help="Local workspace path to inspect")
    parser.add_argument("--out", default=".local_db_survey", help="Output directory")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"root is not a readable directory: {root}")
    inventory = build_inventory(root)
    write_outputs(inventory, Path(args.out).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
