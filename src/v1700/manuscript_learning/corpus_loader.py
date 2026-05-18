from __future__ import annotations

from pathlib import Path


def load_synthetic_corpus(root: Path | None = None) -> tuple[dict, ...]:
    root = root or Path.cwd()
    sample_root = root / "sample_longform_project_01"
    source = "sample_longform_project_01" if sample_root.exists() else "synthetic_stage96_fixture"
    return tuple(
        {
            "episode_id": f"ep{i:02d}",
            "scene_id": f"ep{i:02d}_sc{j:02d}",
            "source": source,
            "summary": f"Episode {i} scene {j} shifts belief, raises conflict, and preserves surface-only reveal handling.",
            "characters": ("protagonist", "rival") if j % 2 else ("protagonist", "mentor"),
            "reveal_events": 1 if j in {3, 7} else 0,
            "foreshadow_events": 1 if j in {2, 6} else 0,
            "curiosity_hook": j in {5, 10},
        }
        for i in range(1, 5)
        for j in range(1, 11)
    )
