from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.code_graph import CodeGraph, CodeGraphBuilder


def build_python_fallback_code_graph(root: Path) -> CodeGraph:
    return CodeGraphBuilder().build(root)
