# 2026-07-15 드라마 분석·데이터베이스 통합 작업 핸드오프

- Session status: `INTEGRATED_VALIDATED_PROGRESS`
- Timezone: Asia/Seoul
- Database lineage: `seqcard_ko(3).zip` → 칼잡이오수정 삽입 → W 업그레이드 → 드림/강남엄마따라잡기 삽입 → 경성스캔들 → 미안하다사랑한다 → 밀회
- EXT6: 기본 보류, 오늘 데이터베이스 작업에는 적용하지 않음

## 1. 오늘 확정한 운영 원칙

1. Stage01~04 exact schema는 `SCHEMA_CONTRACTS_V2.md` 유지.
2. 회차별 Q1→Q4 직접독해와 회차 체크포인트를 지킨다.
3. 개발자 전달·데이터베이스 작업 블록은 8회차 단위로 계획한다.
4. 전 회차 Stage01~03 강검증을 통과한 뒤에만 Stage04로 이동한다.
5. 기존 Stage04 완료작과 교차품질 검증은 기본 필수 게이트가 아니다.
6. 작품 품질은 원본 근거·내용 깊이·반복성·스키마·참조·Stage04 후보 처분으로 내부 검증한다.
7. 독립 작품 ZIP과 갱신된 `seqcard_ko` 전체 DB ZIP을 함께 제공한다.
8. 원본은 로컬/개발자용 `original_extracted`에 저장하되 GitHub 허브에는 raw script를 올리지 않는다.
9. EXT6은 별도 sidecar로 보류한다.

## 2. 칼잡이오수정 신규 분석

### 범위

- 16회
- 회차별 4분할 직접독해
- Stage01~03 전반부/후반부 체크포인트
- Stage04 후보 245건 전수 재심사
- 장면 정렬·참여자·인물키·자동 브리지 보강

### 최종 레코드

| 계층 | 수량 |
|---|---:|
| SceneCard | 1,137 |
| SequenceBlueprint | 139 |
| EpisodeArc | 16 |
| CharacterArc | 122 |
| RelationshipArc | 130 |
| LocalEdge | 386 |
| PayoffCandidate | 245 |
| CrossEpisodeEdge | 71 |
| CandidateDisposition | 245 |
| CandidateReviewEvidence | 245 |
| QuarterAudit | 64 |
| FullSeriesArc | 1 |

### 주요 보강

- EP07 S40~S59 원본 재독해·정렬 복구
- EP14 S63~S71 절도–가출–공항행 연쇄 정렬 복구
- Stage03 trigger participant 교정
- 인물키 `정우탁 / 서재윤 / 윤동관` 통일
- 자동 회차 경계 브리지 5건 제거
- 후보별 고유 review evidence 작성

### 산출물

```text
칼잡이오수정_stage01_04_full_series_repaired_pass_candidate_v2.zip
SHA256 e561beb609e658e9853204865614b0270075874b39f0bf6a2b61e135c7da1218
```

초기 46작품 표준 데이터베이스에 삽입하여 47작품으로 갱신했다.

## 3. 완결 분석본 직접 삽입

### 드림

| 항목 | 수량 |
|---|---:|
| 회차 | 20 |
| SceneCard | 1,180 |
| SequenceBlueprint | 145 |
| CharacterArc | 112 |
| RelationshipArc | 89 |
| LocalEdge | 158 |
| PayoffCandidate | 100 |
| CrossEpisodeEdge | 72 |

```text
dream_ep01_20_full_series_direct_reauthored_v2(1).zip
SHA256 dd404d83257760f0d15eacbd16d7896734d3a536e09e96b09e94aa9431607983
```

### 강남엄마따라잡기

| 항목 | 수량 |
|---|---:|
| 회차 | 18 |
| SceneCard | 1,246 |
| SequenceBlueprint | 154 |
| CharacterArc | 105 |
| RelationshipArc | 90 |
| LocalEdge | 152 |
| PayoffCandidate | 98 |
| CrossEpisodeEdge | 60 |

