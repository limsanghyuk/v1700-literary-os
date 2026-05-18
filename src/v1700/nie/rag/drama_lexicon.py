from __future__ import annotations

import re
from dataclasses import dataclass, field

from v1700.nie.rag.contracts import DramaLexiconBoost

_TOKEN_RE = re.compile(r"[A-Za-z0-9_가-힣]+")


@dataclass(frozen=True)
class DramaLexicon:
    character_names: frozenset[str] = field(default_factory=lambda: frozenset({
        "민준", "수진", "해원", "회장", "형사", "minjun", "sujin", "haewon", "chairman", "detective"
    }))
    episode_terms: frozenset[str] = field(default_factory=lambda: frozenset({
        "화", "회", "1화", "2화", "3화", "4화", "최종화", "에피소드", "episode", "finale"
    }))
    drama_keywords: frozenset[str] = field(default_factory=lambda: frozenset({
        "클라이맥스", "사건", "반전", "복선", "고백", "배신", "대사", "장면", "비밀", "climax", "scene", "payoff", "reveal", "plot"
    }))
    emotion_words: frozenset[str] = field(default_factory=lambda: frozenset({
        "배신감", "긴장", "공포", "연민", "카타르시스", "슬픔", "분노", "감정", "몰입", "dread", "sympathy", "tension", "catharsis"
    }))

    def normalize(self, term: str) -> str:
        return term.strip().lower()

    def tokenize(self, text: str) -> list[str]:
        return [m.group(0).lower() for m in _TOKEN_RE.finditer(text or "")]

    def category(self, term: str) -> str:
        token = self.normalize(term)
        if token in {self.normalize(t) for t in self.character_names}:
            return "CHARACTER_NAMES"
        if token in {self.normalize(t) for t in self.episode_terms}:
            return "EPISODE_TERMS"
        if token in {self.normalize(t) for t in self.emotion_words}:
            return "EMOTION_WORDS"
        if token in {self.normalize(t) for t in self.drama_keywords}:
            return "DRAMA_KEYWORDS"
        if re.fullmatch(r"\d+화", token):
            return "EPISODE_TERMS"
        return "OTHER"

    def boost_weight(self, term: str) -> float:
        category = self.category(term)
        return {
            "CHARACTER_NAMES": 1.5,
            "EPISODE_TERMS": 1.3,
            "DRAMA_KEYWORDS": 1.2,
            "EMOTION_WORDS": 1.15,
        }.get(category, 1.0)

    def boosts_for_query(self, query: str) -> list[DramaLexiconBoost]:
        boosts: list[DramaLexiconBoost] = []
        seen: set[str] = set()
        for token in self.tokenize(query):
            if token in seen:
                continue
            seen.add(token)
            category = self.category(token)
            boost = self.boost_weight(token)
            if boost > 1.0:
                boosts.append(DramaLexiconBoost(term=token, category=category, boost=boost))
        return boosts
