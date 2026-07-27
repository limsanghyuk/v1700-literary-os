# 새 세션 한국 드라마 분석 V10.1 실행 인계서

Document ID: `DRAMA_ANALYSIS_NEW_SESSION_HANDOFF_V10_1`  
Effective date: `2026-07-28`  
Status: `ACTIVE_ENTRYPOINT`  
Authority: `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1`

## 1. 시작 문서

1. `README_V10_1.md`
2. `CURRENT_AUTHORITY_POINTER_V10_1.json`
3. `DRAMA_ANALYSIS_SINGLE_AUTHORITY_V10_1.md`
4. `V10_1_AUTHORITY_MANIFEST.json`
5. `DATABASE_SNAPSHOT_V23_SUMMARY.json`
6. 대상 작품의 `work_state.json`과 마지막 `CHECKPOINT_LOCKED`

V10 문서는 역사·기초 계약으로 보존한다. 충돌 시 V10.1이 우선한다.

## 2. 현재 데이터베이스 상태

- 작품: 87
- 회차: 1,640
- SceneCard: 102,417
- 의미 PASS: 86작품
- Source Hold: 《최강칠우》 1작품
- Semantic Hold: 0
- 신규 CANONICAL 자동 승격: 없음

## 3. 핵심 결정

기존 86개 의미 PASS 작품을 모두 다시 직접 재작업하지 않는다.

기존 작품은 다음 방식으로만 보강한다.

```text
coverage·밀도 결손 탐지
→ 외부 분석 후보 수집
→ 원문·SceneCard·SourceIndex 접지
→ 참여자·중복·lineage 검사
→ SELECTIVE_APPEND
→ 독립 Functional Holdout
→ 비대상 작품 불변성
→ Fresh Extraction
```

Claude 등 외부 분석은 `EXTERNAL_ANALYSIS_CANDIDATE`이며 전량 복사하지 않는다.

## 4. 신규 작품 실행 순서

```text
SourceBoundaryReview
→ 원본 전체 순차 독해
→ Stage01
→ Stage02
→ Stage03 1차
→ Arc Coverage Expansion Pass
→ 회차 경량검사
→ 독립 원문 감사
→ EPISODE_CHECKPOINT_LOCKED
```

전 회차 Stage01~03가 잠긴 뒤에만 Stage04를 수행한다.

## 5. Arc Coverage Expansion Pass

신규 작품은 Stage03 뒤 보조 인물·관계 누락을 추가로 검사한다.

- 실제 상태 변화가 있는 보조 인물만 CharacterArc 후보로 둔다.
- 실제 상호작용과 관계 변화가 있는 관계쌍만 RelationshipArc 후보로 둔다.
- 고정 수량·밀도 목표는 금지한다.
- trigger 장면 당사자 존재를 확인한다.
- 기존 동일 키 record는 중복 추가하지 않는다.
- 후보·수용·거부 이유를 `arc_coverage_audit.json`에 남긴다.

## 6. 외부 분석 선택 수용

기본 mode는 `SELECTIVE_APPEND`다.

수용 조건:

- source hash 또는 canonical ordinal lineage 호환
- target scene 존재
- trigger 참여자 일치
- 실제 state/relationship delta 존재
- evidence와 장면 의미 일치
- 미래 정보 혼입 없음
- exact duplicate·반복 골격 없음
- 독립 원문 감사 완료

하나라도 실패하면 수용하지 않는다.

## 7. Functional Holdout

- 질문 세트와 정답키는 후보 Arc에서 자동 생성하지 않는다.
- 핵심 질문과 보조 질문을 분리한다.
- baseline과 reinforced의 Recall@5·MRR을 비교한다.
- 핵심 Recall@5가 하락하면 실패한다.
- 보조 질문 개선이 없으면 수용하지 않는다.

## 8. Core schema

Stage01~04 exact schema는 V10과 동일하다. V10.1은 다음 보조 증거를 추가한다.

- `arc_coverage_audit.json`
- `provider_selective_adoption_ledger.json`
- `functional_holdout.json`
- provider authorship provenance
- non-target immutability

## 9. 검증된 선례

《하얀거탑》에서 Claude 추가 Arc 160건 중 63건만 선택 수용했다.

- 핵심 Recall@5: 1.00 유지
- 보조 Recall@5: 0.00 → 1.00
- 기존 record overwrite: 0
- 장면 번호 오류·중복·간접 추정: 거부

## 10. 새 세션 첫 명령

```text
README_V10_1.md와 CURRENT_AUTHORITY_POINTER_V10_1.json을 읽고 V10.1을 활성 권위로 사용하라.
새 작품은 원본 직접독해로 Stage01→02→03을 작성한 뒤 Arc Coverage Expansion Pass를 수행하라.
동일 작품의 외부 provider 의미문은 최초 author lock 전에 열지 마라.
기존 작품은 전면 재작업하지 말고 결손 신호가 있는 경우에만 외부 분석을 후보화하여 SELECTIVE_APPEND하라.
Functional Holdout, 비대상 불변성, Fresh Extraction을 통과하기 전에는 보강을 승인하지 마라.
```
