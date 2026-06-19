from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS_ROOT = Path(r"C:\AI_Codex\codex-work\gpt\db\corpus_ko")


def main() -> None:
    corpus_root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CORPUS_ROOT
    report = build_local_corpus_db_survey(corpus_root)

    output_path = ROOT / "release/current/local_corpus_db_survey_report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    markdown_path = ROOT / "docs/development/local_corpus_db_latest_survey_report.md"
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(_to_markdown(report), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))


def build_local_corpus_db_survey(corpus_root: Path) -> dict[str, Any]:
    files = [path for path in corpus_root.rglob("*") if path.is_file()] if corpus_root.exists() else []
    by_extension = Counter(path.suffix.lower() or "[none]" for path in files)
    by_top_dir = Counter(_top_dir(corpus_root, path) for path in files)
    newest_files = sorted(files, key=lambda path: path.stat().st_mtime, reverse=True)[:40]
    scene_summary = _jsonl_summary(corpus_root / "scenes")
    chunk_summary = _jsonl_summary(corpus_root / "chunks")
    feature_summary = _json_summary(corpus_root / "features")

    issues = []
    if not corpus_root.exists():
        issues.append("missing_corpus_root")
    if scene_summary["bad_files"]:
        issues.append("scene_jsonl_parse_errors")
    if chunk_summary["bad_files"]:
        issues.append("chunk_jsonl_parse_errors")
    if feature_summary["bad_files"]:
        issues.append("feature_json_parse_errors")

    return {
        "title": "Local Corpus DB Latest Survey",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "corpus_root": str(corpus_root),
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "safety": {
            "raw_text_exported": False,
            "raw_vectors_exported": False,
            "provider_default_calls": 0,
            "runtime_training_enabled": False,
            "access_policy": "metadata_only",
            "rights_status": "user_provided_structured_analysis_db",
        },
        "inventory": {
            "file_count": len(files),
            "total_bytes": sum(path.stat().st_size for path in files),
            "by_extension": dict(by_extension.most_common()),
            "by_top_dir": dict(by_top_dir.most_common()),
        },
        "latest_files": [
            {
                "relative_path": path.relative_to(corpus_root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
            for path in newest_files
        ],
        "scene_jsonl_summary": scene_summary,
        "chunk_jsonl_summary": chunk_summary,
        "feature_json_summary": feature_summary,
        "source_assets": _source_asset_refs(corpus_root),
    }


def _jsonl_summary(root: Path) -> dict[str, Any]:
    if not root.exists():
        return {"dir": str(root), "file_count": 0, "record_count": 0, "observed_keys": [], "bad_files": []}
    files = sorted(root.glob("*.jsonl"))
    keys: set[str] = set()
    record_count = 0
    bad_files: list[dict[str, str]] = []
    for path in files:
        try:
            with path.open("r", encoding="utf-8-sig") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    record_count += 1
                    if len(keys) < 64:
                        payload = json.loads(line)
                        if isinstance(payload, dict):
                            keys.update(str(key) for key in payload.keys())
        except Exception as exc:  # noqa: BLE001
            bad_files.append({"relative_path": path.name, "error": str(exc)})
    return {
        "dir": str(root),
        "file_count": len(files),
        "record_count": record_count,
        "observed_keys": sorted(keys),
        "bad_files": bad_files,
    }


def _json_summary(root: Path) -> dict[str, Any]:
    if not root.exists():
        return {"dir": str(root), "file_count": 0, "record_count": 0, "bad_files": []}
    files = sorted(root.glob("*.json"))
    record_count = 0
    bad_files: list[dict[str, str]] = []
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
            if isinstance(payload, list):
                record_count += len(payload)
            elif isinstance(payload, dict):
                record_count += 1
        except Exception as exc:  # noqa: BLE001
            bad_files.append({"relative_path": path.name, "error": str(exc)})
    return {"dir": str(root), "file_count": len(files), "record_count": record_count, "bad_files": bad_files}


def _source_asset_refs(corpus_root: Path) -> list[dict[str, Any]]:
    candidates = [
        "manifest.json",
        "sources.json",
        "qc_report.json",
        "parse_stats.json",
        "nkg_summary.json",
        "nkg.json",
        "chroma/chroma.sqlite3",
        ".chroma/chroma.sqlite3",
        "scene_features.db",
    ]
    refs = []
    for rel in candidates:
        path = corpus_root / rel
        if not path.exists() or not path.is_file():
            continue
        refs.append({"relative_path": rel, "size_bytes": path.stat().st_size, "sha256": _sha256(path)})
    return refs


def _top_dir(root: Path, path: Path) -> str:
    rel = path.relative_to(root)
    return rel.parts[0] if rel.parts else "."


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _to_markdown(report: dict[str, Any]) -> str:
    inventory = report["inventory"]
    scene = report["scene_jsonl_summary"]
    chunk = report["chunk_jsonl_summary"]
    feature = report["feature_json_summary"]
    return (
        "# Local Corpus DB Latest Survey Report\n\n"
        f"Created: {report['created_at']}\n"
        f"Corpus root: `{report['corpus_root']}`\n"
        f"Status: `{report['status']}`\n\n"
        "## Safety\n\n"
        "- Raw text exported: `false`\n"
        "- Raw vectors exported: `false`\n"
        "- Provider calls: `0`\n"
        "- Runtime training: `false`\n"
        "- Access policy: `metadata_only`\n\n"
        "## Inventory\n\n"
        f"- File count: `{inventory['file_count']}`\n"
        f"- Total bytes: `{inventory['total_bytes']}`\n"
        f"- Scene JSONL files: `{scene['file_count']}`\n"
        f"- Scene records: `{scene['record_count']}`\n"
        f"- Chunk JSONL files: `{chunk['file_count']}`\n"
        f"- Chunk records: `{chunk['record_count']}`\n"
        f"- Feature JSON files: `{feature['file_count']}`\n"
        f"- Feature records: `{feature['record_count']}`\n\n"
        "## Boundary\n\n"
        "This report intentionally records only aggregate counts, paths, hashes, and schema keys. "
        "It does not export raw script text or vector payloads into the repository.\n"
    )


if __name__ == "__main__":
    main()
