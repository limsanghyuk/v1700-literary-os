from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StageLineageNode:
    stage_id: str
    title: str
    introduced_concepts: tuple[str, ...]
    surviving_runtime_value: str
    current_status: str = "PRESERVED"

    def to_dict(self) -> dict:
        return {
            "stage_id": self.stage_id,
            "title": self.title,
            "introduced_concepts": list(self.introduced_concepts),
            "surviving_runtime_value": self.surviving_runtime_value,
            "current_status": self.current_status,
        }


@dataclass(frozen=True)
class StageLineageGraph:
    nodes: tuple[StageLineageNode, ...] = ()

    @classmethod
    def from_manifest(cls, root: Path) -> "StageLineageGraph":
        manifest_path = root / "manifests" / "stage_lineage_manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        nodes = [
            StageLineageNode(
                stage_id=item["stage_id"],
                title=item.get("title", ""),
                introduced_concepts=tuple(item.get("introduced_concepts", [])),
                surviving_runtime_value=item.get("surviving_runtime_value", ""),
                current_status="OPTIONAL_SIDECAR"
                if item["stage_id"] == "STAGE61-66"
                else "PRESERVED",
            )
            for item in data.get("stages", [])
        ]
        if not any(node.stage_id == "STAGE72.1" for node in nodes):
            nodes.append(
                StageLineageNode(
                    stage_id="STAGE72.1",
                    title="GraphNexus Restoration Patch",
                    introduced_concepts=(
                        "GraphNexus",
                        "GitNexus optional sidecar",
                        "Python fallback graph gate",
                    ),
                    surviving_runtime_value="Restores graph intelligence as optional live architecture.",
                    current_status="LIVE_PATCH",
                )
            )
        return cls(tuple(nodes))

    def has_stage(self, stage_id: str) -> bool:
        return any(node.stage_id == stage_id for node in self.nodes)

    def concepts_for(self, stage_id: str) -> tuple[str, ...]:
        for node in self.nodes:
            if node.stage_id == stage_id:
                return node.introduced_concepts
        return ()

    def to_dict(self) -> dict:
        return {
            "node_count": len(self.nodes),
            "nodes": [node.to_dict() for node in self.nodes],
        }
