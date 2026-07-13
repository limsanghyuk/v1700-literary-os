# GPT EXT6 Phase 1 — 비밀의숲 EP01 독립 저작 보고

- Run ID: `gpt_20260714_bimil_ep01_01`
- Provider: GPT-5.6 Thinking
- Contract: `SEQCARD-EXT6-PHASE1-CONTRACT-v1`
- Status: `GPT_RUN_CANDIDATE_LOCKED_STAGE01_SSOT_BASIS`
- Canonical: **아님**
- Claude row-level Cast/Bridge/Load 열람: **하지 않음**

## 산출물

- EntityBridge: 23행
- CastPresence: 170행
- CharacterLoad: 23행
- SceneCard coverage: 72/72
- annotated: 70
- empty_cast: 2 (`27`, `30`)
- unresolved: 0

## 검증

- Gate A Contract Integrity: **PASS / errors 0**
- Gate B Stage01 grounding: **PASS / errors 0**
- Raw-script direct grounding: **DEFERRED**
- Source-scene alignment: **DEFERRED**

## 상위 CharacterLoad

| 인물 | present | focal | speaking | scene_share | band |
|---|---:|---:|---:|---:|---|
| 황시목 | 49 | 44 | 27 | 0.6806 | DOMINANT |
| 강진섭 | 21 | 14 | 15 | 0.2917 | MAJOR |
| 한여진 | 21 | 17 | 16 | 0.2917 | MAJOR |
| 김수찬 | 8 | 2 | 8 | 0.1111 | MINOR |
| 박무성 어머니 | 8 | 3 | 4 | 0.1111 | MINOR |
| 박무성 | 7 | 0 | 1 | 0.0972 | MINOR |
| 영은수 | 7 | 5 | 7 | 0.0972 | MINOR |
| 서동재 | 6 | 4 | 4 | 0.0833 | MINOR |

## 증거 경계

현재 활성 런타임에는 비밀의숲 원본 대본/76개 source block이 없었습니다. 따라서 GPT는 공유된 Stage01 SceneCard 72개, SequenceBlueprint 14개, EpisodeArc를 직접 읽고 EXT6 P0를 후행 저작했습니다. Claude의 row-level 결과는 사용하지 않았습니다.

이 산출물은 **예비 비교용 candidate**입니다. 원본 대본이 제공되면 새 run_id로 Q1→Q4 raw-source reauthoring을 수행하고, 그 결과만 최종 κ 및 합의 gold 후보로 사용해야 합니다.
