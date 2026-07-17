# 드라마 분석 권위 인덱스 v5

- Status: `AUTHORITATIVE`
- Updated: 2026-07-17
- Supersedes: `DRAMA_ANALYSIS_AUTHORITY_INDEX_V4.md`

## 새 대화창 필수 로드

1. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`
2. `SCHEMA_CONTRACTS_V2.md`

신규 작품 선정 시 `DRAMA_ANALYSIS_DATABASE_STATUS_V12.json` 또는 최신 작품 인덱스 하나를 추가한다. 중단 작업 재개 시 해당 작품 compact checkpoint 하나만 추가한다.

처음 적용하는 모델이나 Stage03~04의 상세 저작 밀도·앙상블·Edge 선택성 기준이 필요한 경우 다음 companion을 추가한다.

```text
DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md
DRAMA_CLAUDE_STAGE03_04_STRENGTH_ADOPTION_POLICY_V1.md
```

## 권위 우선순위

| 영역 | 권위 문서 |
|---|---|
| 실행 순서·속도·검증 cadence | `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md` |
| exact keyset·enum·ID·FK | `SCHEMA_CONTRACTS_V2.md` |
| 기계 판독 실행 정책 | `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json` |
| 최신 DB 상태 | `DRAMA_ANALYSIS_DATABASE_STATUS_V12.json` |
| 상세 신규 작품 실행 해설 | `DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md` |
| Claude Stage03~04 장점 선택적 채택 | `DRAMA_CLAUDE_STAGE03_04_STRENGTH_ADOPTION_POLICY_V1.md` |
| 앙상블·LocalEdge 선택성 세부 정책 | `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md` |
| 직접독해 깊이 | `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` |
| lineage·package | `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` |
| 새 대화창 준비도 근거 | `DRAMA_METHOD_READINESS_AUDIT_2026-07-17.md` |

## 완료 권위

```text
STRUCTURAL_PASS
+ SEMANTIC_QUALITY_PASS
+ PACKAGE_FRESH_EXTRACTION_PASS
= PASS_CANDIDATE
```

구조 PASS만으로 의미 품질 완료를 선언하지 않는다. 사용자 승인 전 `CANONICAL`을 사용하지 않는다.

## Claude 장점 결합 정책

채택:

- CharacterArc의 이전 상태→trigger→선택→새 상태→후속 영향 설명
- RelationshipArc의 신뢰·권력·정보·의존·적대·거래·은폐·공모 다축 해석
- LocalEdge의 source→중간 인과 메커니즘→target 설명
- CrossEpisodeEdge의 plant→변형→payoff→인물·관계·주제 결과 설명
- 조직·가족·팀·경쟁 진영까지 넓은 앙상블 스캔

배제:

- 기계적 전 인물·전 관계 Arc화
- 고정 수량
- 과도한 LocalEdge
- 장면 인접성 자동 연결
- 회차 간 LocalEdge
- 미처리 후보
- 낮은 완결성과 검증 없는 Stage04

```text
Claude식 의미 밀도·앙상블 독해
+
현행 GPT식 선택성·CandidateDisposition·SourceLock·검증·패키징
```

## 기본 전달 규칙

드라마 한 작품의 전 시즌 분석이 완료되면 다음을 같은 보고에서 제공한다.

- 개별 작품 Stage01~04 ZIP
- 개별 Fresh Extraction 검증서
- 작품을 편입한 최신 전체 DB ZIP
- 전체 DB 최종 검증서
- 각 ZIP SHA256과 주요 집계

## 문서 로드 제한

과거 대화 전체, 모든 세션 README, 모든 방법론 문서를 시작 전에 전수 조사하지 않는다. 충돌·품질 감사·계약 변경이 있을 때만 관련 전문 문서를 부분 조회한다.
