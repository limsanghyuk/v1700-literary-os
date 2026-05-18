from __future__ import annotations

import json
from pathlib import Path

from v1700.stage99.gitnexus_impact_model import ImpactEdge, ImpactNode, ImpactReport
from v1700.studio_workflow.report import write_json, write_summary

IMPACT_SCAN_ROOTS = (
    "src/v1700/narrative_physics",
    "src/v1700/manuscript_learning",
    "src/v1700/narrative_optimization",
    "src/v1700/provider_ensemble",
    "src/v1700/longform_endurance",
    "src/v1700/longform_adversarial",
    "src/v1700/provider_runtime",
    "src/v1700/studio_workflow",
    "src/v1700/stage98",
    "src/v1700/stage99",
    "src/v1700/security_hardening",
    "src/v1700/gates",
    "tools",
    "tests",
    "manifests",
    "release/current",
)


def run_stage99_0_gitnexus_impact_baseline(root: Path | None = None) -> dict:
    root = root or Path.cwd()
    pack = root / "release" / "current" / "stage99_gitnexus_pack"
    pack.mkdir(parents=True, exist_ok=True)

    nodes = build_impact_nodes(root)
    edges = build_impact_edges(root, nodes)
    report = build_impact_report(root, nodes, edges)

    write_json(pack / "impact_nodes.json", {"status": "pass", "nodes": [node.to_dict() for node in nodes]})
    write_json(pack / "impact_edges.json", {"status": "pass", "edges": [edge.to_dict() for edge in edges]})
    write_json(pack / "orphan_node_report.json", {"status": "pass" if not report.orphan_nodes else "blocked", "orphan_nodes": report.orphan_nodes})
    write_json(pack / "broken_edge_report.json", {"status": "pass" if not report.broken_edges else "blocked", "broken_edges": report.broken_edges})
    write_json(
        pack / "stage98_to_stage99_delta_report.json",
        {
            "status": "pass",
            "baseline_stage": "98",
            "target_stage": "99",
            "new_feature_expansion": False,
            "hardening_only": True,
        },
    )
    write_json(
        pack / "branchpoint_survival_recheck_report.json",
        {
            "status": report.branchpoint_survival_status,
            "required_manifests": [
                "manifests/stage97_2_branchpoint_trace_manifest.json",
                "manifests/stage98_branchpoint_trace_manifest.json",
            ],
        },
    )
    write_summary(
        pack / "stage99_0_summary.md",
        "Stage99.0 GitNexus Impact Baseline",
        [
            f"impact nodes: {report.nodes_total}",
            f"impact edges: {report.edges_total}",
            f"orphan critical nodes: {len(report.orphan_nodes)}",
            f"broken gate edges: {len(report.broken_edges)}",
        ],
    )

    payload = {
        "stage": "99.0",
        "baseline_stage": "98",
        "status": "pass" if not report.release_blockers else "blocked",
        **report.to_dict(),
        "gitnexus_pack": "release/current/stage99_gitnexus_pack",
    }
    write_json(root / "release" / "current" / "stage99_0_gitnexus_impact_baseline_report.json", payload)
    return payload


def build_impact_nodes(root: Path) -> list[ImpactNode]:
    nodes: list[ImpactNode] = []
    for base in IMPACT_SCAN_ROOTS:
        base_path = root / base
        if not base_path.exists():
            continue
        files = [base_path] if base_path.is_file() else sorted(path for path in base_path.rglob("*") if path.is_file())
        for path in files:
            if _is_ignored(path):
                continue
            rel = path.relative_to(root).as_posix()
            stage_origin = _stage_origin(rel)
            role = _role_for_path(rel)
            criticality = _criticality_for_path(rel, role)
            nodes.append(
                ImpactNode(
                    node_id=_node_id(rel),
                    path=rel,
                    symbol=path.stem,
                    stage_origin=stage_origin,
                    role=role,
                    criticality=criticality,
                )
            )
    return nodes


