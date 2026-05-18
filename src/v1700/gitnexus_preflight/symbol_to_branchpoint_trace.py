from __future__ import annotations

from pathlib import Path
from .contracts import SymbolProbe

SYMBOLS = {
    "MAEOrchestrator": ["stage88_ai_agent_benchmark", "stage113_mae_reward_bridge"],
    "PhysicsCoefficientUpdater": ["stage96_narrative_optimization", "stage113_reward_bridge"],
    "PhysicsCoefficientStore": ["stage96_coefficient_memory", "stage114_amw"],
    "EmotionalMomentumTracker": ["stage73_literary_formulas", "stage114_amw"],
    "HybridRetriever": ["stage53_retrieval_router", "stage116_domain_rag"],
    "ReaderSimulator": ["stage88_agent_benchmark", "stage113_mae_reward_bridge"],
    "CharacterBirthGate": ["stage51_character_event_time_ledger", "stage115_cim"],
    "CharacterClusterDetector": ["stage80_korean_drama_composition", "stage115_cim"],
    "KnowledgeBoundaryGate": ["stage86_arc_reveal_knowledge", "stage115_cim"],
    "NarrativeWeightKernel": ["stage111_1_narrative_weight_kernel", "stage112_preflight"],
    "GitNexusPreflightResult": ["stage112_preflight", "release_gate_integration"],
}

REQUIRED_STAGE112 = {"EmotionalMomentumTracker", "NarrativeWeightKernel", "GitNexusPreflightResult"}


def trace_symbols(root: Path) -> dict:
    probes: list[SymbolProbe] = []
    all_py = list((root / "src").rglob("*.py")) if (root / "src").exists() else []
    cache = {p: p.read_text(encoding="utf-8", errors="ignore") for p in all_py if "__pycache__" not in p.parts and p.name != "symbol_to_branchpoint_trace.py"}
    for symbol, branchpoints in SYMBOLS.items():
        locations = [p.relative_to(root).as_posix() for p, text in cache.items() if symbol in text]
        if symbol == "NarrativeWeightKernel" and (root / "src/v1700/narrative_weight_kernel/report.py").exists():
            locations.append("src/v1700/narrative_weight_kernel/report.py")
        probes.append(SymbolProbe(
            name=symbol,
            expected_kind="class_or_function_or_planned_adapter",
            present=bool(locations),
            locations=locations[:10],
            branchpoints=branchpoints,
            required_for_stage112=symbol in REQUIRED_STAGE112,
        ))
    missing_required = [p.name for p in probes if p.required_for_stage112 and not p.present]
    branchpoint_trace = {p.name: p.branchpoints for p in probes}
    return {
        "status": "pass" if not missing_required else "blocked",
        "queried_symbols": [p.to_dict() for p in probes],
        "missing_required_symbols": missing_required,
        "planned_nie_symbols_missing_but_allowed": [p.name for p in probes if not p.present and not p.required_for_stage112],
        "branchpoint_trace": branchpoint_trace,
    }