```text
gangnam_mom_ep01_18_full_series_direct_reauthored_v2(1).zip
SHA256 d7bff33ceec270159e2cc1a532f45c3c3ca722b3c869b0d9e4a0172738a9f0e9
```

두 작품을 삽입한 뒤 데이터베이스는 49작품으로 확장됐다.

## 4. 기존 Stage01~03 작품의 Stage04 업그레이드

### W·더블유

| 계층 | 수량 |
|---|---:|
| 회차 | 16 |
| SceneCard | 1,220 |
| SequenceBlueprint | 203 |
| CharacterArc | 76 |
| RelationshipArc | 61 |
| LocalEdge | 119 |
| PayoffCandidate | 57 |
| CrossEpisodeEdge | 49 |

주요 작업:

- 구형 turn_type 135건 정규화
- runtime_share 174건 합계 1.0 보정
- Stage03 trigger·직접 상호작용 검증
- 후보 57건 전수 처분
- 원본 16회 `original_extracted` 편입

```text
W_stage01_04_upgraded_full_series_v1.zip
SHA256 3970923a69c196686a655bac625d393111353428d245e60ab7575c6507ac5f00
```

### 경성스캔들

| 계층 | 수량 |
|---|---:|
| 회차 | 16 |
| SceneCard | 1,187 |
| SequenceBlueprint | 150 |
| CharacterArc | 64 |
| RelationshipArc | 64 |
| LocalEdge | 96 |
| PayoffCandidate | 64 |
| CrossEpisodeEdge | 52 |

주요 작업:

- 원본 16회 장면 정렬 재검증
- Stage02 밀도 미달 구간 재분절: 138→150
- turn_type/core_mix/runtime_share 정규화
- 후보 64건 전수 처분

```text
경성스캔들_stage01_04_upgraded_full_series_v1.zip
SHA256 8160135dd048f6c589006b249ddd5a76d2b5e5348f7a1a7f742e2c8a298dcabe
```

### 미안하다사랑한다

| 계층 | 수량 |
|---|---:|
| 회차 | 16 |
| SceneCard | 1,299 |
| SequenceBlueprint | 192 |
| CharacterArc | 64 |
| RelationshipArc | 63 |
| LocalEdge | 96 |
| PayoffCandidate | 64 |
| CrossEpisodeEdge | 43 |

주요 작업:

- EpisodeArc 현행 규격 정규화
- 인물명 `최윤민주 → 민주` 통일
- 관계 trigger/evidence 11건 교정
- 유효 상호작용 없는 관계 1건 제거
- 후보 64건 전수 처분

```text
미안하다사랑한다_stage01_04_upgraded_full_series_v1.zip
SHA256 4ea4cf68855d1c6678f85a36b5aa11b31dcd12ce89cab40461a42b957e6dc93f
```

### 밀회

| 계층 | 수량 |
|---|---:|
| 회차 | 16 |
| SceneCard | 1,144 |
| SequenceBlueprint | 147 |
| CharacterArc | 48 |
| RelationshipArc | 47 |
| LocalEdge | 82 |
| PayoffCandidate | 64 |
| CrossEpisodeEdge | 58 |

주요 작업:

- EP12·EP15·EP16 시퀀스 밀도 미달 재분절
- 구형 turn_type/core_mix/runtime_share 정규화
- CharacterArc trigger 2건, RelationshipArc trigger 2건 교정
- 직접 상호작용 없는 관계 1건 제거
- 후보 64건 전수 처분

```text
밀회_stage01_04_upgraded_full_series_v1.zip
SHA256 70905d4d721baf421231bca1917f379ff2b0333e2839478cc8dda409c7f619e9
```

## 5. 현재 전체 데이터베이스

