import re

GENERIC_REPLACEMENTS = {
    "그 순간, 모든 것이 달라질 것만 같았다": "문틈으로 들어오던 바람이 멎었다",
    "그 순간": "잠깐",
    "말로 표현할 수 없는": "말하지 않은",
    "복잡한 감정": "식은 숨",
    "운명의 장난": "기울어진 시간",
    "가슴이 먹먹했다": "목 안쪽이 마른 종이처럼 붙었다",
}

class AntiLLMSurfaceFilter:
    def rewrite(self, text: str) -> str:
        out = text
        for src, dst in GENERIC_REPLACEMENTS.items():
            out = out.replace(src, dst)
        out = re.sub(r"(그는|그녀는)\s+(.{0,12})감정을 느꼈다", r"\1 손끝을 늦게 접었다", out)
        return out

    def score(self, text: str) -> float:
        hits = sum(1 for key in GENERIC_REPLACEMENTS if key in text)
        hits += len(re.findall(r"복잡한 감정|말로 표현할 수 없는|모든 것이 달라질", text))
        return max(0.0, 10.0 - hits * 1.4)
