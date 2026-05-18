from __future__ import annotations

from pathlib import Path


def probe_v430_sources(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    workspace_root = root.parents[2] if len(root.parents) > 2 else root
    search_roots = [
        workspace_root / "claude",
        workspace_root / "gpt" / "packages",
        workspace_root / "gpt" / "analysis",
        root / "docs",
    ]
    hits: list[str] = []
    for base in search_roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            rel = _safe_rel(path, root)
            lowered = rel.lower()
            if _ignored(lowered):
                continue
            if "v430" in lowered or "stage430" in lowered:
                hits.append(rel)
    unique_hits = sorted(set(hits))
    source_status = "AVAILABLE" if unique_hits else "MISSING"
    return {
        "status": "pass",
        "source_status": source_status,
        "source_available": bool(unique_hits),
        "source_paths": unique_hits[:50],
        "absorption_mode": "gitnexus_impact_then_contract_adapter" if unique_hits else "fixture_contract_validation",
        "v430_untraced_merge": False,
    }


def _safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _ignored(lowered: str) -> bool:
    ignored = (
        ".git/",
        ".gitnexus/",
        ".venv/",
        "__pycache__",
        ".pytest_cache",
        "release/current/",
        "release/history/",
        "packages/",
        "work/_latest_stage99_preflight/",
        "work/_stage100",
        "stage101_cross_lineage_pack",
        "release/current/stage100_v430",
        "src/v1700/stage100/v430",
        "src/v1700/cross_lineage/v430_candidate_probe.py",
        "tests/test_stage100_v430_comparison_bridge.py",
        "manifests/stage100_v430_comparison_manifest.json",
        "docs/stage101_cross_lineage_absorption_scenario_room",
    )
    return any(token in lowered for token in ignored)
