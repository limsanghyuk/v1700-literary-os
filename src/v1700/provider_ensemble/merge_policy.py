from __future__ import annotations

from v1700.provider_ensemble.contracts import ProviderCandidate


def build_directive_level_merge(selected: tuple[ProviderCandidate, ...]) -> str:
    strengths = [candidate.provider_kind for candidate in selected]
    return (
        "Use directive-level merge only: preserve the strongest structure, prose surface, reveal timing, "
        f"and dialogue rhythm from {', '.join(strengths)} while rerunning Node2 surface transform guard."
    )
