"""SP3 data-quality, privacy, dataset-card, and synthetic augmentation utilities.

This package is intentionally local-only and dependency-light so that release gates
can validate ADR-008 style dataset hygiene without provider calls.
"""

from .trace_quality_filter import DedupReport, SP3FilterResult, TraceQualityFilterSP3
from .pii_scrubber import DatasetScrubReport, PIIScrubberSP3, ScrubDetailSP3
from .dataset_card import DatasetCard, DatasetCardGenerator
from .synthetic_augmentor import SyntheticAugmentorSP3, SyntheticRecordSP3

__all__ = [
    "DedupReport",
    "SP3FilterResult",
    "TraceQualityFilterSP3",
    "DatasetScrubReport",
    "PIIScrubberSP3",
    "ScrubDetailSP3",
    "DatasetCard",
    "DatasetCardGenerator",
    "SyntheticAugmentorSP3",
    "SyntheticRecordSP3",
]