```text
파일: seqcard_ko_stage04_progress_W_dream_gangnam_gyeongseong_misa_milhwe_v1.zip
SHA256: fbcff3f8d184d4d36a4364fe8caca14b3591ae0c8b64b07ebccfaf2564b3ad6c
상태: INTEGRATED_VALIDATED_PROGRESS
```

| 항목 | 현재 수량 |
|---|---:|
| 작품 | 49 |
| 회차 | 938 |
| SceneCard | 58,945 |
| Stage01~04 완료 | 34 |
| Stage04 업그레이드 잔여 | 15 |
| 잔여 회차 | 364 |
| 잔여 SceneCard | 23,090 |

오늘 신규 삽입:

```text
칼잡이오수정
드림
강남엄마따라잡기
```

오늘 업그레이드:

```text
W
경성스캔들
미안하다사랑한다
밀회
```

## 6. 잔여 15작품

| 작품 | 회차 | SceneCard | 원본 상태 |
|---|---:|---:|---|
| 공주의남자 | 24 | 1,784 | 데이터베이스 내 원본 있음 |
| 궁 | 24 | 1,089 | 데이터베이스 내 원본 있음 |
| 녹두꽃 | 24 | 1,636 | 데이터베이스 내 원본 있음 |
| 뉴하트 | 23 | 1,238 | 원본 ZIP 수신, DB 미편입 |
| 대장금 | 54 | 3,630 | 데이터베이스 내 원본 있음 |
| 더킹투하츠 | 20 | 1,110 | 원본 ZIP 수신, DB 미편입 |
| 마왕 | 20 | 1,585 | 데이터베이스 내 원본 있음 |
| 모래시계 | 24 | 1,365 | 데이터베이스 내 원본 있음 |
| 스카이캐슬 | 20 | 1,353 | 데이터베이스 내 원본 있음 |
| 싸인 | 20 | 1,358 | 데이터베이스 내 원본 있음 |
| 역전의여왕 | 31 | 1,875 | 데이터베이스 내 원본 있음 |
| 최강칠우 | 20 | 1,398 | 데이터베이스 내 원본 있음 |
| 카인과아벨 | 20 | 1,080 | 데이터베이스 내 원본 있음 |
| 킬미힐미 | 20 | 1,285 | 원본 ZIP 수신, DB 미편입 |
| 하얀거탑 | 20 | 1,304 | 데이터베이스 내 원본 있음 |

수신 원본 SHA256:

```text
뉴하트.zip
5e6ef9594ea618e7097b9f318c170136e1e81ef610cff7690ee6651f142897d3

더킹투하츠.zip
3d7f92c8ed880d9b780237435ffa57eaf0fe032dd6a0836c09d44876dc66f3bc

킬미힐미.zip
888d4992bbd92ddb6379eb86c5dfe9c99235423bc9d3d476b850f5be1f491aff
```

## 7. 검증 공통 결과

오늘 생성·업그레이드한 독립 작품 패키지와 누적 데이터베이스는 다음을 수행했다.

- exact schema·enum·type
- Stage02 coverage·partition·runtime·density·core_mix
- Stage03 trigger participant·pair·LocalEdge target core
- PayoffCandidate 전수 disposition
- CrossEpisodeEdge 방향·gap·type·target core
- 자동 회차 경계 브리지 검사
- 의미문 정확·골격 반복 검사
- ZIP CRC
- 내부 SHA256SUMS
- fresh extraction 후 휴대형 validator 재실행

모든 현재 잠금 작품은 `PASS_CANDIDATE`이며 사용자 승인 전 `CANONICAL`로 승격하지 않았다.

## 8. 다음 재진입 지점

```text
DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json 로드
→ 잔여 15작품 중 1편 선정
→ 원본/기존 Stage01·02·EpisodeArc 검증
→ 회차별 Stage03 보완
→ 전 작품 Stage01~03 강검증
→ Stage04 후보 전수 fan-in
→ 독립 작품 ZIP
→ seqcard_ko 전체 DB ZIP 갱신
```

EXT6은 기본 비활성으로 유지한다.
