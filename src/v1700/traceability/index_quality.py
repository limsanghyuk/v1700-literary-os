from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from v1700.sidecars.gitnexus.probe import probe_gitnexus
from v1700.traceability.contracts import IndexQualityMetrics, IndexQualityThresholds
from v1700.traceability.symbol_trace import build_symbol_to_branchpoint_trace_manifest


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def load_gitnexus_meta(root: Path) -> tuple[str, dict[str, Any] | None]:
    live_meta = _read_json(root / ".gitnexus" / "meta.json")
    if live_meta:
        return "live_gitnexus_meta", live_meta
    snapshot_names = (
        "stage100_gitnexus_meta_snapshot.json",
        "stage97_1_gitnexus_meta_snapshot.json",
        "stage94_gitnexus_meta_snapshot.json",
        "stage86_gitnexus_meta_snapshot.json",
        "stage85_gitnexus_meta_snapshot.json",
    )
    for snapshot_name in snapshot_names:
        snapshot = _read_json(root / "release" / "current" / snapshot_name)
        if snapshot:
            return f"{Path(snapshot_name).stem}_release_snapshot", snapshot
    return "missing", None


def _metrics_from_meta(meta: dict[str, Any] | None) -> IndexQualityMetrics:
    stats = (meta or {}).get("stats", {})
    return IndexQualityMetrics(
        files=int(stats.get("files", 0) or 0),
        nodes=int(stats.get("nodes", 0) or stats.get("symbols", 0) or 0),
        edges=int(stats.get("edges", 0) or 0),
        clusters=int(stats.get("clusters", 0) or stats.get("communities", 0) or 0),
        flows=int(stats.get("flows", 0) or stats.get("processes", 0) or 0),
        embeddings=int(stats.get("embeddings", 0) or 0),
    )


def _load_live_manifest(root: Path) -> dict[str, Any]:
    return _read_json(root / "manifests" / "live_core_manifest.json") or {}


def build_gitnexus_index_quality_report(
    root: Path | None = None,
    thresholds: IndexQualityThresholds | None = None,
) -> dict[str, Any]:
    root = root or _project_root()
    thresholds = thresholds or IndexQualityThresholds()
    meta_source, meta = load_gitnexus_meta(root)
    metrics = _metrics_from_meta(meta)
    trace = build_symbol_to_branchpoint_trace_manifest(root)
    live_manifest = _load_live_manifest(root)
    invariants = live_manifest.get("core_invariants", {})
    probe = probe_gitnexus().to_dict()

    p0_coverage = trace["coverage"]["P0"]["coverage"]
    p1_coverage = trace["coverage"]["P1"]["coverage"]
    checks = {
        "meta_available": meta is not None,
        "files_threshold": metrics.files >= thresholds.min_files,
        "nodes_threshold": metrics.nodes >= thresholds.min_nodes,
        "edges_threshold": metrics.edges >= thresholds.min_edges,
        "clusters_threshold": metrics.clusters >= thresholds.min_clusters,
        "flows_threshold": metrics.flows >= thresholds.min_flows,
        "p0_trace_coverage": p0_coverage >= thresholds.min_p0_coverage,
        "p1_trace_coverage": p1_coverage >= thresholds.min_p1_coverage,
        "gitnexus_optional_sidecar_preserved": invariants.get("gitnexus_optional_only") is True,
        "python_fallback_preserved": invariants.get("python_fallback_available") is True,
        "graphnexus_authority_preserved": invariants.get("graph_nexus_operational_tools") is True,
    }
    issues = [name for name, passed in checks.items() if not passed]
    return {
        "stage": "85",
        "status": "pass" if not issues else "blocked",
        "title": "GitNexus Index Quality Gate",
        "principle": "Use GitNexus as optional high-resolution code impact evidence while preserving GraphNexus authority and Python fallback.",
        "issues": issues,
        "meta_source": meta_source,
        "gitnexus": probe,
        "metrics": metrics.to_dict(),
        "thresholds": thresholds.to_dict(),
        "checks": checks,
        "symbol_to_branchpoint_trace": {
            "status": trace["status"],
            "entry_count": trace["entry_count"],
            "coverage": trace["coverage"],
        },
        "claude_v381_reference": {
            "files": 332,
            "nodes": 10443,
            "edges": 21487,
            "clusters": 361,
            "flows": 140,
        },
        "interpretation": "Stage84 already has comparable flow breadth; Stage85 requires traceable symbol and branchpoint density rather than mandatory GitNexus runtime dependency.",
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }


def export_gitnexus_index_quality_report(root: Path | None = None) -> dict[str, str]:
    root = root or _project_root()
    report = build_gitnexus_index_quality_report(root)
    release_dir = root / "release" / "current"
    release_dir.mkdir(parents=True, exist_ok=True)
    report_path = release_dir / "stage85_gitnexus_index_quality_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"stage85_gitnexus_index_quality_report": str(report_path.relative_to(root))}
