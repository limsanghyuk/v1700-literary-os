# GPT 드라마 분석 작품 카탈로그 — 2026-07-12

Status: PASS_CANDIDATE CATALOG  
Authority: 실제 ZIP 내부 레코드 수와 최신 validation report를 우선함

## 1. 전체 누적

| 항목 | 합계 |
|---|---:|
| 작품 | 5 |
| 회차 | 83 |
| SceneCard | **5,641** |
| SequenceBlueprint | **809** |
| EpisodeArc | 83 |
| CharacterArc | **608** |
| RelationshipArc | **581** |
| LocalEdge | **1,409** |
| PayoffCandidate | **420** |
| CrossEpisodeEdge | **191** |
| FullSeriesArc | 5 |

현재 모든 작품은 사용자 최종 canonical 승인 전이므로 `PASS_CANDIDATE`다.

## 2. 작품별 결과

### 2.1 101번째프로포즈

```text
episodes: 15
scenes: 1,125
sequences: 184
character_arcs: 120
relationship_arcs: 104
local_edges: 185
payoff_candidates: 68
cross_episode_edges: 35
```

패키지:

```text
p101_stage01_04_repaired_final_v2(1).zip
SHA256 c02c65501b89743c630d9f4f4a86c8d57627d48d5e8fd68236dff0589f02c767
ZIP CRC PASS
```

검증:

```text
PASS_CANDIDATE — ERRORS 0
errors 0
warnings 0
```

주요 보강:

- work_id·seq_id 정규화
- Stage02 turn registry 보정
- turning_point 구조화
- 인물명 정규화
- Local/Cross 계층 정리
- 이전 실패 감사 이력 보존

### 2.2 결혼못하는남자

```text
episodes: 16
scenes: 1,250
sequences: 189
character_arcs: 89
relationship_arcs: 92
local_edges: 134
payoff_candidates: 38
cross_episode_edges: 13
```

패키지:

```text
kmn_stage01_04_source_repaired_final_v2(1).zip
SHA256 8abe6b3ba45e0aabe0925739dfe5adbfc37a7c7fe7bc4f4c1e7868eeee6bacde
ZIP CRC PASS
```

최신 검증:

```text
PASS_CANDIDATE — ERRORS 0
errors 0
warnings 0
```

중요 정정:

패키지 안에는 1,249장면을 기준으로 한 과거 strong-gate 보고서와 실패 이력이 남아 있다. 현재 실제 `authored/*.seqcard.jsonl` 전수 집계와 `validation_v2/FINAL_VALIDATION_REPORT.json`은 **1,250장면 / LocalEdge 134 / Payoff 38 / Cross 13**이다. 1,249장면 보고서는 history/superseded 자료로 취급한다.

주요 보강:

- source mismatch 복구
- Stage01/02 Claude 계약 정규화
- Stage03 인물×회차·관계쌍×회차 재저작
- trigger participant 및 core_mix 보정
- Stage04 fan-in 재확정

### 2.3 공주가돌아왔다

```text
episodes: 16
scenes: 1,117
sequences: 160
character_arcs: 147
relationship_arcs: 152
local_edges: 499
payoff_candidates: 94
cross_episode_edges: 33
```

패키지:

```text
princess_stage01_04_full_series_repaired_final_v2(1).zip
SHA256 48c861ad1e414ceeafff438af038585f3faa38ab66d43a3bbbb8d80729dad3e5
ZIP CRC PASS
```

검증:

```text
PASS_CANDIDATE_FULL_SERIES_REPAIRED_V2
errors 0
warnings 0
canonical_allowed false
```

주요 보강:

- 518개 반복 규약 결함 교정
- work_id·seq_id 전량 정규화
- turn_type 35건 정규화
- EpisodeArc turning_point 16건 구조화
- real validator로 stub 교체
- 64 quarter audit 재생성
- 12문항 holdout 분리 실행

### 2.4 시티헌터

```text
episodes: 20
scenes: 1,356
sequences: 171
character_arcs: 156
relationship_arcs: 153
local_edges: 463
payoff_candidates: 140
cross_episode_edges: 55
candidate_dispositions: 140
```

패키지:

```text
cityhunter_stage01_04_full_series_final_v1.zip
SHA256 8c895241875bbb096188fe834daefc6ccfb20e8ae91743e6153ebcf50e05cc37
ZIP CRC PASS
```

검증:

```text
PASS_CANDIDATE_FULL_SERIES_STAGE01_04
errors 0
warnings 0
functional holdout 12/12 PASS_LIMITED_NONBLINDED
```

분석 방식:

- 20회 1,356장면 직접독해
- EP01~10 전반부 / EP11~20 후반부
- 각 회차 Q1→Q4
- PayoffCandidate 140건 전수 disposition
- Stage04 55건 승격

### 2.5 내여자친구는구미호

```text
episodes: 16
scenes: 793
sequences: 105
character_arcs: 96
relationship_arcs: 80
local_edges: 128
payoff_candidates: 80
cross_episode_edges: 55
candidate_dispositions: 80
```

패키지:

```text
gumiho_stage01_04_full_series_final_v1.zip
SHA256 66499cceff00561a3b4441b07cb64e88921215e8492c7983f78d51fdc748194d
ZIP CRC PASS
```

검증:

```text
PASS_CANDIDATE_FULL_SERIES_STAGE01_04
errors 0
warnings 0
functional holdout 12/12 PASS_LIMITED_NONBLINDED
```

분석 방식:

- 원본 scene marker가 없어 빈 줄 의미 블록을 canonical scene으로 잠금
- EP01~08 전반부 / EP09~16 후반부
- 793장면 직접독해
- 후보 80건 전수 disposition
- Stage04 55건 승격

## 3. Claude 수용 상태

Claude의 재평가 문서에 따르면 앞의 4작품(101번째프로포즈, 결혼못하는남자, 공주가돌아왔다, 시티헌터)은 규약 보정과 이중 게이트 후 Claude 코퍼스 수용 대상으로 인정됐다.

정정된 결론:

- 오분석 드라마 지적은 오탐
- 대규모 dangling scene 지적은 오탐
- 실제 의미 내용은 수용 가능
- 핵심 수정 대상은 LocalEdge/CrossEpisodeEdge 계층 분리와 일부 ID·turning_point 정규화

내여자친구는구미호는 그 합의 이후 동일 v2 규격으로 신규 분석됐다.

## 4. 보존·배포 주의

이 카탈로그는 세션에서 전달된 최종 ZIP의 파일명과 SHA256을 기록한다. 대용량 binary ZIP 자체를 이 문서 디렉터리에 중복 커밋하지 않는다.

새 세션 또는 로컬 개발자가 패키지를 다시 받을 때:

1. 파일명이 같아도 SHA256을 확인한다.
2. ZIP CRC를 검사한다.
3. fresh extraction에서 실제 validator를 실행한다.
4. `SHA256SUMS.txt`를 전수 확인한다.
5. 카탈로그 count와 실제 JSONL 레코드 수를 다시 계산한다.

## 5. 다음 작품 선정 제외 목록

한국드라마04에서 다음 작품은 신규 선정 대상에서 제외한다.

```text
101번째프로포즈
결혼못하는남자
공주가돌아왔다
시티헌터
내여자친구는구미호
```

동일 작품을 다시 선택하려면 신규 분석이 아니라 기존 패키지의 독립 재감사·보강·비교 실험으로 명시해야 한다.
