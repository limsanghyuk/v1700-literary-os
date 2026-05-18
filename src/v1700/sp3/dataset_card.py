from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class DatasetCard:
    name: str
    version: str
    license: str
    train_count: int
    val_count: int
    test_count: int
    pii_scrubbed: bool
    dedup_removed: int
    synthetic_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat())
    adr: str = "ADR-008"

    @property
    def total_count(self) -> int:
        return self.train_count + self.val_count + self.test_count

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "license": self.license,
            "train_count": self.train_count,
            "val_count": self.val_count,
            "test_count": self.test_count,
            "total_count": self.total_count,
            "pii_scrubbed": self.pii_scrubbed,
            "dedup_removed": self.dedup_removed,
            "synthetic_count": self.synthetic_count,
            "created_at": self.created_at,
            "adr": self.adr,
        }

    def to_yaml_header(self) -> str:
        data = self.to_dict()
        lines = ["---"]
        for key, value in data.items():
            if isinstance(value, bool):
                rendered = "true" if value else "false"
            else:
                rendered = str(value)
            lines.append(f"{key}: {rendered}")
        lines.append("---")
        return "\n".join(lines) + "\n"

    def to_markdown(self) -> str:
        return (
            f"# Dataset Card: {self.name}\n\n"
            f"- Version: {self.version}\n"
            f"- License: {self.license}\n"
            f"- ADR: {self.adr}\n"
            f"- Total records: {self.total_count}\n"
            f"- Train / Val / Test: {self.train_count} / {self.val_count} / {self.test_count}\n"
            f"- PII scrubbed: {self.pii_scrubbed}\n"
            f"- Dedup removed: {self.dedup_removed}\n"
            f"- Synthetic records: {self.synthetic_count}\n"
            f"- Created at: {self.created_at}\n"
        )


class DatasetCardGenerator:
    """Generate ADR-008 dataset cards with strict license validation."""

    ALLOWED_LICENSES = {"cc-by", "cc-by-sa", "public-domain", "public_domain", "CC_BY", "CC_BY_SA", "PUBLIC_DOMAIN"}

    @classmethod
    def normalize_license(cls, license: str) -> str:
        value = str(license or "").strip().lower().replace("_", "-")
        if value == "public-domain":
            return "public_domain"
        if value == "cc-by":
            return "cc-by"
        if value == "cc-by-sa":
            return "cc-by-sa"
        return value

    @staticmethod
    def _count(items: Iterable[Any] | int | None) -> int:
        if items is None:
            return 0
        if isinstance(items, int):
            return items
        if hasattr(items, "__len__"):
            return len(items)  # type: ignore[arg-type]
        return sum(1 for _ in items)

    def generate(
        self,
        train: Iterable[Mapping[str, Any]] | int | None,
        val: Iterable[Mapping[str, Any]] | int | None,
        test: Iterable[Mapping[str, Any]] | int | None,
        *,
        pii_scrubbed: bool,
        dedup_removed: int,
        license: str = "cc-by",
        name: str = "sp3_dataset",
        version: str = "V497-SP3",
        synthetic_count: int = 0,
    ) -> DatasetCard:
        normalized = self.normalize_license(license)
        allowed = {self.normalize_license(v) for v in self.ALLOWED_LICENSES}
        if normalized not in allowed:
            raise ValueError(f"ADR-008 disallows dataset license: {license}")
        return DatasetCard(
            name=name,
            version=version,
            license=normalized,
            train_count=self._count(train),
            val_count=self._count(val),
            test_count=self._count(test),
            pii_scrubbed=bool(pii_scrubbed),
            dedup_removed=int(dedup_removed),
            synthetic_count=int(synthetic_count),
        )
