# 2026-07-12 드라마 분석 세션 핸드오프

Status: COMPLETE HANDOFF  
Owner project: Literary OS Development / V1700 Literary OS  
Next action: 한국드라마04의 다음 미분석 작품 선정

## 1. 이 세션의 목적과 결과

이 세션에서는 다음을 수행했다.

1. GPT 분석 3작품과 Claude `seqcard_ko` 코퍼스를 객관 비교
2. 분석 확장 단위를 검토하고 반시즌 제출 방식 확정
3. `시티헌터` 20회 1,356장면 Stage01~04 완성
4. `내여자친구는구미호` 16회 793장면 Stage01~04 완성
5. Claude가 GPT 이전 4작품을 재평가·수용한 제안서 분석
6. GPT–Claude 규격 일치화와 편입 규칙 확정
7. 새 대화창에서 바로 분석 가능한 v2 문서군 작성

## 2. GPT–Claude 비교 결론

동일 작품이 없던 초기 비교에서는 다음과 같이 판정했다.

```text
단일 작품 Stage01~04 완결성: GPT 우세
대규모 코퍼스·장르 다양성: Claude 우세
Stage02 고유 goal/obstacle: GPT 우세
작성된 Stage03/04 evidence 길이: Claude 우세
SourceLock·quarter audit·portable validator: GPT 우세
```

이후 Claude가 GPT 4작품을 직접 감사한 결과 초기 오탐을 정정했다.

- 작품명·내용 불일치 아님
- dangling scene 대량 발생 아님
- GPT 의미 분석은 수용 가능
- 실제 핵심 결함은 일부 회차 간 edge를 LocalEdge에 둔 계층 배치 문제

최종 합의:

```text
공통 Stage01~04 스키마
+ Claude 직접독해·반게이밍 규율
+ GPT SourceLock·QuarterAudit·Lineage·FunctionalHoldout·portable validator
```

## 3. 분석 확장 방식 결정

사용자는 한 작품 전체를 반으로 나누어 분석할 수 있는지 질문했다.

최종 운영:

```text
의미 저작 = quarter
잠금 = episode
사용자 제출 = half-season
전체 통합 = full series
```

반시즌은 자동 대량 생성 단위가 아니다. 각 회차 Q1→Q4를 순차 잠그고 전반부 전체가 끝날 때 한 번 제출한다.

### 과거 중단 원인

`시티헌터` EP01 완료 후 내부 회차 체크포인트를 사용자 제출 완료처럼 보고하고 멈췄다. 이후 EP02~EP08 진행에서도 개별 약한 validator와 사후 포장이 섞였다.

확인된 결함:

- EP02 비표준 CORE 6건
- EP02·EP03 sequence density 미달
- source marker와 canonical ordinal 혼동
- CORE 교정 뒤 LocalEdge label 미갱신
- 회차별 validator 규칙 편차

해결:

- 마지막 신뢰 경계를 재확인
- EP02·EP03 시퀀스 재분절
- trigger ordinal 원문 재대조
- 전반부 전체 단일 validator
- 내부 회차 PASS와 사용자 제출 분리

이 교훈은 v2 운영 설명서와 검증 프로토콜에 반영됐다.

## 4. 시티헌터 결과

### Source

```text
episodes 20
scenes 1,356
first half EP01~10: 690
second half EP11~20: 666
```

원본 S#에는 중복·결번·역순이 있어:

```text
canonical scene_no = marker 등장 순서 ordinal
source_marker = 원본 번호 보존
```

### Final counts

```text
SceneCard 1,356
SequenceBlueprint 171
EpisodeArc 20
CharacterArc 156
RelationshipArc 153
LocalEdge 463
PayoffCandidate 140
CrossEpisodeEdge 55
CandidateDisposition 140
FullSeriesArc 1
```

### Stage04 disposition

```text
promoted 55
reclassified local/adjacent causal 13
resolved within episode 10
rejected insufficient evidence 60
rejected source mismatch 2
unprocessed 0
```

### Validation

```text
PASS_CANDIDATE_FULL_SERIES_STAGE01_04
errors 0
warnings 0
functional holdout 12/12 PASS_LIMITED_NONBLINDED
```

### Package

```text
cityhunter_stage01_04_full_series_final_v1.zip
SHA256 8c895241875bbb096188fe834daefc6ccfb20e8ae91743e6153ebcf50e05cc37
```

## 5. 내여자친구는구미호 결과

### Selection reason

- 16회 완전 분리
- 판타지 로맨스로 장르 확장
- Claude 동일 작품 비교 가능
- 시티헌터 이후 정치 액션 편향 보완

### Scene boundary

원본에 scene marker가 없어 빈 줄로 분리된 의미 블록을 canonical scene ordinal로 잠갔다. 첫 원문 행/heading hash를 provenance로 보존했다.

```text
episodes 16
scenes 793
first half EP01~08: 351
second half EP09~16: 442
```

### Final counts

```text
SceneCard 793
SequenceBlueprint 105
EpisodeArc 16
CharacterArc 96
RelationshipArc 80
LocalEdge 128
PayoffCandidate 80
CrossEpisodeEdge 55
CandidateDisposition 80
FullSeriesArc 1
```

