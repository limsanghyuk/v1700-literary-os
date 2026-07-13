# GPT–Claude 드라마 분석 규격 일치화·편입 규칙 v1.1

Document ID: GPT-CLAUDE-DRAMA-ALIGNMENT-V1.1  
Status: AUTHORITATIVE ALIGNMENT RECORD  
Updated: 2026-07-13

## 1. 최종 정정 결론

초기 비교에서 GPT의 Stage03이 얕거나 metadata-derived라는 평가가 있었으나, 이후 GPT가 해당 작품들을 원문 기준으로 재저작·보강했고 Claude가 다시 전수 감사했다.

최종 정정:

- 작품명과 실제 분석 내용 불일치 지적: 오탐
- 장면 참조가 대량 dangling이라는 지적: 오탐
- GPT가 다른 드라마를 분석했다는 지적: 오탐
- 보강 후 Stage01~04 내용 자체: 수용 가능
- GPT와 Claude의 SequenceBlueprint·EpisodeArc 핵심 스키마: 본질적으로 동일

현재 비교 대상은 “스키마가 다른 두 진영”이 아니라 동일한 Stage01~04 계약을 서로 다른 저작·검증 체계로 수행한 결과다.

## 2. 실제로 발견된 핵심 결함

일부 GPT 초기 패키지에서 회차 간 인과 연결을 `LocalEdge`에 넣었다.

```text
src_episode_no != tgt_episode_no
gap_episodes == 1
edge_type == causal
```

이 구조는 LocalEdge라는 계층명과 모순되고 CrossEpisodeEdge 채널과 중복되며 작품별 규약을 불일치시킨다.

최종 보정 규칙:

```text
LocalEdge = 동일 회차, gap 0, causal
CrossEpisodeEdge = 후속 회차, 검증된 callback/plant_payoff/subplot_counterpoint
```

회차 간 bridge는 실제 장거리 회수이면 cross 계층으로 이동하고, 단순 인접 연결이면 기각한다.

## 3. 공통 정본 계약

```text
SceneCard 9 keys
EpisodeMeta 5 keys
SequenceBlueprint 18 keys
EpisodeArc 13 keys
CharacterArc 8 keys
RelationshipArc 9 keys
Local/Cross Edge 12 keys
PayoffCandidate 7 keys
FullSeriesArc 17 keys
QuarterAudit 15 keys
```

공통 enum과 품질 하한:

```text
CORE16
TURN_TYPE11
TURN_CLASS4
PayoffCandidate4
CrossEpisodeEdge3
sequence density >= 0.11
권장 0.12~0.17
runtime_share sum == 1.0
trigger participant presence
core_mix grounding
candidate disposition coverage == 100%
```

## 4. GPT 방식에서 Claude가 수용한 검증 장치

### V1 Functional Holdout

- baseline retrieval과 graph-assisted retrieval 비교
- Recall@5 또는 target evidence hit
- 그래프층의 C축 효용 측정
- 비블라인드 제한 명시

### V2 SourceLock

- 원본 파일 SHA256
- 회차 장면 수
- normalized scene/heading hash
- marker anomaly
- canonical ordinal 정책

### V3 QuarterAudit

- Q1→Q4 직접독해 순서 증명
- 부분 Stage01 hash
- placeholder·중복·Python 의미 생성 검사

### V4 Lineage·Quarantine

- 실패판 격리
- supersession 관계
- 의미 변경과 무손실 규약 보정 구분
- 과거 FAIL과 수정 이력 보존

### V5 Portable Real Validator

- 절대 경로 없음
- 실제 산출물 재계산
- non-zero failure exit
- fresh extraction에서 재실행

## 5. Claude 방식에서 GPT가 수용한 저작 규율

- 원문 직접독해
- Stage01 SSOT
- Stage02 18키와 density floor
- CharacterArc = 인물×회차
- RelationshipArc = 관계쌍×회차
- Stage04는 전 회차 완료 후 fan-in
- trigger 참여자 검증
- core_mix grounding
- 반복 골격·템플릿 반게이밍
- report와 validation 모순 차단

