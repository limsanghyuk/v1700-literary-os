from __future__ import annotations
from pathlib import Path
from v1700.gates.stage79_release_gate import run_stage79_release_gate
from v1700.drama_composition import KoreanDramaCompositionEngine, DramaCompositionGate


def run_stage80_release_gate(root: Path | None = None) -> dict:
    root = root or Path(__file__).resolve().parents[3]
    stage79 = run_stage79_release_gate(root)
    composition = KoreanDramaCompositionEngine().compose(
        "한 인물이 닫힌 제도, 추방의 세계, 귀환의 세계를 통과하며 자신의 역할을 완성하는 한국 드라마"
    )
    composition_gate = DramaCompositionGate().validate(composition)
    issues: list[str] = []
    if stage79.get("status") != "pass":
        issues.append("stage79_release_gate_blocked")
    if composition_gate.get("status") != "pass":
        issues.append("korean_drama_composition_gate_blocked")
    if composition_gate.get("macro_plot_count", 0) < 3:
        issues.append("macro_plot_architecture_missing")
    if composition_gate.get("broadcast_episode_count", 0) < 6:
        issues.append("episode_composition_map_incomplete")
    if composition_gate.get("scene_count", 0) < 54:
        issues.append("scene_chain_scale_incomplete")
    return {
        "stage": "80",
        "status": "pass" if not issues else "blocked",
        "issues": issues,
        "claim": "Stage80 separates Series Story, Macro Plot, Broadcast Episode, Micro Plot, Sequence, and Scene for Korean drama composition.",
        "stage79_release_gate": stage79,
        "korean_drama_composition_gate": composition_gate,
        "provider_default_calls": 0,
        "node2_raw_reveal_access_count": 0,
    }
