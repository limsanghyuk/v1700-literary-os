from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Mapping

from .interface import ProviderBridgeInterface


@dataclass
class ProviderHealthRecord:
    provider_id: str
    state: str = "UNKNOWN"  # UNKNOWN | HEALTHY | DEGRADED | OFFLINE
    last_check_ts: float = 0.0
    consecutive_failures: int = 0
    last_error: str = ""


class ProviderHealthMonitor:
    HEALTH_CHECK_INTERVAL_SECONDS = 60
    FAILURE_THRESHOLD = 3
    RECOVERY_INTERVAL_SECONDS = 300
    CHECK_TIMEOUT_SECONDS = 5

    def __init__(self, providers: Mapping[str, ProviderBridgeInterface] | None = None, fixture_health: Mapping[str, bool] | None = None):
        self.providers = dict(providers or {})
        self.fixture_health = dict(fixture_health or {})
        self.records: dict[str, ProviderHealthRecord] = {pid: ProviderHealthRecord(pid) for pid in self.providers}
        for pid, healthy in self.fixture_health.items():
            self.records[pid] = ProviderHealthRecord(pid, state="HEALTHY" if healthy else "OFFLINE", last_check_ts=time.time())

    def is_healthy(self, provider_id: str) -> bool:
        if provider_id in self.fixture_health:
            return bool(self.fixture_health[provider_id])
        record = self.records.setdefault(provider_id, ProviderHealthRecord(provider_id))
        if record.state == "DEGRADED" and time.time() - record.last_check_ts < self.RECOVERY_INTERVAL_SECONDS:
            return False
        if time.time() - record.last_check_ts < self.HEALTH_CHECK_INTERVAL_SECONDS and record.state in {"HEALTHY", "OFFLINE", "DEGRADED"}:
            return record.state == "HEALTHY"
        return self.force_check(provider_id)

    def get_healthy_providers(self) -> list[str]:
        return [pid for pid in sorted(set(self.providers) | set(self.fixture_health)) if self.is_healthy(pid)]

    def mark_failed(self, provider_id: str, error: str = "") -> None:
        record = self.records.setdefault(provider_id, ProviderHealthRecord(provider_id))
        record.consecutive_failures += 1
        record.last_error = error
        record.last_check_ts = time.time()
        record.state = "DEGRADED" if record.consecutive_failures >= self.FAILURE_THRESHOLD else "OFFLINE"
        self.fixture_health[provider_id] = False if provider_id in self.fixture_health else self.fixture_health.get(provider_id, False)

    def mark_healthy(self, provider_id: str) -> None:
        record = self.records.setdefault(provider_id, ProviderHealthRecord(provider_id))
        record.consecutive_failures = 0
        record.last_error = ""
        record.last_check_ts = time.time()
        record.state = "HEALTHY"
        if provider_id in self.fixture_health:
            self.fixture_health[provider_id] = True

    def force_check(self, provider_id: str) -> bool:
        if provider_id in self.fixture_health:
            healthy = bool(self.fixture_health[provider_id])
            self.records[provider_id] = ProviderHealthRecord(provider_id, state="HEALTHY" if healthy else "OFFLINE", last_check_ts=time.time())
            return healthy
        provider = self.providers.get(provider_id)
        if provider is None:
            self.records[provider_id] = ProviderHealthRecord(provider_id, state="OFFLINE", last_check_ts=time.time(), last_error="provider_not_registered")
            return False
        try:
            healthy = provider.is_available()
        except Exception as exc:  # defensive health boundary
            healthy = False
            self.records[provider_id] = ProviderHealthRecord(provider_id, state="OFFLINE", last_check_ts=time.time(), consecutive_failures=1, last_error=str(exc))
            return False
        self.records[provider_id] = ProviderHealthRecord(provider_id, state="HEALTHY" if healthy else "OFFLINE", last_check_ts=time.time(), consecutive_failures=0 if healthy else 1)
        return healthy
