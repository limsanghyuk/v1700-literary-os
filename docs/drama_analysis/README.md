# 드라마 분석 권위 진입점

- Document status: `AUTHORITATIVE / V5`
- Updated: 2026-07-17

이 디렉터리는 한국 드라마 원본 직접독해, Stage01~04, 구조·의미 품질 검증, 독립 작품 패키지, `seqcard_ko` DB 편입의 단일 진입점이다.

## 1. 새 대화창 최소 필독

새 대화창은 다음 두 문서를 읽고 즉시 실행한다.

1. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`
2. `SCHEMA_CONTRACTS_V2.md`

신규 작품 선정 시 `DRAMA_ANALYSIS_DATABASE_STATUS_V12.json` 또는 최신 DB work index 하나를 추가한다. 중단 작업 재개 시 해당 작품 compact checkpoint JSON 하나를 추가한다.

처음 이 체계를 적용하거나 Stage03~04의 상세 의미 저작 기준이 필요한 모델은 다음 companion을 추가로 읽는다.

```text
DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md
DRAMA_CLAUDE_STAGE03_04_STRENGTH_ADOPTION_POLICY_V1.md
```

과거 대화 전체, 모든 세션 README, 모든 역사 문서를 매번 전수 조사하지 않는다.

## 2. 실행 권위

1. `SCHEMA_CONTRACTS_V2.md` — exact keyset·enum·ID·FK
2. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` — 실행 순서·속도·검증 cadence
3. `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json` — machine-readable 정책
4. `DRAMA_ANALYSIS_AUTHORITY_INDEX_V5.md` — 상세 권위 순서
5. `DRAMA_ANALYSIS_DATABASE_STATUS_V12.json` — 최신 DB 상태
6. `DRAMA_METHOD_READINESS_AUDIT_2026-07-17.md` — 새 대화창 준비도 근거

상세 실행 companion:

```text
DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md
DRAMA_CLAUDE_STAGE03_04_STRENGTH_ADOPTION_POLICY_V1.md
```

## 3. 완료 권위

```text
STRUCTURAL_PASS
+ SEMANTIC_QUALITY_PASS
+ PACKAGE_FRESH_EXTRACTION_PASS
= PASS_CANDIDATE
```

구조 PASS만으로 의미 품질 완료를 선언하지 않는다. 사용자 승인 전 `CANONICAL`로 승격하지 않는다.

## 4. 표준 파이프라인

```text
source inventory → latest DB 차집합 → SourceLock
→ 회차 Q1~Q4 직접독해·QuarterAudit → Stage01~03
→ episode light gate → checkpoint → 다음 회차
→ 전반부/약 8회차 structural+semantic strong gate
→ 후반부 동일 절차 → 후반부 strong gate
→ full Stage01~03 dual gate
→ Stage04 disposition 100% → CrossEpisodeEdge → FullSeriesArc
→ individual ZIP → Fresh extraction
→ incremental DB integration → new-work structural/semantic validator
→ global registry/source/encoding/database/release gates
→ DB ZIP → Fresh extraction
```

## 5. Claude 장점의 선택적 채택

신규 작품은 Claude식 분석에서 확인된 다음 장점을 채택한다.

- CharacterArc에서 이전 상태→trigger→선택→새 상태→후속 영향을 구체적으로 설명
- RelationshipArc에서 신뢰·권력·정보 비대칭·의존·적대·거래·은폐·공모를 다축으로 해석
- LocalEdge note에서 source→중간 인과 메커니즘→target을 설명
- CrossEpisodeEdge note에서 plant→중간 변형→payoff→인물·관계·주제 결과를 설명
- 주인공 외 조직·가족·팀·경쟁 진영의 실제 변화 인물·관계를 폭넓게 스캔

다음은 채택하지 않는다.

- 등장인물·관계쌍 전부의 기계적 Arc화
- 고정 Arc·Edge·Candidate 수량
- 과도한 LocalEdge
- 장면 번호 인접성 자동 연결
- 회차 간 LocalEdge
- 미처리 PayoffCandidate
- 낮은 작품 완결성과 불완전한 Stage04

