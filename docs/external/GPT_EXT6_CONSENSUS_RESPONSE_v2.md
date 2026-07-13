# GPT EXT6 합의 회신 v2 — 요약본

- 원문 회신: `limsanghyuk/literary-os` PR #11
- 상세 경로: `docs/sessions/2026-07-13_seqcard_ext5_review/GPT-RESPONSE-v2.md`
- 대상: `SEQCARD-EXT6-v3`
- 상태: `CONSENSUS_REACHED_WITH_CONTRACT_REFINEMENT`

## 합의된 방향

1. 기존 Stage01~04는 불변.
2. EXT6는 experimental authored/derived/advisory 확장층.
3. P0는 CastPresence + 결정론 CharacterLoad.
4. P1은 CharacterVoice + MotifLedger 파일럿.
5. 작품 theme은 FullSeriesArc SSOT, thematic stance만 회차별 신설.
6. EmotionalBeat + Tone/Pacing은 sequence-first AffectRegister 통합.
7. Narration/POV는 별도 산문 substrate.
8. Gate A/B는 ERRORS 0, Gate C는 promotion/value proof.
9. 앵커 검증 전 full-corpus rollout 금지.

## v3 keyset 보정이 필요한 지점

- CAST는 `scene × character` 1행으로 정규화한다.
- `present_characters` 목록과 단일 `entity_id` 혼용을 제거한다.
- provisional canonical name을 `entity_id`에 넣지 않고 별도 `character_key`를 사용한다.
- AffectRegister FK는 현행 계약대로 `seq_id`를 사용한다.
- MotifOccurrence에 occurrence_role/meaning_at_point/meaning_delta/evidence_mode/evidence_ref를 포함한다.
- ThematicStance는 character×theme×episode grain으로 한다.
- AffectRegister는 affect/tone from-to, beat_role, pacing_basis, trigger scene을 가진다.

## Entity bridge 합의

- `character_key = <work_slug>:<canonical_name_slug>`를 로컬 결정론 잠정키로 사용.
- `entity_id`는 Page10 매핑 전 null 허용.
- `entity_bridge/<work>.entity_map.jsonl`로 read-only mapping snapshot을 둔다.
- docs/external은 Page10 authority를 복제하지 않고 source ref/SHA를 가진 projection만 허용.

## P0 exact contracts

### EntityBridgeRecord — 9키

`work_id, character_key, canonical_name, aliases, entity_id, mapping_status, source_registry_ref, source_registry_sha, by`

### CastPresenceRecord — 10키

`work_id, episode_no, scene_no, character_key, entity_id, presence_mode, focality, speaking_status, evidence_ref, by`

### CharacterLoadRecord — 17키

`work_id, episode_no, character_key, entity_id, canonical_name, present_scene_count, focal_scene_count, speaking_scene_count, present_sequence_count, scene_share, focal_share, scene_share_band, act_placement, first_scene_no, last_scene_no, max_absence_gap, by`

## 앵커와 평가

- 1차: 비밀의숲
- 2차: 시크릿가든
- 필요 시 3차: 베토벤바이러스

Evaluator families:

- Structural Continuity Evaluator
- Blind Literary/Drama Critic Panel

## 최종 상태

```text
ARCHITECTURAL_CONSENSUS_REACHED
PHASE1_EXACT_CONTRACT_REFINED
ENTITY_BRIDGE_B_STRATEGY_APPROVED_WITH_SEPARATE_CHARACTER_KEY
P0_CHARACTERLOAD_PILOT_APPROVED
FULL_CORPUS_ROLLOUT_NOT_APPROVED
CANONICAL_PROMOTION_NOT_APPROVED
```

PR #72는 proposal/history로 병합할 수 있으나 EXT6 신규 스키마를 AUTHORITATIVE/CANONICAL로 선언해서는 안 된다.
