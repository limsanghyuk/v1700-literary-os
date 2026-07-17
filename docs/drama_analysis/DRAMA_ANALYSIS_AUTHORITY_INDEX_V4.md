# 드라마 분석 권위 인덱스 v4

- Status: `AUTHORITATIVE`
- Updated: 2026-07-17

## 즉시 실행 최소 세트

새 대화창은 아래 두 문서만 읽고 분석을 시작한다.

1. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md`
2. `SCHEMA_CONTRACTS_V2.md`

신규 작품을 고를 때 최신 DB status/index 하나를 추가한다. 중단 작업을 이어갈 때 작품 checkpoint JSON 하나를 추가한다. 그 외 문서는 필요할 때만 읽는다.

처음 분석 체계를 적용하거나 Stage03 앙상블·LocalEdge 선택성·Stage04 후보 처분의 상세 사례가 필요한 모델은 다음 companion을 추가로 읽는다.

```text
DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V1.md
```

## 권위 순서

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset·enum·ID·FK
2. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md` — 실행 순서·작업 단위·검증 cadence
3. `DRAMA_VALIDATION_AND_SESSION_EFFICIENCY_POLICY_V1.md` — 경량/강검증 분리·증분 DB 검증·증빙 경량화
4. `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V4.json` — machine-readable execution contract
5. `DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V1.md` — V2의 원본 직접독해·Stage03·Stage04 상세 해설 companion
6. `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md` — Stage03·LocalEdge 선택성 세부 규칙
7. `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` — 직접독해 깊이 세부 규칙
8. `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` — lineage·package 세부 규칙
9. `DRAMA_SESSION_EXECUTION_SAFETY_V1.md` — 복구·세션 안전 참고
10. 최신 DB status 및 세션 handoff

V1 guide와 V3 validation 문서는 역사·세부 참고로 유지한다. 실행 cadence가 충돌하면 V2 guide와 효율 정책을 따른다. 상세 플레이북은 V2·schema·효율 정책을 덮어쓰지 않는다.

## 고정 파이프라인

```text
source inventory → DB 차집합 → SourceLock
→ EP01 Q1~Q4 → Stage01~03 → episode light gate → checkpoint
→ 다음 회차 반복
→ 전반부/약 8회차 strong gate
→ 후반부 반복 → 후반부 strong gate
→ full Stage01~03 gate
→ Stage04 disposition 100% → CrossEpisodeEdge → FullSeriesArc
→ individual ZIP → fresh extraction
→ incremental DB integration → global release gates → DB ZIP → fresh extraction
```

## Stage03 방법론 결합

채택:

- 회차별 주인공·대립자뿐 아니라 조직·가족·팀·경쟁 진영의 실제 변화 인물 추적
- 동맹·경쟁·상하·공모·거래·은폐 관계의 실제 변화 추적
- 앙상블·조직극에서 기능 인물과 사건축을 바꾸는 단역까지 스캔

배제:

- 등장인물·관계쌍 전부를 기계적으로 Arc화
- 고정 수량 채우기
- 과도한 LocalEdge
- 번호 인접성 자동 연결
- 회차 간 LocalEdge
- 미처리 PayoffCandidate

## 검증 경계

- 회차: 구조·참조·재개 가능성만 검사
- 전반부/8회차: 의미 중복·앙상블·관계·Edge 선택성 검사
- 전 시즌: Stage01~03 통합 검사
- Stage04: 후보 전수 처분과 회차 간 연결 검사
- 패키지: checksum·ZIP·fresh extraction 검사

## 운영 DB 증빙

운영 DB는 bulk `quarter_audits/`와 `direct_reading_evidence/`를 기본 제외한다. 독립 작품 패키지가 raw evidence 권위이며, 운영 DB에는 SourceLock attestation·count·aggregate hash·package SHA를 남긴다.

## 금지

- 새 대화창마다 허브·과거 대화 전수 학습
- 회차별 강검증
- 회차별 Fresh Extraction
- 여러 회차 동시 의미 생성
- Python 의미 생성
- LocalEdge 자동 인접 연결
- 회차 간 LocalEdge
- 미처리 후보
- 검증 완료 DB 전체의 불필요한 작품별 재검증
- 사용자 승인 없는 CANONICAL 승격