공식 결합 원칙:

```text
Claude식 의미 밀도·앙상블 독해
+
현행 GPT식 직접독해·선택성·CandidateDisposition·SourceLock·검증·패키징
```

## 6. 검증 cadence

### 회차 경량검증

- parse·exact schema·ID
- SceneCard coverage
- Sequence partition·runtime sum
- trigger/edge references
- LocalEdge same episode/gap0
- checkpoint·next pointer

### 전반부/8회차 강검증

- 구조 검증과 의미 품질 검증을 분리해 모두 실행
- exact·masked semantic repetition
- Stage02 grounding
- 앙상블 변화 누락
- 관계 trigger grounding·역방향 중복
- LocalEdge 반사실 인과·밀도·인접성
- PayoffCandidate 근거·중복
- block ID/FK

회차마다 강검증·Fresh extraction을 실행하지 않는다.

## 7. Stage03~04 선택성 원칙

- Arc는 실제 상태·관계 변화가 있는 대상만 기록한다.
- LocalEdge는 동일 회차의 구체적 causal 연결만 허용한다.
- 번호 인접성·같은 시퀀스·유사 주제는 LocalEdge 근거가 아니다.
- 회차 간 연결은 Stage04 CrossEpisodeEdge에서만 확정한다.
- 모든 PayoffCandidate를 개별 disposition하고 미처리 후보를 0으로 만든다.
- 이전 회 마지막 장면→다음 회 첫 장면 자동 브리지를 금지한다.
- 규칙적 `EP n → EP n+2` CrossEdge와 소수 target 집중을 감사한다.
- 문장 길이는 품질 목표가 아니며 상태·선택·조건·중간 메커니즘·후속 영향의 구체성을 평가한다.

## 8. DB 증분 검증

이전 DB가 고정 ZIP SHA와 Fresh Extraction 검증서를 가진 immutable release이면 신규 작품의 structural/semantic validator와 전체 registry/source/encoding/database/release gate를 실행한다. 이전 tree가 변경되지 않았다면 기존 작품별 의미 validator를 매번 재실행하지 않는다.

## 9. 직접독해 증빙 저장

독립 작품 ZIP은 raw quarter evidence를 보존한다. 운영 DB는 대량 `quarter_audits/`와 `direct_reading_evidence/` 폴더를 기본 제외하고 SourceLock·provenance에 attestation·count·aggregate hash·독립 작품 ZIP SHA·semantic-quality report를 보존한다.

## 10. 현재 DB

```text
release: SEQCARD_KO_GOVERNANCE_RELEASE_V12
works: 57
episodes: 1,066
SceneCard: 66,899
Stage01~04 complete: 56
source hold: 최강칠우
latest integrated work: 스타일 V2 reauthored
validation mode: incremental immutable V11 lineage + new semantic gate
```

상세 상태는 `DRAMA_ANALYSIS_DATABASE_STATUS_V12.json`을 따른다.

## 11. 완료 시 기본 전달물

- 개별 작품 Stage01~04 ZIP
- 개별 Fresh Extraction 검증서
- 작품을 편입한 최신 전체 DB ZIP
- 전체 DB 최종 검증서
- 각 ZIP SHA256과 주요 집계

## 12. 금지

- Python·템플릿 의미 생성
- 여러 회차 동시 의미 생성
- 회차별 강검증
- 회차별 Fresh extraction
- 새 대화창마다 전체 허브 재학습
- 검증·패키징을 하나의 장기 프로세스로 결합
- 신규 작품 선택 전 DB 차집합 생략
- LocalEdge 자동 인접 연결
- 회차 간 LocalEdge
- 미처리 PayoffCandidate
- 구조 PASS만으로 완료 선언
- 사용자 승인 없는 CANONICAL 승격

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 artifact name, SHA256, counts, validation, lineage, handoff만 기록한다.
