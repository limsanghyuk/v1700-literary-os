from __future__ import annotations

import pytest

from v1700.cache.semantic_cache import SemanticCache
from v1700.gates.gate24 import run_gate24
from v1700.observability.tracing import get_tracer
from v1700.sp3 import (
    DatasetCardGenerator,
    PIIScrubberSP3,
    SyntheticAugmentorSP3,
    TraceQualityFilterSP3,
)


def test_sp3_pii_credit_card_precedes_account_masking():
    detail = PIIScrubberSP3().scrub("카드 1234-5678-9012-3456 확인")
    assert "[신용카드]" in detail.text
    assert "[계좌번호]6" not in detail.text
    assert detail.removed_by_category["신용카드"] == 1


def test_sp3_dataset_card_rejects_proprietary_license():
    gen = DatasetCardGenerator()
    with pytest.raises(ValueError):
        gen.generate([], [], [], pii_scrubbed=True, dedup_removed=0, license="proprietary")
    card = gen.generate([{"text": "a"}], [], [], pii_scrubbed=True, dedup_removed=0, license="cc-by")
    assert card.to_dict()["license"] == "cc-by"
    assert "license: cc-by" in card.to_yaml_header()


def test_sp3_trace_filter_exact_and_distinct_jaccard_and_dedup():
    filt = TraceQualityFilterSP3()
    assert filt.jaccard("같은 문장 같은 문장", "같은 문장 같은 문장") == 1.0
    assert filt.jaccard("alpha beta gamma", "delta epsilon zeta") == 0.0
    records = [{"id": str(i), "text": "완전히 같은 데이터 샘플", "tier": "A", "license": "internal"} for i in range(5)]
    result = filt.run(records)
    assert result.dedup_report.kept == 1
    assert result.dedup_report.removed == 4
    assert result.total_kept == 1
    assert filt.run([]).total_kept == 0


def test_sp3_synthetic_augmentor_deterministic_and_traceable():
    records = [{"id": "r1", "text": "원문", "quality": 0.9}]
    a = SyntheticAugmentorSP3(seed=42).augment(records)
    b = SyntheticAugmentorSP3(seed=42).augment(records)
    assert a == b
    assert len(a) == 3
    assert all(x["synthetic"] is True and x["source_id"] == "r1" for x in a)
    assert len(SyntheticAugmentorSP3(seed=42).augment(records, target_count=2)) == 2
    assert SyntheticAugmentorSP3(seed=42).augment([], target_count=2) == []


def test_gate24_documented_symbol_aliases():
    report = run_gate24()
    assert report["pass"] is True
    assert len(report["symbols_verified"]) == 33
    assert report["symbols_checked"] == 33
    assert report["symbols_passed"] == 33


def test_observability_tracer_not_none_and_semantic_cache_low_similarity_miss():
    assert get_tracer() is not None
    cache = SemanticCache(similarity_threshold=0.85)
    cache.put("alpha beta gamma", {"hit": True})
    assert cache.get("alpha beta gamma") == {"hit": True}
    assert cache.get("totally unrelated query") is None
