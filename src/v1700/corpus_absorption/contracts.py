from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class SourceAssetRecord:
    asset_id: str
    relative_path: str
    asset_kind: str
    extension: str
    size_bytes: int
    sha256: str
    rights_status: str
    access_policy: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CanonicalWorkRecord:
    work_id: str
    work_title: str
    source_media: str
    source_type: str
    source_reference: str
    has_txt: bool
    has_scenes: bool
    has_chunks: bool
    has_features: bool
    scene_count: int
    chunk_count: int
    feature_scene_count: int
    parse_methods: dict[str, int]
    qc_flags: tuple[str, ...]
    rights_status: str
    access_policy: str
    processing_status: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class RagIndexRecord:
    work_id: str
    scene_count: int
    chunk_count: int
    scene_index_ready: bool
    chunk_index_ready: bool
    vector_store_kind: str
    vector_binding_mode: str
    embedding_cache_available: bool
    retrieval_policy: str
    text_policy: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class LearningSignalRecord:
    work_id: str
    feature_scene_count: int
    mean_conflict_intensity: float | None
    mean_scene_energy_ratio: float | None
    mean_motif_residue_score: float | None
    mean_curiosity_gradient: float | None
    mean_dialogue_ratio: float | None
    signal_keys: tuple[str, ...]
    learning_ready: bool

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class CorpusAbsorptionReport:
    corpus_id: str
    status: str
    source_asset_records: tuple[SourceAssetRecord, ...]
    canonical_work_records: tuple[CanonicalWorkRecord, ...]
    rag_index_records: tuple[RagIndexRecord, ...]
    learning_signal_records: tuple[LearningSignalRecord, ...]
    issues: tuple[str, ...] = ()
    counters: dict[str, int] = field(default_factory=dict)
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["source_asset_records"] = [record.to_dict() for record in self.source_asset_records]
        payload["canonical_work_records"] = [record.to_dict() for record in self.canonical_work_records]
        payload["rag_index_records"] = [record.to_dict() for record in self.rag_index_records]
        payload["learning_signal_records"] = [record.to_dict() for record in self.learning_signal_records]
        return payload
