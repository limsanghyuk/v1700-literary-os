from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from v1700.graph_nexus.code_graph import CodeGraph, CodeGraphBuilder
from v1700.graph_nexus.graph_nexus_packet import GraphNexusContextPacket
from v1700.graph_nexus.impact import compute_graph_nexus_impact
from v1700.graph_nexus.narrative_graph import NarrativeGraph
from v1700.graph_nexus.stage_lineage_graph import StageLineageGraph
from v1700.ir.scene_intent import EmotionalDelta, SceneIntentIR


@dataclass(frozen=True)
class GraphNexusRegistry:
    code_graph: CodeGraph
    narrative_graph: NarrativeGraph
    stage_lineage_graph: StageLineageGraph

    @classmethod
    def build(cls, root: Path) -> "GraphNexusRegistry":
        sample_scene = SceneIntentIR(
            scene_id="S72_1_SAMPLE",
            scene_goal="Preserve GraphNexus restoration without leaking locked reveals",
            conflict="Optional graph sidecar must not become runtime dependency",
            emotional_delta=EmotionalDelta("uncertain", "focused"),
            forbidden_reveals=("locked_reveal_A",),
            setting_seed="threshold room",
        )
        return cls(
            code_graph=CodeGraphBuilder().build(root),
            narrative_graph=NarrativeGraph.from_scene_intents([sample_scene]),
            stage_lineage_graph=StageLineageGraph.from_manifest(root),
        )

    def context_packet(self, target: str = "ALL") -> GraphNexusContextPacket:
        impact = compute_graph_nexus_impact(
            target,
            self.code_graph,
            self.narrative_graph,
            self.stage_lineage_graph,
        )
        warnings = tuple(impact.get("risks", []))
        return GraphNexusContextPacket(
            code_summary={
                "available": True,
                "source": self.code_graph.source,
                "node_count": len(self.code_graph.nodes),
            },
            narrative_summary={
                "available": True,
                "node_count": len(self.narrative_graph.nodes),
                "edge_count": len(self.narrative_graph.edges),
            },
            lineage_summary={
                "available": True,
                "node_count": len(self.stage_lineage_graph.nodes),
                "stage72_1_present": self.stage_lineage_graph.has_stage("STAGE72.1"),
            },
            warnings=warnings,
        )

    def to_dict(self) -> dict:
        return {
            "code_graph": self.code_graph.to_dict(),
            "narrative_graph": self.narrative_graph.to_dict(),
            "stage_lineage_graph": self.stage_lineage_graph.to_dict(),
        }