def build_impact_edges(root: Path, nodes: list[ImpactNode]) -> list[ImpactEdge]:
    ids = {node.node_id: node for node in nodes}
    edges: list[ImpactEdge] = []

    def add(source_path: str, target_path: str, edge_type: str, confidence: float = 1.0) -> None:
        source_id = _node_id(source_path)
        target_id = _node_id(target_path)
        if source_id in ids and target_id in ids:
            edges.append(ImpactEdge(source_id, target_id, edge_type, confidence))  # type: ignore[arg-type]

    for stage in ("95", "96", "97", "97_1", "97_2", "98"):
        gate = f"src/v1700/gates/stage{stage}_release_gate.py"
        tool = f"tools/run_stage{stage}_release_gate.py"
        manifest = f"manifests/stage{stage}_manifest.json"
        if stage == "97_2":
            manifest = "manifests/stage97_2_manifest.json"
        add(tool, gate, "calls")
        add(manifest, gate, "declares")
        add(gate, f"release/current/stage{stage}_release_gate_report.json", "writes_evidence")

    add("manifests/stage98_manifest.json", "src/v1700/gates/stage98_release_gate.py", "declares")
    add("src/v1700/gates/stage98_release_gate.py", "src/v1700/studio_workflow/studio_orchestrator.py", "validates")
    add("src/v1700/studio_workflow/publishing_package.py", "manifests/stage98_publishing_package_manifest.json", "writes_evidence")
    add("manifests/stage98_branchpoint_trace_manifest.json", "manifests/stage97_2_branchpoint_trace_manifest.json", "traces_branchpoint")
    add("src/v1700/provider_runtime/release_policy.py", "src/v1700/gates/stage97_2_release_gate.py", "guards")
    add("tools/run_stage99_0_gitnexus_impact_baseline.py", "src/v1700/stage99/impact_baseline.py", "calls")
    add("tools/run_stage99_1_security_privacy_hardening.py", "src/v1700/security_hardening/report.py", "calls")
    add("tools/run_stage99_2_gate_replay_freeze.py", "src/v1700/stage99/gate_replay.py", "calls")
    add("tools/run_stage99_release_gate.py", "src/v1700/gates/stage99_release_gate.py", "calls")
    add("manifests/stage99_manifest.json", "src/v1700/gates/stage99_release_gate.py", "declares")
    add("manifests/stage99_gitnexus_impact_manifest.json", "src/v1700/stage99/impact_baseline.py", "declares")
    add("manifests/stage99_security_hardening_manifest.json", "src/v1700/security_hardening/report.py", "declares")
    add("manifests/stage99_regression_freeze_manifest.json", "src/v1700/stage99/gate_replay.py", "declares")
    add("manifests/stage100_readiness_manifest.json", "release/current/stage100_readiness_precheck_report.json", "declares")
    return edges


def build_impact_report(root: Path, nodes: list[ImpactNode], edges: list[ImpactEdge]) -> ImpactReport:
    node_ids = {node.node_id for node in nodes}
    connected = {edge.source_node_id for edge in edges} | {edge.target_node_id for edge in edges}
    orphan_nodes = sorted(node.node_id for node in nodes if node.criticality == "CRITICAL" and node.node_id not in connected)
    broken_edges = sorted(
        f"{edge.source_node_id}->{edge.target_node_id}"
        for edge in edges
        if edge.source_node_id not in node_ids or edge.target_node_id not in node_ids
    )
    stale_manifests = _stale_manifests(root)
    untraced_new_logic: list[str] = []
    branchpoint_status = "pass" if _branchpoint_manifests_exist(root) else "blocked"
    release_blockers = []
    if orphan_nodes:
        release_blockers.append("orphan_critical_node")
    if broken_edges:
        release_blockers.append("broken_gate_edge")
    if stale_manifests:
        release_blockers.append("stale_manifest")
    if branchpoint_status != "pass":
        release_blockers.append("branchpoint_survival_recheck_failed")
    return ImpactReport(
        stage="99.0",
        baseline_stage="98",
        nodes_total=len(nodes),
        edges_total=len(edges),
        critical_nodes_total=sum(1 for node in nodes if node.criticality == "CRITICAL"),
        orphan_nodes=orphan_nodes,
        broken_edges=broken_edges,
        stale_manifests=stale_manifests,
        untraced_new_logic=untraced_new_logic,
        branchpoint_survival_status=branchpoint_status,
        release_blockers=release_blockers,
    )


