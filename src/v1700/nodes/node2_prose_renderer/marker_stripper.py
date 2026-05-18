import re

INTERNAL_MARKERS = [
    r"\[LOCKED_REVEAL[^\]]*\]",
    r"LOCKED_REVEAL",
    r"candidate not canon",
    r"not canon",
    r"canon state",
    r"Command authority",
    r"External provider calls",
    r"source draft",
    r"refined::",
]

class InternalMarkerStripper:
    def strip(self, text: str) -> str:
        cleaned = text
        for pattern in INTERNAL_MARKERS:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
        return re.sub(r"\s+", " ", cleaned).strip()

    def leakage(self, text: str) -> list[str]:
        return [p for p in INTERNAL_MARKERS if re.search(p, text, flags=re.IGNORECASE)]
