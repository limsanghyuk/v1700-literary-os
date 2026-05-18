from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Literal


@dataclass(frozen=True)
class StyleFeatureVector:
    project_id: str
    source_scope: Literal["FEATURE_ONLY", "LOCAL_FULL_TEXT"]
    sentence_rhythm: float
    sensory_density: float
    dialogue_ratio: float
    introspection_ratio: float
    scene_motion_ratio: float
    lexical_signature_hash: str
    raw_text_retained: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class StyleGenome:
    genome_id: str
    author_profile_id: str
    feature_vectors: tuple[StyleFeatureVector, ...]
    authorial_rhythm: float
    sensory_preference: float
    dialogue_preference: float
    introspection_preference: float
    motion_preference: float
    privacy_mode: Literal["FEATURE_ONLY", "LOCAL_FULL_TEXT"] = "FEATURE_ONLY"
    raw_manuscript_retained: bool = False
    provider_export_allowed: bool = False

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["feature_vectors"] = [fv.to_dict() for fv in self.feature_vectors]
        return payload


@dataclass(frozen=True)
class DriftGuardReport:
    status: str
    genome_id: str
    voice_drift_score: float
    allowed_delta: float
    action: Literal["ALLOW", "WARN", "BLOCK"]
    issues: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Node2AuthorProfileBridge:
    status: str
    genome_id: str
    node2_profile_id: str
    allowed_surface_controls: tuple[str, ...]
    forbidden_controls: tuple[str, ...]
    raw_reveal_access: int = 0
    provider_call_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)
