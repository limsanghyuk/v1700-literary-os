# 드라마 분석 현재 권위 상태 — 2026-07-13

Status: **AUTHORITATIVE CURRENT SNAPSHOT**  
Project: 한국드라마04 / Literary OS Development  
Canonical policy: 사용자 승인 전 전 작품 `PASS_CANDIDATE`

## 1. 허브 최신 기준

조사 기준 저장소:

```text
limsanghyuk/v1700-literary-os
branch: main
latest drama authority commit:
555530412ddda6ab623102778e54c79db37156c9
```

해당 커밋은 7작품 authoritative v3 재감사·보강, 파라다이스목장 전 시즌 완결, 작품 카탈로그·상태표·세션 핸드오프 갱신을 기록한다.

대화 중간 체크포인트와 허브가 충돌하면 fresh extraction·내부 SHA·휴대형 validator가 확인된 허브 authoritative v3를 우선한다.

## 2. 완료된 7작품

| 순서 | 작품 | 회차 | SceneCard | Sequence | CharacterArc | RelationshipArc | LocalEdge | Payoff | Cross |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 101번째프로포즈 | 15 | 1,125 | 184 | 120 | 104 | 182 | 68 | 35 |
| 2 | 결혼못하는남자 | 16 | 1,250 | 189 | 89 | 92 | 128 | 38 | 13 |
| 3 | 공주가돌아왔다 | 16 | 1,117 | 160 | 147 | 152 | 477 | 94 | 33 |
| 4 | 시티헌터 | 20 | 1,356 | 171 | 156 | 153 | 463 | 140 | 55 |
| 5 | 내여자친구는구미호 | 16 | 793 | 105 | 96 | 80 | 128 | 80 | 55 |
| 6 | 좋은사람 | 16 | 938 | 114 | 99 | 96 | 128 | 80 | 55 |
| 7 | 파라다이스목장 | 16 | 939 | 120 | 80 | 80 | 128 | 80 | 55 |

누적:

```text
7작품
115회
7,518 SceneCard
1,043 SequenceBlueprint
115 EpisodeArc
787 CharacterArc
757 RelationshipArc
1,634 LocalEdge
580 PayoffCandidate
301 CrossEpisodeEdge
460 QuarterAudit
7 FullSeriesArc
```

## 3. 작품별 authoritative v3 패키지 SHA256

```text
101번째프로포즈
p101_stage01_04_authoritative_final_v3.zip
9fb78c7a95dcf775f70fbeaf99c5f218e5534380e92a27940ba4cec80c0da338

결혼못하는남자
kmn_stage01_04_authoritative_final_v3.zip
79a8641abab51eb0f8a72896be8b096474e2224589d374af3556c54bff142f06

공주가돌아왔다
princess_stage01_04_authoritative_final_v3.zip
f0c682369dfed99ea9eb8621b7ebe7823f127ea091acc5329bd303f2d3e6de93

시티헌터
cityhunter_stage01_04_authoritative_final_v3.zip
871e1abf26256b797e8813768b46423aa2c45afc091f73fd413ce1e23f370414

내여자친구는구미호
gumiho_stage01_04_authoritative_final_v3.zip
6d64412f088aa24303a85a0e27abd5d215295ac529692dd4bd06e7ec4a8adfb3

좋은사람
goodperson_stage01_04_authoritative_final_v3.zip
e5b8fa92f32172a348737d4d80d99e642cfc4832ca495a7104a74b58519589bd

파라다이스목장
paradise_stage01_04_authoritative_final_v3.zip
b5720d6074eae96840d4904065023873227f3eb3a6617b54f9c6339d67b58f50
```

## 4. 공통 검증 상태

```text
7/7 PASS_CANDIDATE_AUTHORITATIVE_V3
errors 0
warnings 0
```

각 패키지에서 확인한 항목:

