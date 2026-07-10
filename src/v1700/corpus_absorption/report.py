from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .contracts import CanonicalWorkRecord, CorpusAbsorptionReport, LearningSignalRecord, RagIndexRecord, SourceAssetRecord

ABSORPTION_MODE = "LOCAL_METADATA_ONLY_CORPUS_ABSORPTION"
DEFAULT_CORPUS_ROOT = Path(r"C:\AI_Codex\codex-work\gpt\db\corpus_ko")
DEFAULT_PACK_DIR = Path("release/current/corpus_ko_absorption_pack")
SAFE_SUMMARY_FILES = (
    "local_db_inventory_summary.json",
    "local_db_file_inventory.csv",
    "local_sqlite_schema_summary.json",
    "local_db_survey_report.md",
)
FEATURE_KEYS = (
    "conflict_intensity",
    "scene_energy_ratio",
    "motif_residue_score",
    "curiosity_gradient",
    "dialogue_ratio",
)


def run_local_corpus_absorption(
    repo_root: Path | None = None,
    corpus_root: Path | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    repo_root = repo_root or Path(__file__).resolve().parents[3]
    corpus_root = corpus_root or DEFAULT_CORPUS_ROOT
    output_dir = output_dir or repo_root / DEFAULT_PACK_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    issues: list[str] = []
    notes: list[str] = [
        "metadata_only_absorption",
        "verbatim_text_not_exported",
        "raw_vectors_not_exported",
        "canonical_store_is_authority_rag_is_index",
    ]

    if not corpus_root.exists():
        issues.append(f"missing_corpus_root:{corpus_root}")
        report = CorpusAbsorptionReport(
            corpus_id="corpus_ko",
            status="blocked",
            source_asset_records=(),
            canonical_work_records=(),
            rag_index_records=(),
            learning_signal_records=(),
            issues=tuple(issues),
            counters={"source_asset_count": 0, "work_count": 0, "rag_ready_count": 0, "learning_ready_count": 0},
            notes=tuple(notes),
        )
        payload = _build_result_payload(report, repo_root, corpus_root, output_dir)
        _write_outputs(repo_root, output_dir, payload)
        return payload

    manifest = _read_json_if_exists(corpus_root / "manifest.json")
    nkg_summary = _read_json_if_exists(corpus_root / "nkg_summary.json")
    sources = _read_json_if_exists(corpus_root / "sources.json") or []
    qc_items = _read_json_if_exists(corpus_root / "qc_report.json") or []

    source_asset_records = _build_source_asset_records(corpus_root)
    work_source_map = _build_source_lookup(sources)
    qc_map = _build_qc_lookup(qc_items)
    scene_stats, method_totals = _scan_scene_records(corpus_root / "scenes")
    chunk_counts = _scan_chunk_records(corpus_root / "chunks")
    feature_stats, feature_totals = _scan_feature_records(corpus_root / "features")
    txt_presence = {
        path.stem
        for path in (corpus_root / "txt").glob("*.txt")
        if path.is_file() and not _is_ignored_work_id(path.stem)
    }
    work_ids = sorted(
        set(work_source_map)
        | set(scene_stats)
        | set(chunk_counts)
        | set(feature_stats)
        | set(txt_presence)
    )

    canonical_work_records: list[CanonicalWorkRecord] = []
    rag_index_records: list[RagIndexRecord] = []
    learning_signal_records: list[LearningSignalRecord] = []

    embedding_cache_available = any((corpus_root / "emb_cache").glob("*"))
    vector_store_kind = "ChromaDB"
    retrieval_policy = "metadata_authority_plus_external_vector_index"
    text_policy = "verbatim_forbidden_in_repo_outputs"

    for work_id in work_ids:
        source = work_source_map.get(work_id, {})
        scene_info = scene_stats.get(work_id, {"scene_count": 0, "parse_methods": {}})
        feature_info = feature_stats.get(work_id, {"count": 0, "means": {}})
        qc_flags = tuple(qc_map.get(work_id, ("UNKNOWN",)))
        scene_count = int(scene_info["scene_count"])
        chunk_count = int(chunk_counts.get(work_id, 0))
        feature_scene_count = int(feature_info["count"])
        has_txt = work_id in txt_presence
        has_scenes = scene_count > 0
        has_chunks = chunk_count > 0
        has_features = feature_scene_count > 0
        processing_status = "ready_for_canonical_store" if has_scenes and has_features else "partial_ingestion"

        canonical_work_records.append(
            CanonicalWorkRecord(
                work_id=work_id,
                work_title=work_id,
                source_media=str(source.get("media", "unknown")),
                source_type=str(source.get("type", "unknown")),
                source_reference=str(source.get("src", "")),
                has_txt=has_txt,
                has_scenes=has_scenes,
                has_chunks=has_chunks,
                has_features=has_features,
                scene_count=scene_count,
                chunk_count=chunk_count,
                feature_scene_count=feature_scene_count,
                parse_methods=dict(scene_info["parse_methods"]),
                qc_flags=qc_flags,
                rights_status="user_provided_structured_analysis_db",
                access_policy="metadata_only",
                processing_status=processing_status,
            )
        )
        rag_index_records.append(
            RagIndexRecord(
                work_id=work_id,
                scene_count=scene_count,
                chunk_count=chunk_count,
                scene_index_ready=has_scenes,
                chunk_index_ready=has_chunks,
                vector_store_kind=vector_store_kind,
                vector_binding_mode="shared_corpus_index",
                embedding_cache_available=embedding_cache_available,
                retrieval_policy=retrieval_policy,
                text_policy=text_policy,
            )
        )
        means = feature_info["means"]
        learning_signal_records.append(
            LearningSignalRecord(
                work_id=work_id,
                feature_scene_count=feature_scene_count,
                mean_conflict_intensity=_safe_round(means.get("conflict_intensity")),
                mean_scene_energy_ratio=_safe_round(means.get("scene_energy_ratio")),
                mean_motif_residue_score=_safe_round(means.get("motif_residue_score")),
                mean_curiosity_gradient=_safe_round(means.get("curiosity_gradient")),
                mean_dialogue_ratio=_safe_round(means.get("dialogue_ratio")),
                signal_keys=FEATURE_KEYS,
                learning_ready=feature_scene_count > 0,
            )
        )

    if not canonical_work_records:
        issues.append("no_canonical_work_records")
    if not any(record.learning_ready for record in learning_signal_records):
        issues.append("no_learning_ready_records")
    if not any(record.scene_index_ready for record in rag_index_records):
        issues.append("no_rag_ready_records")

    if manifest and manifest.get("counts", {}).get("converted_works") and manifest["counts"]["converted_works"] != len(work_ids):
        notes.append("manifest_converted_work_count_differs_from_detected_work_ids")
    if manifest and manifest.get("counts", {}).get("source_files") and manifest["counts"]["source_files"] != len(sources):
        notes.append("manifest_source_file_count_differs_from_sources_json")
    if manifest and manifest.get("tri_store", {}).get("feature_table") and not (corpus_root / "scene_features.db").stat().st_size:
        notes.append("scene_features_db_is_empty_use_json_feature_records_as_authority")
    if method_totals:
        notes.append(f"parse_methods_detected:{','.join(sorted(method_totals))}")
    if feature_totals:
        notes.append(f"feature_keys_detected:{','.join(sorted(feature_totals))}")

    counters = {
        "source_asset_count": len(source_asset_records),
        "work_count": len(canonical_work_records),
        "rag_ready_count": sum(1 for record in rag_index_records if record.scene_index_ready and record.chunk_index_ready),
        "learning_ready_count": sum(1 for record in learning_signal_records if record.learning_ready),
        "source_json_count": len(sources),
        "scene_record_work_count": len(scene_stats),
        "feature_record_work_count": len(feature_stats),
    }
    report = CorpusAbsorptionReport(
        corpus_id="corpus_ko",
        status="pass" if not issues else "blocked",
        source_asset_records=tuple(source_asset_records),
        canonical_work_records=tuple(canonical_work_records),
        rag_index_records=tuple(rag_index_records),
        learning_signal_records=tuple(learning_signal_records),
        issues=tuple(issues),
        counters=counters,
        notes=tuple(notes),
    )
    payload = _build_result_payload(report, repo_root, corpus_root, output_dir, manifest=manifest, nkg_summary=nkg_summary)
    _write_outputs(repo_root, output_dir, payload)
    return payload


def _build_result_payload(
    report: CorpusAbsorptionReport,
    repo_root: Path,
    corpus_root: Path,
    output_dir: Path,
    *,
    manifest: dict[str, Any] | None = None,
    nkg_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = report.to_dict()
    work_records = data["canonical_work_records"]
    rag_records = data["rag_index_records"]
    learning_records = data["learning_signal_records"]

    return {
        "corpus_id": report.corpus_id,
        "title": "Local Corpus Metadata Absorption",
        "status": report.status,
        "mode": ABSORPTION_MODE,
        "issues": list(report.issues),
        "notes": list(report.notes),
        "counters": report.counters,
        "runtime_training_enabled": False,
        "active_meta_learning_enabled": False,
        "provider_default_calls": 0,
        "node2_raw_reveal_access": 0,
        "verbatim_text_exported": False,
        "raw_vectors_exported": False,
        "paths": {
            "repo_root": str(repo_root),
            "corpus_root": str(corpus_root),
            "output_dir": str(output_dir),
        },
        "parts": {
            "source_asset_inventory": data["source_asset_records"],
            "canonical_work_registry": work_records,
            "rag_index_registry": rag_records,
            "learning_signal_registry": learning_records,
            "audit_summary": {
                "manifest_counts": (manifest or {}).get("counts", {}),
                "nkg_summary": nkg_summary or {},
                "empty_feature_db": any(
                    record["relative_path"].endswith("scene_features.db") and record["size_bytes"] == 0
                    for record in data["source_asset_records"]
                ),
                "rag_ready_work_count": sum(
                    1 for record in rag_records if record["scene_index_ready"] and record["chunk_index_ready"]
                ),
                "learning_ready_work_count": sum(1 for record in learning_records if record["learning_ready"]),
            },
        },
    }


def _build_source_asset_records(corpus_root: Path) -> list[SourceAssetRecord]:
    candidates = [
        corpus_root / "manifest.json",
        corpus_root / "sources.json",
        corpus_root / "qc_report.json",
        corpus_root / "parse_stats.json",
        corpus_root / "nkg_summary.json",
        corpus_root / "nkg.json",
        corpus_root / "chroma_export.tar.gz",
        corpus_root / "chroma" / "chroma.sqlite3",
        corpus_root / "scene_features.db",
    ]
    records: list[SourceAssetRecord] = []
    for path in candidates:
        if not path.exists() or not path.is_file():
            continue
        rel = path.relative_to(corpus_root).as_posix()
        records.append(
            SourceAssetRecord(
                asset_id=_stable_asset_id(rel),
                relative_path=rel,
                asset_kind=_asset_kind_for_path(path),
                extension=path.suffix.lower() or "[no_ext]",
                size_bytes=path.stat().st_size,
                sha256=_sha256(path),
                rights_status="user_provided_structured_analysis_db",
                access_policy="metadata_only",
            )
        )
    return records


def _asset_kind_for_path(path: Path) -> str:
    rel = path.as_posix().lower()
    if rel.endswith("manifest.json"):
        return "manifest"
    if rel.endswith("sources.json"):
        return "source_registry"
    if rel.endswith("qc_report.json"):
        return "quality_control_report"
    if rel.endswith("parse_stats.json"):
        return "parse_statistics"
    if rel.endswith("nkg.json") or rel.endswith("nkg_summary.json"):
        return "graph_summary"
    if rel.endswith("chroma_export.tar.gz"):
        return "vector_export_archive"
    if rel.endswith("chroma.sqlite3"):
        return "vector_store_sqlite"
    if rel.endswith("scene_features.db"):
        return "feature_store_sqlite"
    return "metadata_asset"


def _build_source_lookup(sources: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(sources, list):
        return {}
    lookup: dict[str, dict[str, Any]] = {}
    for item in sources:
        if not isinstance(item, dict):
            continue
        work_id = str(item.get("id", "")).strip()
        if not work_id:
            continue
        if _is_ignored_work_id(work_id):
            continue
        lookup[work_id] = item
    return lookup


def _build_qc_lookup(qc_items: Any) -> dict[str, tuple[str, ...]]:
    if not isinstance(qc_items, list):
        return {}
    lookup: dict[str, tuple[str, ...]] = {}
    for item in qc_items:
        if not isinstance(item, dict):
            continue
        work_id = str(item.get("work", "")).strip()
        flags = str(item.get("flags", "")).strip()
        if work_id:
            if _is_ignored_work_id(work_id):
                continue
            lookup[work_id] = tuple(flag.strip() for flag in flags.split("/") if flag.strip()) or ("UNKNOWN",)
    return lookup


def _scan_scene_records(scenes_root: Path) -> tuple[dict[str, dict[str, Any]], set[str]]:
    stats: dict[str, dict[str, Any]] = {}
    method_totals: set[str] = set()
    if not scenes_root.exists():
        return stats, method_totals
    for path in sorted(scenes_root.glob("*.jsonl")):
        work_id = path.stem
        if _is_ignored_work_id(work_id):
            continue
        count = 0
        methods: Counter[str] = Counter()
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                count += 1
                method = str(payload.get("method", "unknown"))
                methods[method] += 1
                method_totals.add(method)
        stats[work_id] = {"scene_count": count, "parse_methods": dict(methods)}
    return stats, method_totals


def _scan_chunk_records(chunks_root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not chunks_root.exists():
        return counts
    for path in sorted(chunks_root.glob("*.jsonl")):
        count = 0
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    count += 1
        if _is_ignored_work_id(path.stem):
            continue
        counts[path.stem] = count
    return counts


def _scan_feature_records(features_root: Path) -> tuple[dict[str, dict[str, Any]], set[str]]:
    stats: dict[str, dict[str, Any]] = {}
    feature_totals: set[str] = set()
    if not features_root.exists():
        return stats, feature_totals
    for path in sorted(features_root.glob("*.json")):
        work_id = path.stem
        if _is_ignored_work_id(work_id):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            continue
        aggregates: defaultdict[str, float] = defaultdict(float)
        count = 0
        for item in payload:
            if not isinstance(item, dict):
                continue
            count += 1
            for key in FEATURE_KEYS:
                value = item.get(key)
                if isinstance(value, (int, float)):
                    aggregates[key] += float(value)
                    feature_totals.add(key)
        means = {key: (aggregates[key] / count if count else None) for key in FEATURE_KEYS}
        stats[work_id] = {"count": count, "means": means}
    return stats, feature_totals


def _read_json_if_exists(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_round(value: float | None) -> float | None:
    return round(value, 6) if isinstance(value, float) else None


def _is_ignored_work_id(work_id: str) -> bool:
    return work_id.startswith(".~lock.") or work_id.startswith("~$") or work_id.endswith("#")


def _stable_asset_id(relative_path: str) -> str:
    digest = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:12]
    return f"asset:{digest}"


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _write_outputs(repo_root: Path, output_dir: Path, payload: dict[str, Any]) -> None:
    parts = payload["parts"]
    _write_json(output_dir / "source_asset_inventory.json", {"source_asset_inventory": parts["source_asset_inventory"]})
    _write_json(output_dir / "canonical_work_registry.json", {"canonical_work_registry": parts["canonical_work_registry"]})
    _write_json(output_dir / "rag_index_registry.json", {"rag_index_registry": parts["rag_index_registry"]})
    _write_json(output_dir / "learning_signal_registry.json", {"learning_signal_registry": parts["learning_signal_registry"]})
    _write_json(output_dir / "audit_summary.json", parts["audit_summary"])
    _write_json(output_dir / "corpus_absorption_report.json", payload)

    fixtures_root = repo_root / "fixtures"
    _write_json(
        fixtures_root / "research" / "drama_script_metadata_inventory_summary.json",
        {
            "corpus_id": payload["corpus_id"],
            "work_count": payload["counters"]["work_count"],
            "source_json_count": payload["counters"]["source_json_count"],
            "scene_record_work_count": payload["counters"]["scene_record_work_count"],
            "feature_record_work_count": payload["counters"]["feature_record_work_count"],
            "status": payload["status"],
            "mode": payload["mode"],
        },
    )
    _write_json(fixtures_root / "research" / "chromadb_featuredb_audit_summary.json", parts["audit_summary"])
    learning_registry = parts["learning_signal_registry"]
    sample_record = learning_registry[0] if learning_registry else {}
    _write_json(fixtures_root / "research" / "script_feature_record_sample.json", sample_record)
    minimum_record_payload = {
        "source_asset_inventory": parts["source_asset_inventory"][:2],
        "canonical_work_registry": parts["canonical_work_registry"][:2],
        "rag_index_registry": parts["rag_index_registry"][:2],
        "learning_signal_registry": parts["learning_signal_registry"][:2],
    }
    _write_json(fixtures_root / "canonical_record_store" / "minimum_records.json", minimum_record_payload)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
