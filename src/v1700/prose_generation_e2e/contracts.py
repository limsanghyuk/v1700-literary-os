from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class E2ESampleBundle:
    project: dict
    characters: dict
    world: dict
    plot_outline: str
    scene_request: dict
    benchmark_expectations: dict

    def to_dict(self) -> dict:
        return {
            "project": self.project,
            "characters": self.characters,
            "world": self.world,
            "plot_outline_excerpt": self.plot_outline[:240],
            "scene_request": self.scene_request,
            "benchmark_expectations": self.benchmark_expectations,
        }


@dataclass(frozen=True)
class CriticResult:
    status: str
    issues: tuple[str, ...]
    provider_default_calls: int = 0
    node2_raw_reveal_access: int = 0

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "issues": list(self.issues),
            "provider_default_calls": self.provider_default_calls,
            "node2_raw_reveal_access": self.node2_raw_reveal_access,
        }
