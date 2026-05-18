from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.graph_nexus_packet import Node2GraphSurfacePacket
from v1700.graph_nexus.tools.contracts import GraphNexusShapeCheckReport


def run_graph_nexus_shape_check(root: Path) -> GraphNexusShapeCheckReport:
    checks: list[dict] = []
    violations: list[str] = []
    packet = Node2GraphSurfacePacket(
        scene_id="S72_2_SHAPE_CHECK",
        sensory_anchors=("door hinge", "cold light"),
        forbidden_reveal_labels=("locked-A",),
    )
    try:
        packet.to_dict()
        checks.append({"name": "node2_surface_packet_safe", "status": "pass"})
    except AssertionError as exc:
        violations.append(str(exc))

    forbidden_terms = ("raw_secret", "canon_secret", "full_graph_internals")
    scanned_paths = [
        root / "docs" / "generated" / "skills",
        root / "docs" / "generated" / "wiki",
    ]
    for scan_root in scanned_paths:
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            if any(term in text for term in forbidden_terms):
                violations.append(f"forbidden term leaked in {path.relative_to(root).as_posix()}")
    checks.append({"name": "generated_docs_no_raw_reveal_terms", "status": "pass" if not violations else "blocked"})
    return GraphNexusShapeCheckReport(
        status="pass" if not violations else "blocked",
        checks=tuple(checks),
        violations=tuple(violations),
    )
