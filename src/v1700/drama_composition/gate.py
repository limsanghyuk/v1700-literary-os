from __future__ import annotations
from .contracts import KoreanDramaComposition


class DramaCompositionGate:
    """Validates Korean drama composition hierarchy.

    The central rule: do not collapse series story, macro plot, broadcast episode,
    micro plot, sequence, and scene into one ambiguous 'episode' concept.
    """
    def validate(self, composition: KoreanDramaComposition) -> dict:
        issues: list[str] = []
        data = composition.to_dict()
        if "SeriesStory != MacroPlot" not in composition.hierarchy_claim:
            issues.append("hierarchy_claim_missing")
        if len(composition.macro_plots) < 3:
            issues.append("macro_plot_count_below_required")
        macro_ids = {plot.macro_plot_id for plot in composition.macro_plots}
        if len(composition.episodes) < len(composition.macro_plots) * 2:
            issues.append("episode_composition_map_too_small")
        if len(composition.supporting_character_web.characters) < 4:
            issues.append("supporting_character_web_too_thin")
        if len(composition.supporting_character_web.relation_edges) < 3:
            issues.append("supporting_relation_edges_too_thin")
        for episode in composition.episodes:
            if episode.macro_plot_id not in macro_ids:
                issues.append(f"episode_without_macro_plot:{episode.episode_id}")
            if len(episode.micro_plots) < 2:
                issues.append(f"micro_plot_count_below_required:{episode.episode_id}")
            if len(episode.sequences) < len(episode.micro_plots):
                issues.append(f"sequence_chain_not_covering_micro_plots:{episode.episode_id}")
            for sequence in episode.sequences:
                if len(sequence.scenes) < 3:
                    issues.append(f"scene_chain_too_short:{sequence.sequence_id}")
        return {
            "status": "pass" if not issues else "blocked",
            "issues": issues,
            "macro_plot_count": len(composition.macro_plots),
            "broadcast_episode_count": len(composition.episodes),
            "micro_plot_count": sum(len(ep.micro_plots) for ep in composition.episodes),
            "sequence_count": sum(len(ep.sequences) for ep in composition.episodes),
            "scene_count": sum(len(seq.scenes) for ep in composition.episodes for seq in ep.sequences),
            "supporting_character_count": len(composition.supporting_character_web.characters),
            "relation_edge_count": len(composition.supporting_character_web.relation_edges),
            "hierarchy_claim": composition.hierarchy_claim,
            "sample_episode": data["episodes"][0] if data["episodes"] else {},
        }
