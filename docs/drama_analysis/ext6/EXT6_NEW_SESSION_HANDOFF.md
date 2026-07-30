# EXT6 새 세션 즉시 재개 핸드오프

Status: `ROLLING_CURRENT_SOURCE_ORDER_HOLD`  
Last updated: `2026-07-30`

이 문서는 새 대화 세션이 EXT6 작업을 즉시 이어가기 위한 단일 rolling handoff다. 새 버전 파일을 만들지 않고 항상 이 경로를 갱신한다.

## 1. 반드시 읽을 권위 문서

1. `docs/drama_analysis/ext6/EXT6_SINGLE_AUTHORITY_V1_2.md`
2. `docs/drama_analysis/ext6/EXT6_EXACT_SCHEMA_REGISTRY_V1_1.json`
3. `docs/drama_analysis/ext6/SECRET_FOREST_EXT6_GOLD_ANCHOR_V1_1.md`
4. `docs/drama_analysis/ext6/EXT6_AUTHORITY_CONSOLIDATION_V1_2_FIXED_20260730.md`
5. `docs/drama_analysis/ext6/EXT6_FIXED_VERSION_CORRECTION_POLICY_20260730.md`
6. 이 문서
7. `docs/drama_analysis/ext6/CURRENT_EXT6_POINTER.json`
8. `docs/drama_analysis/ext6/EXT6_ROLLOUT_STATUS.json`
9. `docs/drama_analysis/ext6/EXT6_ROLLOUT_QUEUE.json`
10. `docs/drama_analysis/ext6/EXT6_GUNG_SOURCE_ORDER_CONFLICT_AUDIT_20260730.md`

## 2. 고정 권위

- 방법: `EXT6_SINGLE_AUTHORITY_V1_2`
- 스키마: `EXT6_EXACT_SCHEMA_REGISTRY_V1_1`
- gold anchor: 《비밀의숲》
- 추가 버전 상향: 금지
- 오류 처리: 같은 FIXED 계열에서 교정하고 supersession ledger 기록
- 기존 Stage01~04: byte-exact 동결
- 자동 CANONICAL 승격: 금지

## 3. 현재 신뢰 baseline

- 파일: `DB90_EXT6_14WORKS_WINDOWS_COMPATIBLE_FIXED_20260730.zip`
- SHA256: `901b266b696dc683cd95eeaeb5ca9e0233ce93a054a52c2f2c993564abcdb829`
- 전체 작품: 90
- EXT6 완료 작품: 14
- 파일 수: 23,754
- 기존 source hold: 《최강칠우》
- 현재 EXT6 quality hold: 《궁》

## 4. 현재 작업: 《궁》

- 회차: 24
- 상태: `SOURCE_ORDER_CONFLICT_HOLD`
- alignment checkpoint 생성: 24회
- 승격 상태: 전부 미승격
- 무효 checkpoint: EP02
- 보존 checkpoint: EP01, EP03~24
- EXT6 완료 패키지: 없음
- DB 편입: 없음

### EP02 충돌

원문 물리 순서:

```text
Scene 30 (L1571)
→ Scene 42 (L1604–1753)
→ Scene 43 (L1754–1798)
→ Scene 44 (L1799–1951)
→ Scene 31 (L1952–1966)
→ Scene 32 이후
```

Stage01 ordinal:

```text
30 → 31 → ... → 41 → 42 → 43 → 44
```

Stage01을 byte-exact로 유지하면 Scene 42~44의 source offset이 Scene 31보다 앞서 V1.2 단조 정렬 규칙을 위반한다. 기존 자동 checkpoint는 Scene 42~44를 L2261–2428의 무관한 가족 장면에 강제 귀속했으므로 EP02 checkpoint는 superseded·invalidated 상태다.

## 5. 재개 조건

1. core Stage01 거버넌스에서 EP02 ordinal과 정본 원문 계보의 권위를 확정한다.
2. Stage01 ordinal 교정이 승인되면 EXT6 내부가 아니라 core 계층에서 supersession을 기록한다.
3. 충돌 해결 후 EP02 alignment와 파생 계층만 다시 생성한다.
4. EP01·EP03~24 checkpoint는 블록 강검사 후 재사용하며 처음부터 다시 만들지 않는다.
5. 《궁》 해결 전에는 다음 작품 《그대웃어요》로 큐를 이동하지 않는다.

## 6. 실행 주기

- 회차별 경검사
- EP01~08, EP09~16, EP17~24 블록별 강검사
- 전 시즌 최종 강검사와 전체 DB Fresh Extraction 1회
- 각 블록 checkpoint 저장
- 중단 시 마지막 완료 checkpoint 다음부터 재개

## 7. 금지 사항

- V1.3 이상 새 방법 권위 생성
- 구조 PASS만으로 작품 완료 처리
- source order inversion을 숨기기 위한 허위 근거 귀속
- Stage01 장면 번호의 EXT6 내부 임의 재배열
- speaking과 PRIMARY의 자동 결합
- 일반명사·행동문·장소명의 Entity 생성
- 동일 evidence의 복수 장면 귀속
- 기존 파일 수정·삭제·재정렬
- RiskAudit·SelectiveAppend·FunctionalHoldout 생략

## 8. 새 세션 첫 행동

1. 위 문서를 순서대로 읽는다.
2. DB90 baseline SHA와 로컬 파일 존재를 확인한다.
3. 《궁》 EP02 order conflict audit를 읽는다.
4. core 권위 해결 여부를 확인한다.
5. 해결되지 않았으면 허위 EXT6를 생성하지 않고 hold를 유지한다.
6. 해결됐으면 EP02만 재구축하고 보존 checkpoint부터 계속한다.
7. 완료 후 이 문서·pointer·status·queue를 같은 고정 경로에서 갱신한다.
