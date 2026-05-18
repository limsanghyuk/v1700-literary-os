from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GraphNexusContextPacket:
    code_summary: dict
    narrative_summary: dict
    lineage_summary: dict
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "code_summary": self.code_summary,
            "narrative_summary": self.narrative_summary,
            "lineage_summary": self.lineage_summary,
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class Node1GraphPacket:
    canon_context: dict
    timeline_context: dict
    blast_radius: dict

    def to_dict(self) -> dict:
        return {
            "packet_type": "Node1GraphPacket",
            "canon_context": self.canon_context,
            "timeline_context": self.timeline_context,
            "blast_radius": self.blast_radius,
        }


@dataclass(frozen=True)
class Node2GraphSurfacePacket:
    scene_id: str
    surface_tone: str = "reader_facing"
    relationship_pressure: str = "medium"
    sensory_anchors: tuple[str, ...] = ()
    forbidden_reveal_labels: tuple[str, ...] = ()
    style_drift_warnings: tuple[str, ...] = ()
    raw_secret: str | None = field(default=None, repr=False)

    def assert_surface_safe(self) -> None:
        if self.raw_secret:
            raise AssertionError("Node2GraphSurfacePacket must not contain raw_secret")
        for label in self.forbidden_reveal_labels:
            if ":" in label or len(label.split()) > 5:
                raise AssertionError("Node2 forbidden reveal labels must be opaque and short")

    def to_dict(self) -> dict:
        self.assert_surface_safe()
        return {
            "packet_type": "Node2GraphSurfacePacket",
            "scene_id": self.scene_id,
            "surface_tone": self.surface_tone,
            "relationship_pressure": self.relationship_pressure,
            "sensory_anchors": list(self.sensory_anchors),
            "forbidden_reveal_labels": list(self.forbidden_reveal_labels),
            "style_drift_warnings": list(self.style_drift_warnings),
        }


@dataclass(frozen=True)
class Node3GraphCriticPacket:
    contradiction_risks: tuple[str, ...] = ()
    leakage_risks: tuple[str, ...] = ()
    impact: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "packet_type": "Node3GraphCriticPacket",
            "contradiction_risks": list(self.contradiction_risks),
            "leakage_risks": list(self.leakage_risks),
            "impact": self.impact,
        }
