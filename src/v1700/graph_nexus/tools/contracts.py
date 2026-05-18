from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GraphNexusQueryRequest:
    query: str
    context: str = ""
    goal: str = ""
    limit: int = 5
    use_gitnexus: bool = True


@dataclass(frozen=True)
class GraphNexusQueryResult:
    status: str
    query: str
    source: str
    matches: tuple[dict, ...] = ()
    gitnexus: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "query": self.query,
            "source": self.source,
            "matches": [dict(match) for match in self.matches],
            "gitnexus": dict(self.gitnexus),
        }


@dataclass(frozen=True)
class GraphNexusContextRequest:
    target: str = "ALL"
    use_gitnexus: bool = True


@dataclass(frozen=True)
class GraphNexusImpactRequest:
    target: str
    include_tests: bool = True
    use_gitnexus: bool = True


@dataclass(frozen=True)
class GraphNexusDetectChangesReport:
    status: str
    source: str
    mode: str
    changed_paths: tuple[str, ...] = ()
    impacted_tests: tuple[str, ...] = ()
    stale_index: bool = False
    gitnexus: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "source": self.source,
            "mode": self.mode,
            "changed_paths": list(self.changed_paths),
            "impacted_tests": list(self.impacted_tests),
            "stale_index": self.stale_index,
            "gitnexus": dict(self.gitnexus),
        }


@dataclass(frozen=True)
class GraphNexusRouteMap:
    status: str
    routes: tuple[dict, ...]
    missing_paths: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "routes": [dict(route) for route in self.routes],
            "missing_paths": list(self.missing_paths),
        }


@dataclass(frozen=True)
class GraphNexusToolMap:
    status: str
    tools: tuple[dict, ...]
    gates: tuple[dict, ...]
    tests: tuple[str, ...]
    missing_paths: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "tools": [dict(tool) for tool in self.tools],
            "gates": [dict(gate) for gate in self.gates],
            "tests": list(self.tests),
            "missing_paths": list(self.missing_paths),
        }


@dataclass(frozen=True)
class GraphNexusShapeCheckReport:
    status: str
    checks: tuple[dict, ...]
    violations: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "checks": [dict(check) for check in self.checks],
            "violations": list(self.violations),
        }


@dataclass(frozen=True)
class GeneratedStageSkill:
    stage: str
    path: str
    source_files: tuple[str, ...]

    def to_dict(self) -> dict:
        return {"stage": self.stage, "path": self.path, "source_files": list(self.source_files)}


@dataclass(frozen=True)
class GeneratedNodeSkill:
    node: str
    path: str
    source_files: tuple[str, ...]

    def to_dict(self) -> dict:
        return {"node": self.node, "path": self.path, "source_files": list(self.source_files)}


@dataclass(frozen=True)
class GeneratedSceneSkill:
    scene: str
    path: str
    source_files: tuple[str, ...]

    def to_dict(self) -> dict:
        return {"scene": self.scene, "path": self.path, "source_files": list(self.source_files)}


@dataclass(frozen=True)
class GeneratedWikiPage:
    title: str
    path: str
    source_files: tuple[str, ...]

    def to_dict(self) -> dict:
        return {"title": self.title, "path": self.path, "source_files": list(self.source_files)}
