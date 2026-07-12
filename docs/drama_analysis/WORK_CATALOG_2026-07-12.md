# GPT 드라마 분석 작품 카탈로그 — 2026-07-12 authoritative v3

Status: **PASS_CANDIDATE CATALOG**  
Authority: 실제 authoritative v3 ZIP, fresh extraction, 내부 SHA, 휴대형 validator 결과를 우선함

## 1. 전체 누적

| 항목 | 합계 |
|---|---:|
| 작품 | **7** |
| 회차 | **115** |
| SceneCard | **7,518** |
| SequenceBlueprint | **1,043** |
| EpisodeArc | 115 |
| CharacterArc | **787** |
| RelationshipArc | **757** |
| LocalEdge | **1,634** |
| PayoffCandidate | **580** |
| CrossEpisodeEdge | **301** |
| FullSeriesArc | 7 |
| QuarterAudit | **460** |

모든 작품은 사용자 최종 승인 전이므로 `PASS_CANDIDATE`다. `CANONICAL`은 사용하지 않는다.

## 2. 작품별 authoritative v3

| 순서 | 작품 | 회차 | SceneCard | Sequence | Local | Cross | 패키지 SHA256 |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | 101번째프로포즈 | 15 | 1,125 | 184 | 182 | 35 | `9fb78c7a95dcf775f70fbeaf99c5f218e5534380e92a27940ba4cec80c0da338` |
| 2 | 결혼못하는남자 | 16 | 1,250 | 189 | 128 | 13 | `79a8641abab51eb0f8a72896be8b096474e2224589d374af3556c54bff142f06` |
| 3 | 공주가돌아왔다 | 16 | 1,117 | 160 | 477 | 33 | `f0c682369dfed99ea9eb8621b7ebe7823f127ea091acc5329bd303f2d3e6de93` |
| 4 | 시티헌터 | 20 | 1,356 | 171 | 463 | 55 | `871e1abf26256b797e8813768b46423aa2c45afc091f73fd413ce1e23f370414` |
| 5 | 내여자친구는구미호 | 16 | 793 | 105 | 128 | 55 | `6d64412f088aa24303a85a0e27abd5d215295ac529692dd4bd06e7ec4a8adfb3` |
| 6 | 좋은사람 | 16 | 938 | 114 | 128 | 55 | `e5b8fa92f32172a348737d4d80d99e642cfc4832ca495a7104a74b58519589bd` |
| 7 | 파라다이스목장 | 16 | 939 | 120 | 128 | 55 | `b5720d6074eae96840d4904065023873227f3eb3a6617b54f9c6339d67b58f50` |

패키지명:

```text
p101_stage01_04_authoritative_final_v3.zip
kmn_stage01_04_authoritative_final_v3.zip
princess_stage01_04_authoritative_final_v3.zip
cityhunter_stage01_04_authoritative_final_v3.zip
gumiho_stage01_04_authoritative_final_v3.zip
goodperson_stage01_04_authoritative_final_v3.zip
paradise_stage01_04_authoritative_final_v3.zip
```

## 3. 순차 보강 결과

### 101번째프로포즈

- EpisodeMeta 15회 exact 5-key 정규화
- 비권위 turn_type 59건을 registry 값으로 교정
- 회차 간 causal bridge 3건을 LocalEdge에서 제거하고 boundary evidence로 보존
- 최종: `PASS_CANDIDATE_AUTHORITATIVE_V3`, errors 0, warnings 0

### 결혼못하는남자

- EpisodeMeta 16회 exact 5-key 정규화
- 비권위 turn_type 80건 교정
- runtime_share 13회차 합계 1.0 보정
- 회차 간 causal bridge 6건을 LocalEdge에서 제거
- 최종: `PASS_CANDIDATE_AUTHORITATIVE_V3`, errors 0, warnings 0

### 공주가돌아왔다

- runtime_share 1회차 정밀 보정
- 회차 간 causal bridge 22건을 LocalEdge에서 제거
- 최종: `PASS_CANDIDATE_AUTHORITATIVE_V3`, errors 0, warnings 0

### 시티헌터·내여자친구는구미호·좋은사람

- 의미 데이터 변경 없음
- SourceLock v2, episode×4 QuarterAudit, 공통 권위 validator와 fresh-extraction 증빙을 통일
- 최종: 3작품 모두 errors 0, warnings 0

### 파라다이스목장

- EP09~EP16 460장면 직접독해·SceneCard 저작 완료
- 후반부 SequenceBlueprint 59건 및 Stage03 렛저 완료
- 전 시즌 939장면 / 120 SequenceBlueprint
- PayoffCandidate 80건 전수 disposition
- CrossEpisodeEdge 55건 승격
- FullSeriesArc 및 기능 holdout 12/12 완료
- 최종: `PASS_CANDIDATE_FULL_SERIES_STAGE01_04`, errors 0, warnings 0

## 4. 공통 최종 감사

7개 ZIP을 별도 경로에 다시 풀어 다음을 일괄 검사했다.

- ZIP CRC
- 내부 `SHA256SUMS.txt`
- Stage01 exact 9-key, CORE16, ordinal coverage
- EpisodeMeta exact 5-key
- Stage02 exact 18-key, turn registry, value_shift, coverage, runtime, density, core_mix
- EpisodeArc, CharacterArc, RelationshipArc 참조
- LocalEdge 동일 회차·gap0·causal
- CrossEpisodeEdge forward-only 및 허용 3유형
- FullSeriesArc exact 17-key와 집계
- SourceLock 및 회차당 4개 QuarterAudit
- 휴대형 validator 재실행

결과:

```text
7/7 PASS_CANDIDATE_AUTHORITATIVE_V3
errors 0
warnings 0
```

## 5. 보존·배포 규칙

대용량 ZIP 자체는 문서 저장소에 중복 커밋하지 않는다. 새 세션 또는 로컬 개발자는 반드시 파일명만 믿지 말고 다음 순서로 검증한다.

1. 카탈로그 SHA256 대조
2. ZIP CRC
3. fresh extraction
4. 내부 SHA 전수 확인
5. 휴대형 validator 실행
6. JSONL 실제 레코드 수 재집계

## 6. 다음 작품 선정 제외 목록

```text
101번째프로포즈
결혼못하는남자
공주가돌아왔다
시티헌터
내여자친구는구미호
좋은사람
파라다이스목장
```

다음 정상 진입점은 `한국드라마04` archive inventory 후 위 7작품을 제외한 작품 선정과 `EP01 Q1` 직접독해다.
