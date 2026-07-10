from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class FormulaSignalStoreSpec:
    name: str
    path: str
    source_report: str
    mode: str
    advisory_only: bool
    canonical_mutation_allowed: bool

    def to_dict(self) -> dict[str, str | bool]:
        return asdict(self)


@dataclass(frozen=True)
class FormulaSignalIndexEntry:
    formula_signal_id: str
    work_id: str
    formula_id: str
    formula_group: str
    output_signal_type: str
    review_status: str
    writer_ide_panel_ref: str
    confidence: float
    checksum: str

    def to_dict(self) -> dict[str, str | float]:
        return asdict(self)


@dataclass(frozen=True)
class WriterIdeAdvisoryCard:
    card_id: str
    panel_ref: str
    work_id: str
    headline: str
    summary: str
    severity: str
    signal_refs: tuple[str, ...]
    badges: tuple[str, ...]
    advisory_only: bool
    canonical_mutation_allowed: bool

    def to_dict(self) -> dict[str, str | bool | tuple[str, ...]]:
        return asdict(self)
