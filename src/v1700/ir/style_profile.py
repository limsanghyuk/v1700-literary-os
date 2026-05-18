from dataclasses import dataclass

@dataclass(frozen=True)
class StyleProfileIR:
    profile_id: str = "user_style_profile_v1"
    sentence_rhythm: str = "short-long-mixed"
    metaphor_policy: str = "rare_specific"
    emotion_policy: str = "indirect_behavioral"
    dialogue_policy: str = "understated_with_subtext"
    sensory_axis: tuple[str, ...] = ("light", "temperature", "object_texture")
    anti_elements: tuple[str, ...] = (
        "direct_emotion_label",
        "summary_exposition",
        "generic_poetic_phrase",
        "overexplained_motivation",
        "screenplay_flat_dialogue",
    )

    @classmethod
    def from_dict(cls, data: dict) -> "StyleProfileIR":
        return cls(
            profile_id=data.get("profile_id", cls.profile_id),
            sentence_rhythm=data.get("sentence_rhythm", cls.sentence_rhythm),
            metaphor_policy=data.get("metaphor_policy", cls.metaphor_policy),
            emotion_policy=data.get("emotion_policy", cls.emotion_policy),
            dialogue_policy=data.get("dialogue_policy", cls.dialogue_policy),
            sensory_axis=tuple(data.get("sensory_axis", cls.sensory_axis)),
            anti_elements=tuple(data.get("anti_elements", cls.anti_elements)),
        )

    def to_dict(self) -> dict:
        return {
            "profile_id": self.profile_id,
            "sentence_rhythm": self.sentence_rhythm,
            "metaphor_policy": self.metaphor_policy,
            "emotion_policy": self.emotion_policy,
            "dialogue_policy": self.dialogue_policy,
            "sensory_axis": list(self.sensory_axis),
            "anti_elements": list(self.anti_elements),
        }