### Stage04 disposition

```text
promoted 55
rejected duplicate 11
rejected insufficient evidence 5
reclassified adjacent/local 2
resolved within/final episode 7
source ordinal repairs 3
unprocessed 0
```

### Validation

```text
PASS_CANDIDATE_FULL_SERIES_STAGE01_04
errors 0
warnings 0
functional holdout 12/12 PASS_LIMITED_NONBLINDED
```

### Package

```text
gumiho_stage01_04_full_series_final_v1.zip
SHA256 66499cceff00561a3b4441b07cb64e88921215e8492c7983f78d51fdc748194d
```

## 6. 이전 보강 3작품

### 101번째프로포즈

```text
15 episodes / 1,125 scenes / 184 sequences
120 char / 104 rel / 185 local / 68 payoff / 35 cross
package SHA256 c02c65501b89743c630d9f4f4a86c8d57627d48d5e8fd68236dff0589f02c767
PASS_CANDIDATE — ERRORS 0
```

### 결혼못하는남자

```text
16 episodes / 1,250 current scenes / 189 sequences
89 char / 92 rel / 134 local / 38 payoff / 13 cross
package SHA256 8abe6b3ba45e0aabe0925739dfe5adbfc37a7c7fe7bc4f4c1e7868eeee6bacde
PASS_CANDIDATE — ERRORS 0
```

주의: 패키지 history에 1,249장면 구판 보고서가 남아 있다. 현재 실제 authored count와 validation_v2는 1,250장면이다.

### 공주가돌아왔다

```text
16 episodes / 1,117 scenes / 160 sequences
147 char / 152 rel / 499 local / 94 payoff / 33 cross
package SHA256 48c861ad1e414ceeafff438af038585f3faa38ab66d43a3bbbb8d80729dad3e5
PASS_CANDIDATE_FULL_SERIES_REPAIRED_V2
```

## 7. 전체 누적

```text
5 works
83 episodes
5,641 SceneCards
809 SequenceBlueprints
608 CharacterArcs
581 RelationshipArcs
1,409 LocalEdges
420 PayoffCandidates
191 CrossEpisodeEdges
```

## 8. 최종 규격 결정

### Stage01

```text
SceneCard 9 keys
CORE16 only
```

### Stage02

```text
SequenceBlueprint 18 keys
value_shift {from,to}
turn_type registry 11
turn_class RISE/FALL/REVEAL/STALL
runtime sum 1.0
density >= 0.11
```

### Stage03

```text
EpisodeArc 13 keys
CharacterArc = character × episode
RelationshipArc = pair × episode
LocalEdge = same episode, causal, gap0
PayoffCandidate = unconfirmed candidate
```

### Stage04

```text
all candidates dispositioned
CrossEpisodeEdge only after full-season fan-in
FullSeriesArc 17 keys
```

## 9. Python 경계

허용:

```text
extract / decode / split / hash / serialize / validate / package
```

금지:

```text
SceneCard meaning
Sequence meaning
Character/Relationship arc meaning
Edge/Payoff/Cross meaning
FullSeriesArc meaning
```

## 10. 개발자 보고 원칙

사용자가 “개발자 보고는 최소로”라고 지시했다.

앞으로 완료 보고는 다음만 포함한다.

```text
작품
범위
핵심 count
판정/errors/warnings
package link or repository path
SHA256
next
```

중간 작업 업데이트는 장시간 작업 시 간단히 제공하되 내부 quarter/episode PASS를 완료 결과처럼 보고하지 않는다.

## 11. 현재 정확한 상태

```text
101번째프로포즈 PASS_CANDIDATE
결혼못하는남자 PASS_CANDIDATE
공주가돌아왔다 PASS_CANDIDATE
시티헌터 PASS_CANDIDATE
내여자친구는구미호 PASS_CANDIDATE
CANONICAL 작품 0 — 사용자 최종 승격 전
```

## 12. 다음 정상 단계

```text
한국드라마04 archive 조사
→ 완료 5작품 제외
→ 다음 작품 1편 선정
→ SourceLock v2
→ 전반부 계획
→ EP01 Q1 직접독해
```

새 세션은 `docs/drama_analysis/NEXT_SESSION_BOOTSTRAP_CHECKLIST.md`를 그대로 실행한다.

## 13. 중요한 금지 재확인

- 시티헌터 또는 구미호를 신규 작품으로 다시 선정하지 않음
- Claude판과 GPT판의 서로 다른 scene numbering 계층 혼합 금지
- `LocalEdge`에 회차 간 bridge 금지
- internal episode checkpoint에서 사용자 제출 완료 선언 금지
- 과거 PASS JSON만 보고 신뢰 금지
- 사용자 승인 없이 CANONICAL 금지

## 14. 이 handoff의 next pointer

```text
last_completed_work = 내여자친구는구미호
last_completed_scope = FULL_SERIES_STAGE01_04
next_action = SELECT_NEXT_UNANALYZED_WORK_FROM_한국드라마04
next_internal_step = SOURCE_ARCHIVE_INVENTORY
```