- ZIP CRC
- 내부 `SHA256SUMS.txt`
- fresh extraction
- Stage01 exact 9-key 및 CORE16
- EpisodeMeta exact 5-key
- Stage02 exact 18-key, coverage, partition, runtime, density, core_mix
- EpisodeArc 13-key, structured turning point, act tiling
- CharacterArc trigger participant
- RelationshipArc 양쪽 participant
- LocalEdge 동일 회차·gap0·causal·target CORE
- PayoffCandidate 참조와 enum
- CrossEpisodeEdge forward-only·허용 3유형
- PayoffCandidate disposition 100%
- FullSeriesArc exact 17-key와 실제 count
- SourceLock v2
- 회차당 QuarterAudit 4개
- portable real validator
- raw script 미포함
- Python 의미 생성 없음

## 5. 주요 보강 이력

### 101번째프로포즈

- EpisodeMeta 15회 exact 5-key 정규화
- turn_type 59건 registry 교정
- 회차 간 LocalEdge 3건 제거·boundary evidence 보존

### 결혼못하는남자

- EpisodeMeta 16회 정규화
- turn_type 80건 교정
- runtime_share 13회차 합계 1.0 보정
- 회차 간 LocalEdge 6건 제거

### 공주가돌아왔다

- runtime_share 1회차 정밀 보정
- 회차 간 LocalEdge 22건 제거

### 시티헌터·내여자친구는구미호·좋은사람

- 의미 데이터 변경 없음
- SourceLock·QuarterAudit·공통 validator·fresh extraction 증빙 통일

### 파라다이스목장

- EP09~EP16 460장면 직접독해 및 Stage01 완료
- 후반부 SequenceBlueprint 59건과 Stage03 완료
- 전 시즌 939장면 / 120 SequenceBlueprint
- PayoffCandidate 80건 전수 disposition
- CrossEpisodeEdge 55건
- FullSeriesArc 및 기능 holdout 12/12

## 6. 최신 방법론 핵심

```text
원본 → SourceLock → Stage01 → Stage02 → Stage03 → Stage04
```

운영 단위:

```text
의미 저작: quarter
잠금: episode
사용자 제출: half-season
안전 축소: two episodes
최종 통합: full series
```

Python 허용:

```text
추출·인코딩 복원·경계 탐지·해시·직렬화·검증·패키징
```

Python 금지:

```text
장면 의미·시퀀스 의미·인물/관계 아크·인과·복선·Stage04 생성
```

## 7. 문서 드리프트 감사

2026-07-13 조사에서 다음 과거 5작품 표기를 발견해 갱신했다.

- `GPT_CLAUDE_ALIGNMENT_AND_INGESTION_V1.md` 수용 목록
- `NEXT_SESSION_BOOTSTRAP_CHECKLIST.md` 완료·제외 목록
- `results/README.md` 패키지·결과 인덱스

`FULL_SERIES_SYNTHESIS_5_WORKS_2026-07-12.md`는 최초 5작품 의미 종합인 historical subset으로 보존한다.

## 8. 다음 정확한 진입점

```text
SELECT_NEXT_UNANALYZED_WORK_FROM_한국드라마04
→ SOURCE_ARCHIVE_INVENTORY
→ 완료 7작품 제외
→ 후보 원본·인코딩·scene boundary·반시즌 균형 평가
→ 1작품 선정
→ SourceLock v2
→ EP01 Q1 직접독해
```

새 세션은 파라다이스목장 후반부를 다시 시작하지 않는다. 허브 authoritative v3에서 이미 전 시즌 완료됐다.

## 9. 새 대화창 전달문

```text
개발자 허브 limsanghyuk/v1700-literary-os의 docs/drama_analysis/README.md와 CURRENT_AUTHORITY_SNAPSHOT_2026-07-13.md를 먼저 읽어라.
7작품 authoritative v3 상태와 WORK_STATUS를 우선하고, 완료 작품 7편을 신규 선정에서 제외하라.
운영 설명서·스키마·검증 프로토콜을 로드한 뒤 한국드라마04의 다음 미분석 작품을 선정하여 SourceLock v2를 만들고 EP01 Q1부터 직접독해하라.
Python은 추출·직렬화·검증·패키징에만 사용하고 의미 생성에 사용하지 마라.
```
