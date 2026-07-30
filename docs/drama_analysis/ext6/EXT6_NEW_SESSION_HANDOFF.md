# EXT6 새 세션 즉시 재개 핸드오프

Status: `ROLLING_CURRENT`  
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
- 현재 source hold: 《최강칠우》

## 4. 현재 작업

- 대상: 《궁》
- 회차: 24
- 상태: `IN_PROGRESS_V1_2_AUTHORITY`
- 시작 기준: DB90 baseline의 기존 Stage01~04·원본·SourceLock
- 다음 완료 조건: 10개 EXT6 계층, V1.2 RiskAudit, SelectiveAppendLedger, FunctionalHoldout, Fresh Extraction

## 5. 실행 주기

- 회차별 경검사
- EP01~08, EP09~16, EP17~24 블록별 강검사
- 전 시즌 최종 강검사와 전체 DB Fresh Extraction 1회
- 각 블록 checkpoint 저장
- 중단 시 마지막 완료 checkpoint 다음부터 재개

## 6. 금지 사항

- V1.3 이상 새 방법 권위 생성
- 구조 PASS만으로 작품 완료 처리
- speaking과 PRIMARY의 자동 결합
- 일반명사·행동문·장소명의 Entity 생성
- 동일 evidence의 복수 장면 귀속
- 기존 파일 수정·삭제·재정렬
- RiskAudit·SelectiveAppend·FunctionalHoldout 생략

## 7. 새 세션 첫 행동

1. 위 문서를 순서대로 읽는다.
2. baseline SHA와 로컬 파일 존재를 확인한다.
3. 현재 작품과 checkpoint를 확인한다.
4. 완료된 블록을 다시 생성하지 않는다.
5. V1.2 방법으로 남은 블록부터 즉시 계속한다.
6. 완료 후 이 문서의 baseline·현재 작품·checkpoint를 갱신한다.
