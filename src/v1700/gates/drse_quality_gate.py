from __future__ import annotations

from pathlib import Path

from v1700.literary_formulas.drse import DRSEEngine, DRSEInputNode


def run_drse_quality_gate(root: Path | None = None) -> dict:
    nodes = (
        DRSEInputNode("cause", "causality", "과거 사건의 결과가 현재 장면을 압박한다", ("causal",), ("stage39",)),
        DRSEInputNode("emotion", "emotion", "신뢰와 불신이 관계의 감정선을 바꾼다", ("emotion",), ("stage56",)),
        DRSEInputNode("residue", "residue", "복선 잔향은 사물의 위치로만 남는다", ("residue", "reveal"), ("stage52",)),
    )
    context = DRSEEngine().score("과거 사건의 결과와 불신의 감정선이 현재 선택을 압박한다", nodes)
    top = context.top_scores(1)[0] if context.scores else None
    issues = []
    if not context.scores:
        issues.append("drse_no_scores")
    if top and top.final_score <= 0:
        issues.append("drse_top_score_zero")
    if not context.to_surface_directives():
        issues.append("drse_surface_directives_missing")
    return {
        "stage": "73.1",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "score_count": len(context.scores),
        "dominant_pattern": context.dominant_pattern,
        "surface_directive_count": len(context.to_surface_directives()),
        "provider_default_calls": 0,
    }
