from __future__ import annotations
from .contracts import EditorialReviewer

def build_reviewer_profiles() -> list[EditorialReviewer]:
    return [
        EditorialReviewer("rev_literary_critic", "LITERARY_CRITIC", "literary merit, image density, voice integrity", 1.15),
        EditorialReviewer("rev_dramaturg", "DRAMATURG", "conflict, scene necessity, dramatic turn", 1.10),
        EditorialReviewer("rev_market_editor", "MARKET_EDITOR", "commercial readability, hook, positioning", 1.00),
        EditorialReviewer("rev_genre_editor", "GENRE_EDITOR", "genre promise, thriller tension, payoff setup", 1.00),
        EditorialReviewer("rev_continuity_auditor", "CONTINUITY_AUDITOR", "longform continuity, character memory, branchpoint survival", 1.20),
        EditorialReviewer("rev_scenario_producer", "SCENARIO_PRODUCER", "scene beat, production feasibility, visual clarity", 1.05),
    ]
