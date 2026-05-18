from __future__ import annotations

from pathlib import Path

from v1700.graph_nexus.tools.contracts import GeneratedNodeSkill, GeneratedSceneSkill, GeneratedStageSkill


def generate_graph_nexus_skills(root: Path) -> dict:
    out_dir = root / "docs" / "generated" / "skills"
    out_dir.mkdir(parents=True, exist_ok=True)
    stage = _write(
        out_dir / "stage_skill_stage72_2.md",
        "# StageSkill: Stage72.2\n\n"
        "Purpose: operate GitNexus capabilities through GraphNexus contracts.\n\n"
        "Source files:\n"
        "- src/v1700/graph_nexus/tools/query.py\n"
        "- src/v1700/graph_nexus/tools/context.py\n"
        "- src/v1700/graph_nexus/tools/impact.py\n"
        "- src/v1700/graph_nexus/tools/detect_changes.py\n",
    )
    node = _write(
        out_dir / "node_skill_node2_surface_safety.md",
        "# NodeSkill: Node2 Surface Safety\n\n"
        "Node2 receives only surface-safe graph packets: opaque reveal labels, relationship pressure, sensory anchors, and style warnings.\n\n"
        "Source files:\n"
        "- src/v1700/graph_nexus/graph_nexus_packet.py\n"
        "- src/v1700/graph_nexus/tools/shape_check.py\n",
    )
    scene = _write(
        out_dir / "scene_skill_graph_context_scene.md",
        "# SceneSkill: Graph Context Scene\n\n"
        "Scene generation may use GraphNexus context to preserve continuity, but rendering remains local-first and provider-call-free by default.\n\n"
        "Source files:\n"
        "- src/v1700/graph_nexus/registry.py\n"
        "- src/v1700/nodes/node2_prose_renderer/compiler.py\n",
    )
    return {
        "status": "pass",
        "stage_skill": GeneratedStageSkill("Stage72.2", stage, ("src/v1700/graph_nexus/tools/query.py",)).to_dict(),
        "node_skill": GeneratedNodeSkill("Node2", node, ("src/v1700/graph_nexus/tools/shape_check.py",)).to_dict(),
        "scene_skill": GeneratedSceneSkill("GraphContextScene", scene, ("src/v1700/graph_nexus/registry.py",)).to_dict(),
    }


def _write(path: Path, text: str) -> str:
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
    return path.as_posix()
