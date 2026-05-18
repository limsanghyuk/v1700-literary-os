from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import sqrt
from typing import Any
import re

_TOKEN_RE = re.compile(r"[\w가-힣]+", re.UNICODE)


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(str(text or "").lower())


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(v * b.get(k, 0.0) for k, v in a.items())
    na = sqrt(sum(v * v for v in a.values()))
    nb = sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


@dataclass(frozen=True)
class CacheHit:
    key: str
    value: Any
    similarity: float


class SemanticCache:
    """Small deterministic semantic cache with conservative miss behavior."""

    def __init__(self, *, similarity_threshold: float = 0.85) -> None:
        self.similarity_threshold = float(similarity_threshold)
        self._entries: list[tuple[str, dict[str, float], Any]] = []

    @staticmethod
    def _embedding(text: str) -> dict[str, float]:
        counts: dict[str, float] = {}
        for token in _tokens(text):
            counts[token] = counts.get(token, 0.0) + 1.0
        return counts

    @staticmethod
    def key_for(text: str) -> str:
        return sha256(str(text or "").encode("utf-8")).hexdigest()

    def put(self, text: str, value: Any) -> str:
        key = self.key_for(text)
        self._entries.append((key, self._embedding(text), value))
        return key

    def get(self, text: str) -> Any | None:
        hit = self.lookup(text)
        return None if hit is None else hit.value

    def lookup(self, text: str) -> CacheHit | None:
        probe = self._embedding(text)
        best: CacheHit | None = None
        for key, emb, value in self._entries:
            similarity = _cosine(probe, emb)
            if best is None or similarity > best.similarity:
                best = CacheHit(key=key, value=value, similarity=similarity)
        if best is None or best.similarity < self.similarity_threshold:
            return None
        return best

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)
