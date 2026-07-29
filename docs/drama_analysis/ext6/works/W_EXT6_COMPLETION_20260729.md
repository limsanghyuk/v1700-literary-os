# W EXT6 V1.2 완료 기록

- 작품: `W`
- 회차: 16
- 처리 방식: `EXT6_EVIDENCE_FIRST` → 원문 직접 감사 → `SELECTIVE_APPEND`
- 상태: `PASS_CANDIDATE_EXT6_SELECTIVE_REINFORCEMENT_COMPLETE`
- 기존 Stage01·02·04 변경: 0
- 기존 Stage03 레코드 덮어쓰기·삭제: 0

## EXT6 증거층

- SceneCard / SourceSceneAlignment: 1,220 / 1,220
- 미해결 정렬: 0
- CastPresence: 3,063
- CharacterLoad: 375
- EntityBridge: 44
- 출연 주석 장면: 1,171
- 정당한 빈 장면: 49

## 위험도 감사와 선택 보강

- 후보: 30
- 채택: 18
- 기각: 12
- 미결: 0
- CharacterArc: 76 → 86, 10건 추가
- RelationshipArc: 61 → 69, 8건 추가

주요 보강은 서도윤의 비밀 탈출 공모·연락책·유산 수탁, 박수봉의 세계 법칙 수용, 손현석의 단서 발견·피살, 오성무–진범의 침식·강제 융합, 윤소희의 기억 의존적 재소환이다. 단순 직무 수행·회상·공동 등장만 존재한 후보는 기각했다.

## 검증

- EXT6 독립검증: PASS
- 현행 구조검사: PASS
- 현행 의미검사: PASS
- Functional Holdout: PASS
- Fresh Extraction: PASS
- ZIP CRC 및 내부 SHA-256: PASS

Holdout Recall@5:

- 핵심 질문: 1.0 → 1.0
- 결손 질문: 0.0 → 1.0
- 전체: 0.3571 → 1.0

## 개발자 패키지

- 파일명: `W_EXT6_V1_2_INDIVIDUAL_PACKAGE_20260729.zip`
- SHA-256: `e98da25d08e1536fe95150c1e4f73a68c79defaec2f24280bd13ee6eb2f10fc7`
- 파일 수: 284
- 다음 작품: `강남엄마따라잡기`

대용량 ZIP은 저장소에 커밋하지 않고 작품별 결과·검증값·SHA-256만 허브에 기록한다.
