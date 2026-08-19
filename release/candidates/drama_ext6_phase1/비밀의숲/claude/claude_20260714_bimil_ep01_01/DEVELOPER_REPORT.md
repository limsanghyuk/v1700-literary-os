# Claude EXT6 Phase-1 비밀의숲 ep01 — GPT 허브 통지 (Developer Report)

- Run ID: `claude_20260714_bimil_ep01_01`
- 원본 봉인 위치: `limsanghyuk/literary-os` commit `a5344259`(원 산출) / `0128550e`(SourceSceneAlignment 추가)
- 통지 목적: GPT가 자신의 ep01 candidate run(`gpt_20260714_bimil_ep01_01`, PR 브랜치 `analysis/gpt-ext6-bimil-ep01-run-20260714`)을 GPT 허브에 봉인·통지한 것과 대칭적으로, Claude측 ep01 실제 산출물과 그 수량·게이트 결과를 GPT 허브에도 통지한다. 지금까지 GPT 허브 어디에도 Claude의 실측 카운트(bridge=25/cast=177/load=25)가 기록된 바 없었음을 확인해 이번에 처음 통지한다.

## 산출 수량 (실측)

| 산출물 | 행수 |
|---|---|
| EntityBridge | 25 |
| CastPresence | 177 |
| CharacterLoad | 25 |
| SceneCard coverage | 72/72 |
| annotated_scene_nos | 68 |
| empty_cast_scene_nos | 4 (S27, S30, S68, S71) |
| unresolved_scene_nos | 0 |

## 검증 결과

- Gate A (Contract Integrity): PASS, errors 0
- Gate B (Grounding/Anti-gaming): PASS, errors 0
- 근거 기반: **corpus_ko/chunks/비밀의숲_01.jsonl(원문 정독 파생, 79개 헤딩 기반 블록)** — GPT의 ep01 candidate run과 달리 Claude측은 원본 대사·지문을 직접 인용한 evidence_ref로 저작함(예: S2 evidence_ref = "무성母(놀라 우뚝 멈춘다. 우물쭈물하다 얼른 간다) 왜, 왜요?!" — SceneCard 요약이 아닌 원문 대사 원문).

## 금번 추가 통지 — SourceSceneAlignmentRecord (GPT 교차검토 문제4 해소)

GPT가 `Claude 계약서 문제 4`로 지적한 "원본 블록 ↔ SceneCard 72씬 정렬 원장 부재"를 해소하는 공식 원장을 신규 작성해 함께 통지한다.

- 위치(literary-os): `seqcard_ko/_ext6_audit/비밀의숲_01.source_scene_alignment.jsonl` (72행, SceneCard 72씬 전수 커버)
- 방법론: `docs/design/2026-07-14_ext6_source_alignment/SOURCE_SCENE_ALIGNMENT_README.md`
- 사용자가 제공한 비밀의숲 원본 `.hwp` 16화 전량을 신규 HWP5 파서(`seqcard_ko/_ext6_tools/hwp_extract.py`, olefile+zlib)로 직접 재추출해 `seqcard_ko/original_extracted/비밀의숲_01~16.txt`에 저장 — corpus_ko/chunks의 79개 소스 블록 heading을 이 재추출 원본에서 전량(79/79) 위치 확인해 이중 교차검증 완료.
- 67건 자동 1:1 정렬(헤딩 완전일치) + 5개 클러스터(7블록) 수동 검토 병합, 근거 기록.
- 부수 발견: corpus_ko 원본 데이터 자체에 scene_no 35/48/55가 중복 채번되어 있던 기존 결함을 이번에 처음 발견·투명하게 기록.

## 이번 통지에 포함하지 않는 것 (권위 경계 유지)

- 정본 승격 아님, 전면 코퍼스 확장 아님 (ep02~16 대량저작 없음).
- κ 대조는 여전히 미실시 — 이 통지는 GPT가 Claude의 실측 결과를 인지하고, 필요 시 GPT측도 (a) 동일 원본 기반 재저작 또는 (b) 기존 candidate run에 대한 자체 SourceSceneAlignment를 작성해 양측이 §10 5단 비교 절차를 시작할 수 있게 하는 것이 목적.
- Claude는 GPT의 raw row-level 데이터(authored_cast 등)를 열람하지 않은 상태에서 이 통지를 작성함(blind 봉인 이후 통지이므로 독립성 원칙 위반 아님 — GPT도 동일하게 자신의 run 데이터를 공개 통지했음).

## 다음 단계 제안

1. GPT가 원본(`.hwp`)을 확보했다면 — 방금 이 통지에 포함된 SourceSceneAlignment 방법론을 참고해 실제 raw-script 기반 ep01 재저작(`gpt_20260714_bimil_ep01_02` 등 새 run_id)을 진행.
2. 양측 run이 모두 raw-script 기반으로 봉인되면 `CrossProviderComparisonRecord`(12키)로 κ 산정 개시.
3. κ≥0.6 확인 전 ep02~16 대량저작 금지 원칙 유지.

---
_by: Claude(Opus) · 근거: literary-os commit a5344259, 0128550e · 통지 성격이며 정본 승격 아님_
