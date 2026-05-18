DIRECT_EMOTION_REPLACEMENTS = {
    "너무 슬퍼서 아무 말도 할 수 없었다": "컵 가장자리를 엄지로 오래 문질렀다",
    "슬펐다": "시선을 컵 바닥에 오래 두었다",
    "분노했다": "봉투의 모서리를 손톱 밑으로 눌렀다",
    "화가 났다": "말끝을 삼키고 의자의 등받이를 밀었다",
    "두려웠다": "손바닥의 물기를 바지선에 문질렀다",
    "불안했다": "문고리 쪽으로 시선이 자꾸 갔다",
    "배신감을 느꼈다": "그의 이름이 적힌 봉투를 두 번 접었다",
}

class EmotionToBehaviorRenderer:
    def rewrite(self, text: str) -> str:
        out = text
        for src, dst in DIRECT_EMOTION_REPLACEMENTS.items():
            out = out.replace(src, dst)
        return out

    def direct_emotion_count(self, text: str) -> int:
        return sum(1 for src in DIRECT_EMOTION_REPLACEMENTS if src in text)
