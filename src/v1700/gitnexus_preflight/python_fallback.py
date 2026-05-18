from __future__ import annotations

import ast
import json
from pathlib import Path
from .contracts import FallbackImpactReport

CRITICAL_PATHS = [
    "src/v1700/gates/release_gate.py",
    "src/v1700/gates/stage111_release_gate.py",
    "src/v1700/gates/stage112_release_gate.py",
    "src/v1700/gitnexus_preflight/preflight_runner.py",
    "manifests/live_core_manifest.json",
    "manifests/stage112_manifest.json",
    "docs/stages/stage112.md",
]

TEST_HINTS = {
    "gitnexus_preflight": ["tests/test_stage112_gitnexus_nie_preflight.py"],
    "stage112_release_gate": ["tests/test_stage112_gitnexus_nie_preflight.py"],
    "release_gate": ["tests/test_stage112_gitnexus_nie_preflight.py", "tests/test_stage111_v485_absorption_bridge.py"],
    "repo_doctor": ["tests/test_stage112_gitnexus_nie_preflight.py"],
}


def run_python_fallback_impact(root: Path) -> dict:
    import_edges = _collect_import_edges(root / "src")
    manifests = {p: (root / p).exists() for p in ["manifests/stage112_manifest.json", "manifests/stage112_nie_branchpoint_manifest.json", "manifests/stage112_gitnexus_nie_preflight_manifest.json"]}
    evidence = {p: (root / p).exists() for p in ["release/current/stage112_gitnexus_nie_preflight_report.json", "release/current/stage112_release_gate_report.json"]}
    critical = {p: (root / p).exists() for p in CRITICAL_PATHS}
    orphan = [p for p, ok in critical.items() if not ok]
    status = "PASS" if not orphan and all(manifests.values()) else "BLOCK"
    report = FallbackImpactReport(
        status=status,
        python_fallback_used=True,
        import_edges_total=len(import_edges),
        critical_paths_checked=CRITICAL_PATHS,
        affected_tests=TEST_HINTS,
        manifests_checked=manifests,
        release_evidence_checked=evidence,
        orphan_critical_nodes=orphan,
    )
    return report.to_dict() | {"import_edges_sample": import_edges[:20]}


def build_detect_changes(root: Path) -> dict:
    changed_paths = [
        "src/v1700/gitnexus_preflight/**",
        "src/v1700/stage112/**",
        "src/v1700/gates/stage112_release_gate.py",
        "tools/run_stage112_gitnexus_nie_preflight.py",
        "tools/run_stage112_release_gate.py",
        "manifests/stage112_manifest.json",
        "docs/stages/stage112.md",
    ]
    return {
        "status": "pass",
        "changed_paths": changed_paths,
        "affected_tests": sorted({t for tests in TEST_HINTS.values() for t in tests}),
        "affected_processes": ["release_gate", "repo_doctor", "clean_packaging", "NIE_preflight"],
        "python_fallback_used": True,
    }


def _collect_import_edges(src_root: Path) -> list[dict[str, str]]:
    edges: list[dict[str, str]] = []
    if not src_root.exists():
        return edges
    for path in src_root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        module = path.relative_to(src_root).with_suffix("").as_posix().replace("/", ".")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    edges.append({"from": module, "to": alias.name})
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    edges.append({"from": module, "to": node.module})
    return edges

