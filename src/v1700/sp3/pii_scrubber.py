from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Pattern, Any
import re


@dataclass(frozen=True)
class ScrubDetailSP3:
    original: str
    text: str
    removed_by_category: dict[str, int] = field(default_factory=dict)

    @property
    def scrubbed_text(self) -> str:
        return self.text

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "scrubbed_text": self.text,
            "removed_by_category": dict(self.removed_by_category),
        }


@dataclass(frozen=True)
class DatasetScrubReport:
    records: list[dict[str, Any]]
    category_totals: dict[str, int]
    record_count: int
    pii_scrubbed: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "records": self.records,
            "category_totals": dict(self.category_totals),
            "record_count": self.record_count,
            "pii_scrubbed": self.pii_scrubbed,
        }


@dataclass(frozen=True)
class _PatternSpec:
    category: str
    pattern: Pattern[str]
    priority: int


class PIIScrubberSP3:
    """ADR-008 compliant local PII scrubber.

    Credit-card matching deliberately has higher priority than bank-account
    matching. The previously observed failure masked
    ``1234-5678-9012-3456`` as ``[계좌번호]6``; non-overlap matching with this
    priority order prevents that class of partial replacement.
    """

    # Public category labels are Korean because existing evidence reports use
    # Korean replacement tokens.
    _PATTERNS: tuple[_PatternSpec, ...] = (
        _PatternSpec("신용카드", re.compile(r"(?<!\d)(?:\d{4}[- ]?){3}\d{4}(?!\d)"), 10),
        _PatternSpec("주민등록번호", re.compile(r"(?<!\d)\d{6}-[1-4]\d{6}(?!\d)"), 20),
        _PatternSpec("전화번호", re.compile(r"(?<!\d)(?:\+82[- ]?)?0?1[016789][- ]?\d{3,4}[- ]?\d{4}(?!\d)"), 30),
        _PatternSpec("이메일", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), 40),
        _PatternSpec("계좌번호", re.compile(r"(?<!\d)\d{2,6}[- ]\d{2,6}[- ]\d{2,8}(?![- ]?\d)"), 50),
        _PatternSpec("IP주소", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), 60),
        _PatternSpec("URL", re.compile(r"\bhttps?://[^\s)]+"), 70),
        _PatternSpec("주소", re.compile(r"[가-힣A-Za-z0-9\- ]+(?:로|길)\s?\d+(?:번길)?\s?\d*"), 80),
        _PatternSpec("여권번호", re.compile(r"\b[MSROD][0-9]{8}\b", re.IGNORECASE), 90),
        _PatternSpec("사업자등록번호", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{5}(?!\d)"), 100),
    )

    def __init__(self, patterns: Iterable[_PatternSpec] | None = None) -> None:
        self.patterns = tuple(sorted(patterns or self._PATTERNS, key=lambda p: p.priority))

    def _collect_matches(self, text: str) -> list[tuple[int, int, str]]:
        candidates: list[tuple[int, int, str, int]] = []
        for spec in self.patterns:
            for m in spec.pattern.finditer(text):
                candidates.append((m.start(), m.end(), spec.category, spec.priority))
        # Prefer earlier priority, then longer span. Drop overlaps deterministically.
        candidates.sort(key=lambda item: (item[3], -(item[1] - item[0]), item[0]))
        accepted: list[tuple[int, int, str]] = []
        occupied: list[tuple[int, int]] = []
        for start, end, category, _priority in candidates:
            if any(not (end <= a or start >= b) for a, b in occupied):
                continue
            accepted.append((start, end, category))
            occupied.append((start, end))
        accepted.sort(key=lambda item: item[0])
        return accepted

    def scrub(self, text: str) -> ScrubDetailSP3:
        source = str(text or "")
        matches = self._collect_matches(source)
        if not matches:
            return ScrubDetailSP3(original=source, text=source, removed_by_category={})
        totals: dict[str, int] = {}
        out: list[str] = []
        cursor = 0
        for start, end, category in matches:
            out.append(source[cursor:start])
            out.append(f"[{category}]")
            totals[category] = totals.get(category, 0) + 1
            cursor = end
        out.append(source[cursor:])
        return ScrubDetailSP3(original=source, text="".join(out), removed_by_category=totals)

    def scrub_dataset(self, records: Iterable[Mapping[str, Any]]) -> DatasetScrubReport:
        scrubbed: list[dict[str, Any]] = []
        totals: dict[str, int] = {}
        for record in records:
            clone = dict(record)
            text_key = "text" if "text" in clone else "content" if "content" in clone else "text"
            detail = self.scrub(str(clone.get(text_key, "")))
            clone[text_key] = detail.text
            clone["pii_scrubbed"] = True
            clone["removed_by_category"] = dict(detail.removed_by_category)
            for category, count in detail.removed_by_category.items():
                totals[category] = totals.get(category, 0) + count
            scrubbed.append(clone)
        return DatasetScrubReport(records=scrubbed, category_totals=totals, record_count=len(scrubbed))
