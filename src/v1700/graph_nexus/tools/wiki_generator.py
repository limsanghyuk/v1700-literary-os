from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.registry import GraphNexusRegistry
from v1700.graph_nexus.tools.contracts import GeneratedWikiPage


def generate_graph_nexus_wiki(root: Path) -> dict:
    out_dir = root / "docs" / "generated" / "wiki"
    out_dir.mkdir(parents=True, exist_ok=True)
    registry = GraphNexusRegistry.build(root)
    architecture_path = _write(
        out_dir / "architecture_wiki.md",
        "# Architecture Wiki\n\n"
        "V1700 is organized as Node1 architecture, Node2 reader-facing rendering, Node3 critic validation, and GraphNexus structural memory.\n\n"
        "Source files:\n"
        "- src/v1700/cli.py\n"
        "- src/v1700/graph_nexus/registry.py\n"
        "- src/v1700/gates/stage72_2_release_gate.py\n",
    )
    lineage_lines = "\n".join(
        f"- {node.stage_id}: {node.title}" for node in registry.stage_lineage_graph.nodes
    )
    lineage_path = _write(
        out_dir / "stage_lineage_wiki.md",
        "# Stage Lineage Wiki\n\n"
        f"{lineage_lines}\n\n"
        "Source files:\n"
        "- manifests/stage_lineage_manifest.json\n"
        "- docs/stages/STAGE_INDEX.md\n",
    )
    narrative_path = _write(
        out_dir / "narrative_wiki.md",
        "# Narrative Wiki\n\n"
        "GraphNexus keeps narrative graph context separate from Node2 prose rendering. Node2 receives only surface-safe packets.\n\n"
        "Source files:\n"
        "- src/v1700/graph_nexus/narrative_graph.py\n"
        "- src/v1700/graph_nexus/graph_nexus_packet.py\n",
    )
    return {
        "status": "pass",
        "pages": [
            GeneratedWikiPage("Architecture Wiki", architecture_path, ("src/v1700/cli.py",)).to_dict(),
            GeneratedWikiPage("Stage Lineage Wiki", lineage_path, ("manifests/stage_lineage_manifest.json",)).to_dict(),
            GeneratedWikiPage("Narrative Wiki", narrative_path, ("src/v1700/graph_nexus/narrative_graph.py",)).to_dict(),
        ],
    }


def _write(path: Path, text: str) -> str:
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
    return path.as_posix()
