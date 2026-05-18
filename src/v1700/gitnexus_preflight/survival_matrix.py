from __future__ import annotations

from pathlib import Path

BRANCHPOINT_FILES = {
    "stage51_character_event_time_ledger": "src/v1700/ledgers/character_event_time.py",
    "stage52_reveal_budget_memory_guard": "src/v1700/ledgers/reveal_budget.py",
    "stage72_graphnexus_lineage": "src/v1700/graph_nexus/stage_lineage_graph.py",
    "stage80_korean_drama_composition": "src/v1700/drama_composition/engine.py",
    "stage86_arc_reveal_knowledge": "src/v1700/arc_reveal_knowledge/series_arc_planner.py",
    "stage95_narrative_physics": "src/v1700/narrative_physics/engine.py",
    "stage96_coefficient_memory": "src/v1700/manuscript_learning/coefficient_memory.py",
    "stage97_longform_endurance": "src/v1700/longform_endurance/endurance_orchestrator.py",
    "stage97_1_adversarial_validation": "src/v1700/longform_adversarial/adversarial_orchestrator.py",
    "stage107_longform_production_suite": "src/v1700/longform_production/suite_orchestrator.py",
    "stage111_absorption_candidate_bridge": "src/v1700/stage111/orchestrator.py",
    "stage111_1_narrative_weight_kernel": "src/v1700/narrative_weight_kernel/report.py",
}


def build_survival_matrix(root: Path) -> dict[str, bool]:
    return {name: (root / rel).exists() for name, rel in BRANCHPOINT_FILES.items()}


def survival_status(matrix: dict[str, bool]) -> dict:
    missing = [name for name, ok in matrix.items() if not ok]
    return {"status": "pass" if not missing else "blocked", "missing": missing, "survival_matrix": matrix}

