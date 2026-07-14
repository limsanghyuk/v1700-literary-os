# 드라마 분석 권위 인덱스 v3

- Document ID: `DRAMA-ANALYSIS-AUTHORITY-INDEX-V3`
- Status: `AUTHORITATIVE_CANDIDATE`
- Date: 2026-07-14
- Scope: 한국 드라마 원본 직접독해, Stage01~04, EXT6 Phase 1, 검증·계보·세션 안전 운영

## 1. 목적

드라마 분석 관련 규범이 기존 스키마 계약, Issue #60, EXT6 파일럿 문서, 작품별 체크포인트에 분산되어 있었다. 이 인덱스는 각 문서의 권위와 적용 순서를 하나로 연결한다.

## 2. 권위 순서

1. `docs/drama_analysis/SCHEMA_CONTRACTS_V2.md`
   - Stage01~04 exact keyset, enum, ID, FK, 불변식의 기존 권위 문서.
2. `docs/drama_analysis/DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md`
   - 원본 직접독해 방식, Q1→Q4 운영, 내용 깊이, Stage별 저작 순서.
3. `docs/drama_analysis/DRAMA_STAGE_EXT6_CONTRACT_MATRIX_V3.md`
   - Stage01~04와 EXT6 Phase 1의 결합 시점·산출물·공통 규격.
4. `docs/drama_analysis/DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md`
   - 구조·내용·반게이밍·EXT6·Stage04·패키지 검증.
5. `docs/drama_analysis/DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md`
   - SourceLock, QuarterAudit, quarantine, supersession, ZIP, 허브 편입.
6. `docs/drama_analysis/DRAMA_SESSION_EXECUTION_SAFETY_V1.md`
   - 세션 한도, 영속화 경계, 메모리/작업공간 정리, 재시작 규칙.
7. `docs/drama_analysis/RETURNED_ILJIMAE_EP20_24_EXECUTION_PLAN_V1.md`
   - 현재 작품의 EP20~EP24 실행 계획과 재진입 지점.

## 3. 기존 자산과의 관계

- Issue #60 `Drama Close Reading Protocol — Stage 1/2 Co-Authoring Quality Gate`의 핵심 원칙을 문서화하여 정식 운영 규범으로 승계한다.
- `SCHEMA_CONTRACTS_V2.md`의 Stage01~04 exact schema는 변경하지 않는다.
- EXT6은 Stage01~04를 수정하지 않는 sidecar 계층이다.
- EntityBridge·CastPresence·CharacterLoad는 Phase 1 동결 범위다.
- CharacterVoice·MotifLedger·ThematicStance·AffectRegister 등은 별도 계약 전까지 실험 계층이다.

## 4. 최우선 운영 원칙

```text
원본 직접독해
→ 회차 Q1→Q2→Q3→Q4
→ 각 Q에서 Stage01 + EXT6 capture
→ 회차 Stage02 재통합
→ Stage03 직접 저작
→ CharacterLoad 결정론 파생
→ 회차 강한 게이트
→ 체크포인트 영속화
→ 전 회차 완료 후 Stage04 fan-in
```

## 5. 공통과 모델별 자유의 경계

### 공통으로 고정

- 동일 SourceLock
- 동일 논리 SceneCard 경계
- exact keyset·자료형·enum
- ID·FK·계산식
- 검증기와 release gate
- provider/run provenance

### 모델별 최적화 허용

- 내부 메모 방식
- 에이전트 수
- 직접독해 보조 분업
- 검토 순서

단, 최종 산출물은 공통 계약으로 직렬화해야 한다.

## 6. 권위 상태

```text
STAGE01_04_SCHEMA: AUTHORITATIVE
CLOSE_READING_PROTOCOL_V3: AUTHORITATIVE_CANDIDATE
EXT6_PHASE1_ROW_SCHEMA: FROZEN
EXT6_ARTIFACT_SCHEMA_V2: ACCEPTED
CANONICAL_PROMOTION: USER_APPROVAL_REQUIRED
```
