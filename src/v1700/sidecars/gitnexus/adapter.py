from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.code_graph import CodeGraph
from v1700.sidecars.gitnexus.probe import probe_gitnexus
from v1700.sidecars.gitnexus.python_fallback import build_python_fallback_code_graph


class GitNexusAdapter:
    def build_code_graph(self, root: Path) -> CodeGraph:
        probe = probe_gitnexus()
        # Stage72.1 keeps GitNexus optional. The deterministic Python graph is
        # authoritative for release gates unless an explicit sidecar adapter is added.
        graph = build_python_fallback_code_graph(root)
        return CodeGraph(
            nodes=graph.nodes,
            fallback_used=not probe.installed,
            source="gitnexus_optional_probe" if probe.installed else "python_fallback",
        )
