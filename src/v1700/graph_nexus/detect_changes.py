from __future__ import annotations

from v1700.graph_nexus.code_graph import CodeGraph


def detect_graph_nexus_changes(previous: CodeGraph | None, current: CodeGraph) -> dict:
    if previous is None:
        return {
            "status": "pass",
            "mode": "initial_scan",
            "changed_paths": [node.path for node in current.nodes],
            "stale_index": False,
        }
    old_paths = {node.path for node in previous.nodes}
    new_paths = {node.path for node in current.nodes}
    changed = sorted(old_paths.symmetric_difference(new_paths))
    return {
        "status": "pass",
        "mode": "compare",
        "changed_paths": changed,
        "stale_index": bool(changed),
    }
