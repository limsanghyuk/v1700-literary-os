import re

class RhythmRewriter:
    def rewrite(self, text: str) -> str:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?。！？])\s+|(?<=다\.)\s+", text) if s.strip()]
        if len(sentences) <= 1:
            return text
        # Insert paragraph break before the last beat to create reader-facing cadence.
        head = " ".join(sentences[:-1])
        tail = sentences[-1]
        return f"{head}\n\n{tail}"

    def score(self, text: str) -> float:
        lengths = [len(s) for s in re.split(r"[.!?。！？]|다\.", text) if s.strip()]
        if not lengths:
            return 7.0
        variety = len(set(min(5, l // 20) for l in lengths))
        return min(10.0, 7.2 + variety * 0.55)
