from __future__ import annotations

from dataclasses import dataclass, field

from .response import ProviderResponse


@dataclass
class ProviderCallRecord:
    provider_id: str
    provider_kind: str
    call_count: int = 0
    total_tokens: int = 0
    total_latency_ms: float = 0.0
    estimated_cost_usd: float | None = 0.0


@dataclass
class ProviderCostLedger:
    series_id: str
    episode_idx: int | None = None
    records: dict[str, ProviderCallRecord] = field(default_factory=dict)
    total_estimated_cost_usd: float | None = 0.0
    release_mode: bool = True

    def record_call(self, response: ProviderResponse) -> None:
        pid = response.provider_id
        if pid not in self.records:
            self.records[pid] = ProviderCallRecord(provider_id=pid, provider_kind=response.provider_kind)
        rec = self.records[pid]
        rec.call_count += 1
        rec.total_tokens += int(response.tokens_used or 0)
        rec.total_latency_ms += float(response.latency_ms or 0.0)
        if response.estimated_cost_usd is None or rec.estimated_cost_usd is None or self.total_estimated_cost_usd is None:
            rec.estimated_cost_usd = None
            self.total_estimated_cost_usd = None
        else:
            rec.estimated_cost_usd += float(response.estimated_cost_usd)
            self.total_estimated_cost_usd += float(response.estimated_cost_usd)

    def to_dict(self) -> dict:
        return {
            "series_id": self.series_id,
            "episode_idx": self.episode_idx,
            "release_mode": self.release_mode,
            "total_estimated_cost_usd": self.total_estimated_cost_usd,
            "records": {pid: rec.__dict__ for pid, rec in self.records.items()},
        }
