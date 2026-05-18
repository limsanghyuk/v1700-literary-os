from __future__ import annotations
from dataclasses import dataclass
from .core_logic_survival import build_core_logic_survival_matrix

@dataclass(frozen=True)
class OrganicRelation:
    source: str
    relation: str
    target: str
    evidence: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {"source": self.source, "relation": self.relation, "target": self.target, "evidence": list(self.evidence)}


def build_organic_relation_graph() -> tuple[OrganicRelation, ...]:
    relations: list[OrganicRelation] = []
    for entry in build_core_logic_survival_matrix():
        relations.append(OrganicRelation(entry.source_branchpoint, "DEFINES_LOGIC", entry.logic_id))
        if entry.current_location:
            relations.append(OrganicRelation(entry.logic_id, "CURRENT_LOCATION", entry.current_location, entry.evidence_files))
        for test in entry.test_coverage:
            relations.append(OrganicRelation(entry.logic_id, "REQUIRES_TEST", test))
        for gate in entry.gate_coverage:
            relations.append(OrganicRelation(entry.logic_id, "REQUIRES_GATE", gate))
        if entry.reabsorption_priority == "P0" and entry.survival_status != "LIVE_RUNTIME":
            relations.append(OrganicRelation(entry.logic_id, "BLOCKS_FULL_LITERARY_CLAIM_UNTIL_REABSORBED", "Stage76_or_later"))
    relations.append(OrganicRelation("GitNexus", "SUPPORTS", "GraphNexus CodeGraph"))
    relations.append(OrganicRelation("GraphNexus", "SUPPORTS", "BranchpointLogicGraph"))
    relations.append(OrganicRelation("BranchpointLogicGraph", "PROTECTS", "Longform Literary Engine"))
    relations.append(OrganicRelation("DRSE", "SAFE_PROJECTS_TO_NODE2", "Node2GraphSurfacePacket"))
    return tuple(relations)
