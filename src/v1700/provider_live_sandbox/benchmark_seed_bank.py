from __future__ import annotations

def default_seed_bank() -> list[dict]:
    return [
        {'seed_id':'seed_001','genre':'literary_thriller','prompt':'전직 기상청 예보관이 서울 변두리 폐역에서 잃어버린 동생의 실종일을 전광판에서 다시 본다. Feature-only premise only.'},
        {'seed_id':'seed_002','genre':'family_mystery','prompt':'장례식 전날 가족 중 한 명만 기억하지 못하는 여름 폭우 사건의 단서를 정리한다. Feature-only premise only.'},
        {'seed_id':'seed_003','genre':'scenario_suspense','prompt':'32부작 드라마 8화에서 주인공이 과거 예보 오류와 현재 집단 실종 사건의 연결을 발견한다. Feature-only premise only.'},
    ]

def modes() -> tuple[str, str]:
    return ('PROSE','SCENARIO')