## 6. 외부 산출물 편입 절차

```text
1. staging에 별도 해제
2. 패키지 SHA256·ZIP CRC
3. SourceLock과 실제 scene count 대조
4. 작품 내부 schema inventory
5. 규약 보정과 의미 재저작 분리
6. work_id/seq_id/edge_id 정규화
7. turning_point를 {seq_index, desc}로 정규화
8. LocalEdge 회차 간 bridge 제거
9. verify_work 또는 동등 gate 실행
10. verify_new_layers 또는 동등 gate 실행
11. 두 gate ERRORS 0
12. fresh extraction 재검증
13. 기존 정본 백업
14. supersession manifest
15. PASS_CANDIDATE로 편입
```

## 7. 동일 작품 충돌 규칙

서로 다른 분석판의 장면 수 또는 canonical ordinal이 다르면 계층을 혼합하지 않는다.

금지:

```text
Claude Stage01 + GPT Stage03/04
GPT SceneCard + Claude Sequence
서로 다른 scene numbering의 edge 결합
```

허용:

- 한 판본 전체 유지
- 다른 판본 전체 교체
- 원본 재감사 후 새로운 통합판 전량 생성

교체 전 기존 파일을 백업하고 rollback 가능하게 한다.

## 8. 무손실 규약 보정과 의미 재저작

### 무손실 보정

- `work_id`와 ID 접두사 통일
- 문자열 `scene_span`을 동일 값 list로 변환
- turning point를 containing sequence에 매핑
- 검증된 Local bridge를 CrossEdge로 이동
- runtime 반올림의 마지막 값 보정

의미 문장을 변경하지 않고 ledger에 `semantic_text_changed: false`를 기록한다.

### 의미 재저작

- source ordinal이 설명과 불일치
- trigger scene에 인물 부재
- 동일 evidence 복사
- invented core_mix
- 자동 sequence-successor edge
- Stage04 미확인 연결

원문·Stage01을 다시 읽고 작성하며 `semantic_text_changed: true`를 기록한다.

## 9. 최신 수용 상태 — 7작품 authoritative v3

2026-07-13 현재 다음 7작품은 최신 권위 계약과 독립 재검증을 통과한 `PASS_CANDIDATE`다.

```text
101번째프로포즈
결혼못하는남자
공주가돌아왔다
시티헌터
내여자친구는구미호
좋은사람
파라다이스목장
```

누적:

```text
115회
7,518 SceneCard
1,043 SequenceBlueprint
787 CharacterArc
757 RelationshipArc
1,634 LocalEdge
580 PayoffCandidate
301 CrossEpisodeEdge
460 QuarterAudit
7 FullSeriesArc
```

공통 감사 결과:

```text
7/7 PASS_CANDIDATE_AUTHORITATIVE_V3
errors 0
warnings 0
fresh extraction PASS
ZIP CRC PASS
internal SHA PASS
portable validator PASS
```

사용자 승인 전 `CANONICAL`은 금지한다. 최신 개별 수량·패키지 SHA는 `WORK_STATUS_2026-07-12.json`과 `WORK_CATALOG_2026-07-12.md`가 권위다.

## 10. 추가 분석 계층

새 계층은 다음 절차를 따른다.

```text
proposal
→ anchor work
→ baseline/ablation
→ structural gate
→ functional holdout
→ false-positive audit
→ versioned schema
→ adoption decision
```

스키마 필드가 많아지는 것 자체는 진화가 아니다. 기존 계층으로 표현되지 않는 기능적 가치가 독립 검증으로 입증돼야 한다.

## 11. 공통 최종 원칙

```text
내용은 원문에서 쓴다.
구조는 공통 스키마에 맞춘다.
검증은 실제 파일을 재계산한다.
장거리 연결은 전 시즌 뒤에만 확정한다.
외부 결과는 staging과 이중 게이트를 거쳐 수용한다.
사용자 승인 전에는 canonical이라 부르지 않는다.
```