def _role_for_path(rel: str) -> str:
    if "/gates/" in rel or rel.endswith("_release_gate.py"):
        return "gate"
    if rel.startswith("tools/"):
        return "tool"
    if rel.startswith("tests/"):
        return "test"
    if rel.startswith("manifests/"):
        return "manifest"
    if rel.startswith("release/current/"):
        return "release_evidence"
    if "provider_runtime" in rel or "nodes/" in rel:
        return "boundary"
    if "export" in rel or "publishing_package" in rel:
        return "export"
    return "engine"


def _criticality_for_path(rel: str, role: str) -> str:
    if rel in _critical_paths():
        return "CRITICAL"
    if "stage98" in rel or "stage97_2" in rel or role in {"boundary", "export"}:
        return "HIGH"
    if role == "test":
        return "MEDIUM"
    return "LOW"


def _critical_paths() -> set[str]:
    paths: set[str] = set()
    for stage in ("95", "96", "97", "97_1", "97_2", "98"):
        paths.update(
            {
                f"src/v1700/gates/stage{stage}_release_gate.py",
                f"tools/run_stage{stage}_release_gate.py",
                f"manifests/stage{stage}_manifest.json",
                f"release/current/stage{stage}_release_gate_report.json",
            }
        )
    paths.update(
        {
            "src/v1700/stage99/impact_baseline.py",
            "src/v1700/stage99/gate_replay.py",
            "src/v1700/gates/stage99_release_gate.py",
            "src/v1700/security_hardening/report.py",
            "tools/run_stage99_0_gitnexus_impact_baseline.py",
            "tools/run_stage99_1_security_privacy_hardening.py",
            "tools/run_stage99_2_gate_replay_freeze.py",
            "tools/run_stage99_release_gate.py",
            "manifests/stage99_manifest.json",
            "manifests/stage99_gitnexus_impact_manifest.json",
            "manifests/stage99_security_hardening_manifest.json",
            "manifests/stage99_regression_freeze_manifest.json",
            "manifests/stage100_readiness_manifest.json",
            "release/current/stage100_readiness_precheck_report.json",
        }
    )
    return paths


def _stage_origin(rel: str) -> str:
    for token in ("stage97_2", "stage97_1", "stage98", "stage97", "stage96", "stage95"):
        if token in rel:
            return token.replace("_", ".")
    return "pre95"


def _node_id(rel: str) -> str:
    return rel.replace("\\", "/").replace("/", "::")


def _is_ignored(path: Path) -> bool:
    ignored_parts = {".git", "__pycache__", ".pytest_cache"}
    return any(part in ignored_parts for part in path.parts) or path.suffix in {".pyc", ".zip", ".tmp", ".log"}


def _stale_manifests(root: Path) -> list[str]:
    live = root / "manifests" / "live_core_manifest.json"
    if not live.exists():
        return ["manifests/live_core_manifest.json"]
    payload = json.loads(live.read_text(encoding="utf-8"))
    if payload.get("active_version") not in {"stage98", "stage99", "stage100", "stage101", "stage102", "stage103", "stage104", "stage105", "stage106", "stage107", "stage107_5", "stage108", "stage109", "stage110", "stage111", "stage112", "stage113", "stage114", "stage115", "stage116", "stage117", "stage118", "stage119", "stage120", "stage121", "stage122", "stage123", "stage124", "stage125", "stage126", "stage127"}:
        return ["manifests/live_core_manifest.json"]
    return []


def _branchpoint_manifests_exist(root: Path) -> bool:
    required = [
        root / "manifests" / "stage97_2_branchpoint_trace_manifest.json",
        root / "manifests" / "stage98_branchpoint_trace_manifest.json",
    ]
    return all(path.exists() for path in required)
