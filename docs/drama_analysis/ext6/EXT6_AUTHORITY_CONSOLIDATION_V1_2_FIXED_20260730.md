# EXT6 권위 통일 잠금

Status: `ACTIVE_BINDING`  
Last amended: `2026-07-30`

## 단일 권위 순서

1. 사용자의 최신 명시 지시
2. `EXT6_SINGLE_AUTHORITY_V1_2` — 분석 방법·완료 정의·실행 순서
3. `EXT6_EXACT_SCHEMA_REGISTRY_V1_1` — 레코드 키·enum·자료형
4. 《비밀의숲》 — gold method anchor
5. `EXT6_FIXED_VERSION_CORRECTION_POLICY_20260730.md` — 동일 고정 계열의 교정·supersession 기록
6. `EXT6_NEW_SESSION_HANDOFF.md` — 현재 baseline·작품·checkpoint

V1.4·V1.5·V1.6 등의 표기는 과거 패키지 또는 교정 이력일 뿐 분석 방법의 권위가 아니다. 새 작품은 V1.2 방법과 V1.1 exact schema만 사용한다.

## 영구 버전 동결

- EXT6 방법 권위는 `V1.2`로 고정한다.
- EXT6 데이터 계약은 `V1.1`로 고정한다.
- 데이터 오류·검증기 오류·정렬 오류·Entity 오류 때문에 새 버전 문서를 만들지 않는다.
- 문제가 발견되면 `EXT6_SINGLE_AUTHORITY_V1_2.md`, 이 문서, 교정 정책, rolling handoff를 같은 경로에서 수정·보강한다.
- 동일 날짜·동일 파일명의 교정본은 SHA256과 supersession ledger로 구분한다.

## 작업 시작 전 차단 게이트

- V1.2 권위 문서와 V1.1 schema 로드
- gold anchor와 완료 정의 확인
- Stage01~04 byte-exact 동결
- baseline DB SHA와 파일 수 고정
- 대상 EXT6 경로 충돌 0
- SceneCard 수와 SourceSceneAlignment 수 일치 계획
- source format adapter와 수동 override 정책 확인
- rolling handoff의 현재 작품·checkpoint 확인

## 필수 완료 계층

다음 10개 계층이 모두 있어야 완료다.

`EntityRegistry` → `EntityBridge` → `SourceHeadingRegistry` → `SourceSceneAlignment` → `CastPresence` → `CastCoverageLedger` → `CharacterLoad` → `RiskAudit` → `SelectiveAppendLedger` → `FunctionalHoldout`

구조 validator, ZIP CRC 또는 Fresh Extraction만 통과한 상태를 완료로 올리지 않는다.

## Source order와 immutable scene ID

Stage01의 immutable `scene_no` 순서가 원문 물리 순서와 다른 경우 다음을 적용한다.

- Stage01 레코드와 scene_no는 수정·재발번하지 않는다.
- SourceSceneAlignment JSONL은 원문 물리 offset 순서로 직렬화할 수 있다.
- 각 alignment 레코드는 원래 scene_no를 identity로 유지한다.
- scene_no 집합은 SceneCard 전집합과 정확히 일치해야 하며 중복·누락은 0이어야 한다.
- 물리 순서 차이는 `LOGICAL_REHEADING` 또는 `MERGED_SOURCE_HEADINGS_WITH_LOGICAL_REHEADING`, `VERIFIED_MANUAL_OVERRIDE`, alignment note로 명시한다.
- validator는 source offset 증가·비중첩과 scene_no 전집합 유일성을 독립 검사한다.
- scene_no 오름차순을 맞추려고 무관한 후행 원문에 근거를 강제 귀속하는 행위를 금지한다.

## 최종 차단 게이트

- 원문 근거가 해당 장면 배타 구간 내부에 존재
- 장면 간 동일 근거 재사용 0
- 정렬 중첩·source offset 역행 0
- SceneCard scene_no 전집합과 alignment scene_no 전집합 일치
- alias 충돌·비인물 Entity 0
- focality와 speaking의 기계적 1:1 결합 금지
- presence mode 문맥 판정
- RiskAudit 후보별 직접 판정
- SelectiveAppend 수용·기각 원장
- core Recall@5 비하락, supplemental Recall@5 개선
- 최종 레코드 동결 후 감사 재계산
- 패키지 CRC 및 Fresh Extraction PASS
- 기존 기준 DB 파일 해시 변화 0

## 실행 한도 보호

- 회차별 경검사
- 8회 블록별 강검사
- 전 시즌 최종 강검사·DB 해제·전수 해시는 1회
- 회차·블록 checkpoint를 저장하고 재개 시 마지막 완료 지점 다음부터 실행

데이터 오류는 버전 상승으로 처리하지 않고 동일 FIXED 계열에서 교정한 뒤 supersession ledger에 기록한다.
