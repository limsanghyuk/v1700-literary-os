from __future__ import annotations
from v1700.longform.engine import LongformExecutionEngine
from v1700.reabsorption import run_stage60_reabsorption_smoke
from v1700.nodes.node2_prose_renderer.rewrite_orchestrator import run_node2_rewrite_restoration_smoke
from v1700.drama_execution import run_drama_execution_smoke

class FullLiteraryOSIntegration:
    """Stage79 final integration of branchpoint logic, literary formulas, and longform execution."""
    def run(self, prompt: str = "침묵한 조력자와 사라진 증거를 둘러싼 장편 드라마") -> dict:
        longform = LongformExecutionEngine().execute(prompt).to_dict()
        stage60 = run_stage60_reabsorption_smoke(prompt)
        node2 = run_node2_rewrite_restoration_smoke()
        drama = run_drama_execution_smoke()
        issues: list[str] = []
        if longform.get("status") != "pass":
            issues.append("stage74_longform_blocked")
        if stage60.get("status") != "pass":
            issues.append("stage60_reabsorption_blocked")
        if node2.get("status") != "pass":
            issues.append("node2_rewrite_blocked")
        if drama.get("status") != "pass":
            issues.append("drama_execution_blocked")
        scale = stage60.get("stage50_scale_plan", {})
        if scale.get("scene_count_total", 0) < 532:
            issues.append("full_literary_scene_scale_not_recovered")
        final_output = {
            "kind": "stage79_integrated_smoke_output",
            "season_arc": longform.get("plan", {}).get("season_arc"),
            "episode_count": scale.get("episode_count"),
            "sequence_count_total": scale.get("sequence_count_total"),
            "scene_count_total": scale.get("scene_count_total"),
            "rendered_scene_count": len(longform.get("rendered", [])),
            "selected_reader_surface_text": node2.get("rewrite", {}).get("selected", {}).get("text"),
            "drama_pressure_peak": drama.get("emotional_pressure_valve", {}).get("peak"),
        }
        return {
            "stage": "79",
            "status": "pass" if not issues else "blocked",
            "issues": issues,
            "final_output": final_output,
            "longform_execution": longform,
            "stage60_literary_engine_reabsorption": stage60,
            "node2_rewrite_restoration": node2,
            "drama_execution_reabsorption": drama,
            "provider_default_calls": 0,
            "node2_raw_reveal_access_count": 0,
            "claim": "Stage79 integrates branchpoint survival, Stage60-scale literary engine metadata, Node2 rewrite restoration, drama execution, and Stage74 literary formula smoke into one local-first loop.",
        }

def run_full_literary_os_smoke(prompt: str = "침묵한 조력자와 사라진 증거를 둘러싼 장편 드라마") -> dict:
    return FullLiteraryOSIntegration().run(prompt)
