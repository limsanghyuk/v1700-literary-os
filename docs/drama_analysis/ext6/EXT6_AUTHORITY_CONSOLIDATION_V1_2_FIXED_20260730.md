# EXT6 권위 통일 잠금

Status: `ACTIVE_BINDING`

## 단일 권위 순서

1. 사용자의 명시 지시
2. `EXT6_SINGLE_AUTHORITY_V1_2` — 분석 방법과 실행 순서
3. `EXT6_EXACT_SCHEMA_REGISTRY_V1_1` — 레코드 키와 enum
4. 《비밀의숲》 — gold method anchor
5. `EXT6_FIXED_VERSION_CORRECTION_POLICY_20260730` — 동일 고정 계열의 교정·supersession 기록

V1.4·V1.5·V1.6 등의 표기는 과거 패키지 또는 교정 이력일 뿐 분석 방법의 권위가 아니다. 이 문서 이후 새 작품은 V1.2 방법과 V1.1 exact schema만 사용한다.

## 작업 시작 전 차단 게이트

- V1.2 권위 문서 SHA 고정
- V1.1 schema SHA 및 enum 고정
- Stage01~04 byte-exact 동결
- 대상 EXT6 경로 충돌 0
- SceneCard 수와 SourceSceneAlignment 수 일치
- 정렬 구간 증가·비중첩
- Entity alias 단일 귀속

## 최종 차단 게이트

- 원문 근거가 해당 장면 구간 내부에 존재
- 장면 간 동일 근거 재사용 0
- 비인물 Entity 0
- focality와 speaking의 기계적 1:1 결합 금지
- presence mode 문맥 판정
- 최종 레코드 동결 후 감사 재계산
- 패키지 CRC 및 Fresh Extraction PASS
- 기존 기준 DB 파일 해시 변화 0

데이터 오류는 버전 상승으로 처리하지 않고 동일 FIXED 계열에서 교정한 뒤 supersession ledger에 기록한다.