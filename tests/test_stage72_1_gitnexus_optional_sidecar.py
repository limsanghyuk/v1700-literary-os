from pathlib import Path

from v1700.sidecars.gitnexus.adapter import GitNexusAdapter
from v1700.sidecars.gitnexus.probe import probe_gitnexus


ROOT = Path(__file__).resolve().parents[1]


def test_gitnexus_is_optional_and_python_fallback_is_available():
    probe = probe_gitnexus()
    assert probe.optional_runtime_dependency is False
    assert probe.fallback_available is True

    graph = GitNexusAdapter().build_code_graph(ROOT)
    assert graph.nodes
    assert graph.source in {"python_fallback", "gitnexus_optional_probe"}
    assert any("node2_prose_renderer/compiler.py" in node.path for node in graph.nodes)
