# EXT6 고정 버전 교정 정책

시행일: 2026-07-30  
Last amended: 2026-07-30

## 상위 원칙

EXT6 분석 방법은 `EXT6_SINGLE_AUTHORITY_V1_2`, 데이터 규격은 `EXT6_EXACT_SCHEMA_REGISTRY_V1_1`로 고정한다. 분석 오류, 검증기 오류, 장면 귀속 오류 또는 Entity 정규화 오류가 발견되더라도 이를 이유로 EXT6 방법·스키마 버전 번호를 계속 올리지 않는다.

## 교정 방식

1. 기존 Stage01~04와 기존 EXT6 정본 파일은 byte-exact로 동결한다.
2. 새 작품은 신규 EXT6 사이드카만 추가한다.
3. 기존 작품의 잘못된 EXT6 산출물은 같은 FIXED 계열 안에서 교정한다.
4. 교정 전 산출물은 덮어쓰거나 조용히 삭제하지 않고 `superseded` 또는 `revoked intermediate`로 기록한다.
5. 교정 이유, 영향 경로, 전후 해시, 폐기 대상과 채택 대상을 교정 원장에 남긴다.
6. 규격 변경과 데이터 교정을 구분한다. 데이터 오류 교정은 규격 버전 상승 사유가 아니다.
7. 최종 레코드를 동결한 뒤 품질감사를 새로 계산한다. 과거 감사 결과를 재사용하지 않는다.
8. 원문 근거, 장면 배타 구간, Entity 별칭, 출연 방식, 초점도와 발화 여부를 독립적으로 검사한다.
9. 기존 정본 파일 해시 변화, 경로 충돌, 스키마 외 enum, 장면 간 근거 중복 또는 비인물 Entity가 하나라도 있으면 편입을 금지한다.
10. `RiskAudit`, `SelectiveAppendLedger`, `FunctionalHoldout` 누락은 구조 PASS와 무관하게 완료 실패다.
11. 사용자 승인 전 상태는 `PASS_CANDIDATE_FIXED`이며 자동 CANONICAL 승격을 금지한다.
12. 교정 후 `EXT6_NEW_SESSION_HANDOFF.md`, pointer, status, queue를 같은 커밋 계열에서 갱신한다.

## 파일 명명

신규 EXT6 개별 산출물은 버전 번호 대신 다음 고정 명명 규칙을 사용한다.

`<작품명>_EXT6_APPEND_ONLY_EVIDENCE_FIXED_<YYYYMMDD>.zip`

통합 DB는 전체 작품 수와 EXT6 완료 작품 수를 분리해 기록한다.

`DB<전체작품수>_EXT6_<완료EXT6작품수>WORKS_WINDOWS_COMPATIBLE_FIXED_<YYYYMMDD>.zip`

같은 날짜에 교정이 발생하면 버전을 올리지 않고 교정 원장과 SHA256으로 정본을 식별한다.

## 실행 한도 보호

- 회차별 경검사
- 8회 블록별 강검사
- 전 시즌 최종 강검사와 Fresh Extraction은 1회
- checkpoint를 남기고 중단 시 완료 구간을 재실행하지 않는다.

## 현재 기준

- 방법 권위: `EXT6_SINGLE_AUTHORITY_V1_2`
- 고정 스키마: `EXT6_EXACT_SCHEMA_REGISTRY_V1_1`
- 편입 방식: `APPEND_ONLY_EXT6_SIDECAR_ONLY`
- 기존 의미 계층 수정: 금지
- 의미 보강 후보 패치 혼합: 금지
- Fresh Extraction: 필수
- 자동 정본 승격: 금지
- 새 방법·스키마 버전 상향: 금지
