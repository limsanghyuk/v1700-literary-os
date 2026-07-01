# GPT V1700 North Star Alignment Audit

## Status

- 문서 성격: 기준 기획안 부속 감사 문서
- 기준 문서: `docs/planning/gpt_v1700_integrated_master_plan.md`
- 추적 문서: `docs/planning/page18_to_page28_traceability_matrix.md`
- 기준 authority: Stage242 / Page17 Authority Closure
- Page18 상태: boundary only, runtime unopened
- Stage243 상태: not created

## 1. 목적

이 문서는 기존 Page18~28 설계와 신규 보강안이 GPT V1700의 최종 목표와 정합하는지 감사한다. 설계가 최종 목표와 충돌할 경우 최종 목표를 상위 authority로 두고 설계를 수정·강등·폐기한다.

## 2. North Star

> 인간 작가팀의 사고·판단·창작·비평·수정·학습 구조를 GPT V1700 Literary OS 안에 이식하여, 스스로 장기 문학을 기획하고, 스스로 장면을 생성하며, 스스로 오류를 감지하고, 스스로 수정 후보를 만들고, 측정된 결과를 다시 학습 신호로 축적하는 자율 문학 생성 운영체제를 만든다.

## 3. 감사 기준

각 설계는 다음 5개 질문을 통과해야 한다.

1. 이 설계는 인간 작가팀의 어떤 기능을 구현하는가?
2. 이 설계는 기획→생성→평가→수정→학습 폐회로 중 어디를 연결하는가?
3. 이 설계는 raw text, raw vector, token, adapter, canonical mutation 위험을 만드는가?
4. 이 설계는 측정 가능한 report, manifest, test를 남기는가?
5. 이 설계는 Page18~28 중 어디에 속하는가?

## 4. 판정 체계

| 판정 | 의미 | 처리 |
|---|---|---|
| KEEP | 최종 목표와 직접 정합 | 유지 및 우선 개발 가능 |
| PATCH | 방향은 맞지만 보강 필요 | 보강 설계 추가 후 개발 |
| DEFER | 최종 목표와 관련은 있으나 현재 순서가 아님 | 후순위 보류 |
| REJECT | 최종 목표와 충돌 | 금지 또는 폐기 |

## 5. Page별 감사 결과

| 대상 | 판정 | 이유 | 후속 처리 |
|---|---|---|---|
| Page18 Boundary | KEEP+PATCH | 생성 전 안전 경계로 North Star와 정합. 단 live generation으로 오해하면 위험 | Boundary hardening, opening checklist |
| Page19 Narrative State Graph | PATCH | 장기 상태 모델로 정합. 단 회차 loop와 feedback이 없으면 미완 | Season Wiring Orchestrator 추가 |
| Page20 Value Proof | PATCH | 비평·오류 감지와 정합. 단 평가 데이터 품질층 필요 | Pair Builder / per-token / held-out 선행 |
| Page21 Writer Studio | PATCH | 수정 후보와 작가 승인에 정합. 단 제품 표면 약함 | demo surface 선행 |
| Page22 Safe Personalization | DEFER | 장기 선호 반영에 정합하나 memory mutation 위험 | 승인 기반 memory boundary 이후 |
| Page23 Plugin Capability | DEFER | 확장성에 필요하나 기본 폐회로 전 확장 위험 | 기본 loop 이후 |
| Page24 Multi-Agent Studio | DEFER+CORE | 최종 목표와 직결되나 Page19~21 전에는 hollow multi-agent 위험 | 역할계약만 선행 가능 |
| Page25 Distribution | DEFER+HYGIENE | 제품화에 필요. 다만 core loop 전 full productization은 과도 | clean package hygiene만 선행 |
| Page26 Dashboard | DEFER | 가시화에 필요하나 보여줄 core loop가 먼저 필요 | Page21 축소판 후 |
| Page27 Data Foundry | KEEP+IMMEDIATE | 데이터→의도층→측정 asset 변환으로 매우 정합 | 즉시 선행 |
| Page28 Measured Learning | KEEP+IMMEDIATE | 측정 결과→학습 신호 축적에 매우 정합 | 즉시 선행 |

## 6. REJECT 조건

다음은 North Star와 충돌하므로 금지한다.

- Page18 live provider generation을 boundary 없이 여는 것
- OutputCaptureSchema freeze 없이 output capture를 시작하는 것
- canonical memory 자동 mutation
- runtime training 자동 시작
- 측정 없는 adapter promotion
- raw corpus text export
- raw vector payload export
- HF token / secret / adapter weight commit
- Stage243 자동 생성 또는 Stage244 자동 진행
- 문서·gate만 늘리고 16/24부작 작가팀 폐회로를 연결하지 않는 개발

## 7. PATCH 요구사항

### 7.1 Page19 Patch

필수 보강:

- Season Wiring Orchestrator
- N→N+1 feedback
- PayoffBrief injection
- SceneBeatGrid state binding
- NarrativeStateGraph serialization

### 7.2 Page20 Patch

필수 보강:

- Preference Pair Builder
- per-token only
- length neutrality
- no verbatim gate
- work-level split
- tokenizer lock
- held-out evaluation report

### 7.3 Page21 Patch

필수 보강:

- fixture-only Demo Writer Studio
- SceneFunctionCard
- AdvisoryDiffCard
- ApprovalDecisionRecord
- HTML/Markdown report

## 8. Immediate KEEP 우선순위

즉시 선행해야 하는 설계:

1. Page27 Data Foundry
2. Page28 Measured Learning Registry
3. Page19 Season Wiring Patch
4. Page18 Boundary Hardening
5. Page20 Value Proof Preflight
6. Page21 Demo Surface

## 9. 결론

기존 Page18~28 설계는 큰 방향에서 North Star와 정합한다. 그러나 그대로 순차 진행하면 데이터·학습·배선이 늦어져 자율 문학 생성 폐회로가 지연될 수 있다. 따라서 Page27/28을 선행하고, Page19에 Season Wiring을 보강하며, Page18 runtime opening은 계속 금지한다.

최종 판정:

> 기존 설계는 폐기하지 않는다. North Star 기준으로 재정렬한다. Stage243은 live generation이 아니라 Season Wiring + Data/Learning Bridge를 검증하는 pre-runtime stage로 정의한다.
