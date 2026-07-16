# 드라마 분석 권위 진입점

- Document status: `AUTHORITATIVE / V4`
- Updated: 2026-07-17

이 디렉터리는 한국 드라마 원본 직접독해, Stage01~04, 검증, 독립 작품 패키지, `seqcard_ko` DB 편입의 단일 진입점이다.

## 1. 새 대화창 최소 필독

새 대화창은 다음 두 문서만 읽고 즉시 실행한다.

1. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md`
2. `SCHEMA_CONTRACTS_V2.md`

신규 작품 선택 시 `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-17.json` 또는 실제 DB work index 하나를 추가한다. 중단 작업 재개 시 해당 작품 compact checkpoint JSON 하나를 추가한다.

**프로젝트 전체, 과거 대화, 모든 세션 README, 모든 방법론 문서를 매번 전수 조사하지 않는다.**

## 2. 실행 권위

1. `SCHEMA_CONTRACTS_V2.md` — exact schema·enum·ID·FK
2. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V2.md` — 즉시 실행 절차
3. `DRAMA_VALIDATION_AND_SESSION_EFFICIENCY_POLICY_V1.md` — 경량/강검증 분리·증분 DB 검증
4. `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V4.json` — machine-readable 계약
5. `DRAMA_ANALYSIS_AUTHORITY_INDEX_V4.md` — 상세 권위 순서

V1 guide와 V3 validation 문서는 역사·세부 참고로 유지한다. 실행 cadence가 충돌하면 V2 guide와 효율 정책이 우선한다.

## 3. 표준 파이프라인

```text
source inventory → current DB 차집합 → SourceLock
→ 회차 Q1~Q4 직접독해 → Stage01~03
→ episode light gate → checkpoint → 다음 회차
→ 전반부/약 8회차 strong gate
→ 후반부 동일 절차 → 후반부 strong gate
→ full Stage01~03 gate
→ Stage04 disposition 100% → CrossEpisodeEdge → FullSeriesArc
→ individual ZIP → fresh extraction
→ incremental DB integration → global gates → DB ZIP → fresh extraction
```

## 4. 검증 cadence

### 회차 경량검증

- parse·exact schema·ID
- SceneCard coverage
- Sequence partition·runtime sum
- trigger/edge references
- LocalEdge same episode/gap0
- checkpoint·next pointer

### 전반부/8회차 강검증

- 의미 반복
- Stage02 grounding
- 앙상블·관계 전역 감사
- LocalEdge 선택성·밀도·인접성
- PayoffCandidate 중복
- block ID/FK

회차마다 강검증·Fresh extraction을 실행하지 않는다.

## 5. DB 증분 검증

이전 DB가 ZIP SHA와 Fresh Extraction 검증서를 가진 immutable release이면 신규 작품만 작품 validator를 실행하고, 전체 registry/source/encoding/database/release gate를 실행한다. 이전 tree가 변경되지 않았다면 기존 작품별 의미 validator를 매번 재실행하지 않는다.

## 6. 직접독해 증빙 저장

독립 작품 ZIP은 raw quarter evidence를 보존한다. 운영 DB는 대량 `quarter_audits/`와 `direct_reading_evidence/` 폴더를 기본 제외하고 SourceLock·provenance에 attestation·count·aggregate hash·독립 패키지 SHA를 보존한다.

## 7. 현재 DB

```text
artifact: seqcard_ko_developer_release_54works_53complete_governance_v10.zip
SHA256: bec1959b6de3267674638519c128a4dcd57013b47d8176318093bd1db9128275
works: 54
episodes: 1,018
SceneCard: 63,941
Stage01~04 complete: 53
remaining: 최강칠우 / SOURCE_HOLD_EXPERIMENTAL
new work: 굿캐스팅
validation current reports: 54 PASS
fresh extraction: PASS
errors: 0
```

```text
CANONICAL_USER_APPROVED: 14
PASS_CANDIDATE_STRUCTURAL: 39
SOURCE_HOLD_EXPERIMENTAL: 1
```

상세 상태는 `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-17.json`을 따른다.

## 8. 금지

- Python·템플릿 의미 생성
- 여러 회차 동시 의미 생성
- 회차별 강검증
- 회차별 Fresh extraction
- 새 대화창마다 전체 허브 재학습
- 검증·패키징을 하나의 장기 프로세스로 결합
- 신규 작품 선택 전 DB 차집합 생략
- 사용자 승인 없는 CANONICAL 승격

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 artifact name, SHA256, counts, validation, lineage, handoff만 기록한다.
