from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Literal

PluginKind = Literal["genre_pack", "evaluator_pack", "export_pack", "provider_adapter_pack", "studio_extension"]
TrustLevel = Literal["core", "review_required", "blocked"]

@dataclass(frozen=True)
class PluginManifest:
    plugin_id: str
    name: str
    version: str
    kind: PluginKind
    entrypoint: str
    trust_level: TrustLevel
    enabled_by_default: bool
    requires_live_provider: bool
    requires_raw_manuscript: bool
    writes_release_evidence: bool
    branchpoint_trace_id: str
    test_target: str

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class PluginValidationResult:
    plugin_id: str
    status: Literal["pass", "warn", "blocked"]
    issues: list[str]

    def to_dict(self) -> dict:
        return asdict(self)
