from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NodeAuthorityRule:
    state_name: str
    node1_access: str
    node2_access: str
    node3_access: str
    node1_module: str
    node2_module: str
    node3_module: str
    rationale: str

    def to_dict(self) -> dict[str, str]:
        return {
            "state_name": self.state_name,
            "node1_access": self.node1_access,
            "node2_access": self.node2_access,
            "node3_access": self.node3_access,
            "node1_module": self.node1_module,
            "node2_module": self.node2_module,
            "node3_module": self.node3_module,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class PacketRoute:
    route_name: str
    source_packet: str
    target_node: str
    delivery_form: str
    blocked_content: str
    module_anchor: str
    rationale: str

    def to_dict(self) -> dict[str, str]:
        return {
            "route_name": self.route_name,
            "source_packet": self.source_packet,
            "target_node": self.target_node,
            "delivery_form": self.delivery_form,
            "blocked_content": self.blocked_content,
            "module_anchor": self.module_anchor,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class SurfaceProjectionRule:
    state_name: str
    source_field: str
    node2_projection: str
    node3_projection: str
    blocked_to_node2: str
    rationale: str

    def to_dict(self) -> dict[str, str]:
        return {
            "state_name": self.state_name,
            "source_field": self.source_field,
            "node2_projection": self.node2_projection,
            "node3_projection": self.node3_projection,
            "blocked_to_node2": self.blocked_to_node2,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class BoundaryControl:
    name: str
    description: str
    enforced: bool
    evidence: str

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "name": self.name,
            "description": self.description,
            "enforced": self.enforced,
            "evidence": self.evidence,
        }
