from dataclasses import dataclass

@dataclass(frozen=True)
class SurfaceOnlyContract:
    allow_new_facts: bool = False
    allow_causal_change: bool = False
    allow_reveal_change: bool = False
    allow_character_truth_change: bool = False
    allow_scene_goal_change: bool = False
    allow_timeline_change: bool = False
    surface_only: bool = True

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def assert_valid(self) -> None:
        if not self.surface_only:
            raise AssertionError("Node2 must remain surface_only")
        blocked = [
            self.allow_new_facts,
            self.allow_causal_change,
            self.allow_reveal_change,
            self.allow_character_truth_change,
            self.allow_scene_goal_change,
            self.allow_timeline_change,
        ]
        if any(blocked):
            raise AssertionError("Node2 contract violation: structural permissions must be false")
