from statistics import mean
from .anti_llm_filter import AntiLLMSurfaceFilter
from .emotion_renderer import EmotionToBehaviorRenderer
from .rhythm_rewriter import RhythmRewriter
from .dialogue_renderer import DialogueTasteRenderer
from .sensory_anchor import SensoryAnchorInjector

class ReaderSurfaceScorer:
    def __init__(self):
        self.anti = AntiLLMSurfaceFilter()
        self.emotion = EmotionToBehaviorRenderer()
        self.rhythm = RhythmRewriter()
        self.dialogue = DialogueTasteRenderer()
        self.sensory = SensoryAnchorInjector()

    def score(self, text: str) -> dict[str, float]:
        direct = self.emotion.direct_emotion_count(text)
        emotion_accessibility = max(0.0, 8.8 - direct * 1.3)
        scores = {
            "anti_llm": round(self.anti.score(text), 2),
            "emotion_accessibility": round(emotion_accessibility, 2),
            "naturalness": round(min(10.0, 8.0 + (0.4 if "\n\n" in text else 0.0) + (0.3 if len(text) > 120 else 0.0)), 2),
            "rhythm": round(self.rhythm.score(text), 2),
            "dialogue_taste": round(self.dialogue.score(text), 2),
            "sensory_afterimage": round(self.sensory.score(text), 2),
        }
        scores["reader_surface_average"] = round(mean(scores.values()), 2)
        return scores
