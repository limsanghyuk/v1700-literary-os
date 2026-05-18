from __future__ import annotations

from dataclasses import dataclass
from contextlib import contextmanager
from typing import Iterator


@dataclass(frozen=True)
class NoopSpan:
    name: str

    def set_attribute(self, key: str, value: object) -> None:
        return None

    def end(self) -> None:
        return None


class NoopTracer:
    """Dependency-free tracer fallback used when OpenTelemetry is unavailable."""

    @contextmanager
    def start_as_current_span(self, name: str) -> Iterator[NoopSpan]:
        yield NoopSpan(name)

    def start_span(self, name: str) -> NoopSpan:
        return NoopSpan(name)


def get_tracer(name: str = "v1700") -> object:
    try:
        from opentelemetry import trace  # type: ignore

        tracer = trace.get_tracer(name)
        return tracer if tracer is not None else NoopTracer()
    except Exception:
        return NoopTracer()


def test_tracer_not_none() -> bool:
    return get_tracer() is not None
