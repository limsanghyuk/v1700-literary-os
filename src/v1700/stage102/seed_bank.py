from __future__ import annotations

from .contracts import WriterTrialSeed


def build_stage102_seed_bank() -> tuple[WriterTrialSeed, ...]:
    return (
        WriterTrialSeed(
            seed_id="stage102_seed_prose_01",
            prompt="A Seoul trauma surgeon finds that a past rescue has become the key to a political cover-up.",
            target_mode="PROSE",
            evaluation_goal="Measure reader-facing prose, emotional access, and anti-LLM surface.",
            constraints=("no raw reveal", "surface-only prose", "scene necessity required"),
        ),
        WriterTrialSeed(
            seed_id="stage102_seed_scenario_01",
            prompt="A quiet archivist and a rookie detective track a prop-led clue across three episodes.",
            target_mode="SCENARIO",
            evaluation_goal="Measure scene beats, action movement, dialogue silence, and prop-led reveal control.",
            constraints=("scenario beats visible", "reveal budget preserved", "production scene mapping required"),
        ),
        WriterTrialSeed(
            seed_id="stage102_seed_hybrid_01",
            prompt="A family restaurant drama expands into a 16-episode season about memory, labor, and betrayal.",
            target_mode="HYBRID",
            evaluation_goal="Measure hybrid longform structure, revision efficiency, and writer workflow usability.",
            constraints=("longform continuity", "payoff debt audit", "writer approval guard"),
        ),
    )
