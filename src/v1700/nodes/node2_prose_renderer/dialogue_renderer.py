class DialogueTasteRenderer:
    def rewrite(self, text: str, dialogue_seed: str = "") -> str:
        if dialogue_seed and "“" not in text and '"' not in text:
            return f"{text}\n\n“{dialogue_seed}”"
        return text

    def score(self, text: str) -> float:
        if "“" in text or '"' in text:
            return 8.2
        return 7.9
