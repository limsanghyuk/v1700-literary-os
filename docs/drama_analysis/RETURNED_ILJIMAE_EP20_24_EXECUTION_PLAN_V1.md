# 돌아온 일지매 EP20~EP24 실행 계획 v1

- Document ID: `RETURNED-ILJIMAE-EP20-24-EXECUTION-PLAN-V1`
- Status: `READY_TO_EXECUTE`
- Work: `돌아온일지매`

## 1. 현재 잠금 상태

```text
완료·검증 범위: EP01~EP19
다음 재진입: EP20 Q1
EP20 대화상 독해 보고: 존재
EP20 영속 파일/QuarterAudit/checkpoint: 없음
판정: INTERRUPTED_BEFORE_PERSISTENCE
Stage04: DEFERRED
```

EP01~EP19 개발자 핸드오프는 결정론적 계약 교정 36건 반영 후 `PASS_CANDIDATE_EP01_19_AFTER_DETERMINISTIC_CONTRACT_REPAIR` 상태다.

누적 규모:

```text
SceneCard 1,065
SequenceBlueprint 138
EpisodeArc 19
CharacterArc 138
RelationshipArc 115
LocalEdge 194
PayoffCandidate 161
EntityBridge 342
CastPresence 3,876
CharacterLoad 729
SourceSceneAlignment 1,065
QuarterAudit 76
```

## 2. 실행 분할

세션 한도 재발 방지를 위해 한 실행에서 한 회차만 완료한다.

```text
Run A: EP20 Q1→Q4 → Stage01~03/EXT6 → 강한 게이트 → checkpoint
Run B: EP21 Q1→Q4 → Stage01~03/EXT6 → 강한 게이트 → checkpoint
Run C: EP22 Q1→Q4 → Stage01~03/EXT6 → 강한 게이트 → checkpoint
Run D: EP23 Q1→Q4 → Stage01~03/EXT6 → 강한 게이트 → checkpoint
Run E: EP24 Q1→Q4 → Stage01~03/EXT6 → 강한 게이트 → checkpoint
Run F: EP01~EP24 Stage04 fan-in + FullSeriesArc + 전 시즌 강한 감사
```

## 3. 회차별 트랜잭션

각 Run은 반드시 다음 파일을 만든 뒤 종료한다.

```text
authored/<work>_NN.seqcard.jsonl
authored/<work>_NN.episode_meta.json
authored_seq/<work>_NN.seqblueprint.jsonl
authored_arc/<work>_NN.episodearc.json
authored_chararc/<work>_NN.chararc.jsonl
authored_relarc/<work>_NN.relarc.jsonl
authored_edges/<work>_NN.local_edges.jsonl
authored_edges/<work>_NN.payoff_candidates.jsonl
authored_cast/<work>_NN.cast.jsonl
derived_character_load/<work>_NN.load.jsonl
_ext6_audit/<work>_NN.source_scene_alignment.jsonl
_ext6_audit/<work>_NN.castcoverage.json
quarter_audits/<work>_NN_Q1..Q4.json
validation/<work>_NN_strong_validation.json
checkpoint ZIP + SHA256
SourceLock next 갱신
```

## 4. 회차별 검증

- Stage01/02 exact schema
- Q1~Q4 `LOCKED_PASS`
- Stage02 I-COVER/I-PARTITION/I-COUNT
- EpisodeArc act tiling
- Character/Relationship trigger presence
- LocalEdge target-core equality
- PayoffCandidate reference
- Bridge/Cast/Load exact schema·FK·recalculation
- Alignment and Coverage partition
- 반복 문형·keyword artifact·placeholder 0
- raw script export false
- Python semantic generation false

## 5. EP21 주의사항

과거 원본 조사에서 EP21의 scene numbering anomaly 가능성이 보고됐다. 원본 표기 번호를 정본 scene_no로 직접 사용하지 않고 canonical ordinal과 `source_heading_indexes/source_marker_anomaly`를 분리한다.

## 6. Stage04 마무리

EP24 checkpoint 성공 전 Stage04를 만들지 않는다.

Run F에서:

1. EP01~EP24 PayoffCandidate 전수 대조.
2. 실제 회수·변형·반향만 CrossEpisodeEdge 승격.
3. 모든 후보 disposition.
4. FullSeriesArc counts·시즌 구조 작성.
5. Stage01~04 + EXT6 전 시즌 강한 감사.
6. `PASS_CANDIDATE_FULL_SERIES` 패키지 생성.
7. 사용자 승인 전 canonical=false.

## 7. 진행 보고 규칙

회차가 대화상으로 이해되었더라도 checkpoint가 없으면 완료라고 보고하지 않는다. 다음 형식만 사용한다.

```text
EPxx_CHECKPOINT_LOCKED
Gate errors: 0
SourceLock next: EPyy
```
