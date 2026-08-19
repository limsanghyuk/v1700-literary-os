# 결혼못하는남자 Stage01~04 Claude 가이드 포렌식 재평가 v1

## 판정

`FAIL_EXISTING_KMN_STAGE01_04_UNDER_CLAUDE_GUIDE`

기존 `kmn_stage01_04_developer_delivery_claude_style_v1.zip`과 PR #62의 `PASS_FINAL_STAGE01_04_PRECISION_AUDIT` 주장은 새로 병합된 `docs/external/claude_drama_analysis_method_manual_stage01_04_v1.md` 기준에서 철회한다.

## Stage01

- 1,249개 장면의 상세 직접독해 내용은 부분 활용 가능하다.
- 기존 `authored/*.seqcard.jsonl`은 Claude canonical 9키가 아닌 GPT 확장 스키마다.
- title은 1,220/1,249 고유하다.
- `dramatic_function`의 CORE 마스킹 골격 3종이 각 22회, 총 66건 반복된다. 15% hard gate 미만이나 수정 경고 대상이다.
- 기존 상세본은 `authored_gpt_extended/`로 보존하고, Claude 9키 호환 투영본을 새 canonical Stage01 후보로 사용한다.

## Stage02

- 총 189개 SequenceBlueprint.
- EP03 `value_shift`에 허용되지 않은 `summary` 추가 키가 있다.
- EP05~EP10은 `value_shift` 문자열과 A/B 또는 자유 `turn_class`를 사용한다.
- EP11~EP16은 문자열 `scene_span`, 문자열 `value_shift`, 자유 `turn_class`를 사용한다.
- 16회차 전부 정확한 18키, `value_shift={from,to}`, list `scene_span`, 4버킷 `turn_class`로 교정했다.

## Stage03

- CharacterArc는 시즌 인물당 1건, 총 6건으로 구성되어 인물×회차 규칙을 위반한다.
- RelationshipArc는 시즌 관계쌍당 1건, 총 9건으로 구성되어 관계쌍×회차 규칙을 위반한다.
- 동일한 4등분 phase map 및 공통 start/end 문구가 반복된다.
- `by=gpt-5.5-thinking-stage03-stage04-metadata-derived`로 직접독해가 아닌 자동 파생임을 명시한다.
- LocalEdge 173건의 edge_type/label/note가 동일한 sequence-successor 형식이며 Claude causal edge 규격을 위반한다.
- PayoffCandidate도 정확한 회차별 7키 규격이 아니다.

## Stage04

- 기존 CrossEpisodeEdge는 인접 회차 말미→다음 회차 첫 sequence 자동 연결이며, 실제 callback/plant_payoff/subplot_counterpoint 확정이 아니다.
- edge_type과 label이 Claude enum/target-core 규칙을 위반한다.
- 기존 season wiring은 보조 참고물일 뿐 canonical Stage04가 아니다.

## 교정 상태

```text
Stage01: Claude 9키 호환 투영 완료
Stage02: 18키 전수 교정 완료
Stage03: QUARANTINED — 회차별 직접 재저작 필요
Stage04: QUARANTINED — 전 회차 fan-in 직접 재저작 필요
```

## 로컬 교정 산출물 SHA256

```text
kmn_claude_guide_reassessment_stage01_02_corrected_v1.zip
3194fc9678af1a718b0738ecd102b07c2c6fb1a5acab118c1a417f26611c757a

kmn_claude_guide_forensic_audit_v1.zip
e6aff1e5ccd04bca758400a6f262cadf73b6b619ec24b9ff86bed67e06f802ee
```

Stage03/04를 새 가이드에 따라 전량 재저작하고 강한 게이트가 `ERRORS 0`을 반환하기 전에는 작품 전체 PASS를 재선언하지 않는다.
