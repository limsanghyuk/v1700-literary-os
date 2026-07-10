# GPT V1700 Literary OS 통합 기준 기획안

## Status

- 문서 성격: 기준 기획안 / planning authority supplement
- 기준 authority: Stage242 / Page17 Authority Closure
- Page18 상태: boundary / pre-runtime, runtime unopened
- Stage243 상태: not created
- 원칙: metadata-only, no raw corpus text, no raw vector payload, no provider live generation, no canonical mutation

## 1. North Star

GPT V1700의 최종 목표는 단순 대본 생성기가 아니다.

> 인간 작가팀의 사고·판단·창작·비평·수정·학습 구조를 GPT V1700 Literary OS 안에 이식하여, 스스로 장기 문학을 기획하고, 스스로 장면을 생성하며, 스스로 오류를 감지하고, 스스로 수정 후보를 만들고, 측정된 결과를 다시 학습 신호로 축적하는 자율 문학 생성 운영체제를 만든다.

이 목표는 모든 Page, Stage, Gate, 데이터 흡수, 학습 실험, 제품화 판단보다 상위의 설계 기준이다.

## 2. 현재 위치

GPT V1700은 현재 완성된 자율 문학 생성 모델이 아니다. 현재 위치는 다음과 같다.

- 자율 문학 생성 모델을 만들기 위한 권위·안전·데이터·경계·측정 기반 시스템
- metadata-only corpus absorption과 corpus-to-formula bridge가 추가된 상태
- Page18 runtime은 열리지 않았고, generation boundary/preflight만 허용된 상태
- Page27/Data Foundry와 Page28/Measured Learning은 최종 목표 달성을 위해 선행 중요도가 상승한 상태

## 3. 작가팀 폐회로

GPT V1700이 구현해야 하는 폐회로는 다음이다.

```text
Seed / Prompt
→ Synopsis Assembler
→ WorldSpec / ThemeSpec / CharacterSpec
→ CausalSpine
→ SeasonPlan
→ EpisodePlan
→ SceneBeatGrid
→ Page18 Generation Boundary
→ Scene Output Metadata
→ Page20 Value Proof
→ Revision Proposal
→ Human Approval
→ Page28 Measured Learning
→ Next Improvement
```

이 폐회로가 닫히지 않으면, 모델은 장면을 출력할 수는 있어도 인간 작가팀처럼 사고·판단·수정·학습하는 시스템이라고 볼 수 없다.

## 4. 데이터 확보에 대한 해석

개발자가 제공한 corpus, seqcard, 4070 실험 데이터는 GPT V1700에 필요한 데이터 기반으로 간주한다. 단, 데이터는 다음 세 계층으로 분리한다.

### 4.1 Raw Source Layer

예: Scripts.zip, corpus_ko01.zip 내부 raw txt/hwp/pdf/doc 가능 영역, original_extracted 계층.

- 로컬 private archive로만 유지
- GitHub/release/provider 전송 금지
- 직접 학습 투입 금지
- hash/provenance/inventory만 허용

### 4.2 Derived Metadata Layer

예: seqcard_ko.zip, scene intent records, episode_meta, series_arc, core/core2 taxonomy, scene function distribution.

- Page27/Data Foundry의 핵심 흡수 대상
- Page19/Narrative State Graph와 Season Writer Planner에 연결
- raw text 대신 장면 기능과 서사 의도를 구조화하는 계층

### 4.3 Experiment Evidence Layer

예: 4070_oneclick.zip, DPO pairs, W/M metrics, LoRA config metadata, training result metadata.

- Page28/Measured Learning Registry에 등록
- adapter weight, token, raw logs는 금지
- W/M/per-token/held-out/effect report만 허용

## 5. Claude Literary OS 참고 원칙

Claude literary-os는 GPT V1700의 authority가 아니다. 다만 다음 장점은 GPT V1700 독자 설계 안으로 재해석하여 흡수한다.

- SeqCard 의도층
- P0 Preference Pair Builder
- per-token 평가 원칙
- length neutrality
- no verbatim gate
- work-level split
- tokenizer lock
- Wiring Orchestrator
- NarrativeStateTensor feedback
- 8B / Frontier 역할분담
- 문학 생성 빈칸 5종

다음은 흡수하지 않는다.

- Claude의 version/stage authority
- raw text
- adapter weight
- token
- provider live logs
- 조기 성공 선언 방식
- 평가 편향이 있는 benchmark 결론

## 6. Page18~28 운영 해석

- Page18: Controlled Literary Generation Boundary. live generation 시작점이 아니라 boundary hardening 대상.
- Page19: Narrative State Graph. Season Wiring Orchestrator가 붙어야 실제 장기 회차 loop가 된다.
- Page20: Value Proof. Preference Pair Builder와 held-out evaluation 선행 필요.
- Page21: Writer Studio. full UI 이전에 fixture-only demo surface 필요.
- Page22: Safe Personalization. 후순위, 자동 memory mutation 금지.
- Page23: Plugin Capability. 후순위, 기본 창작 폐회로 이후.
- Page24: Multi-Agent Literary Studio. 최종 목표와 직결되지만 Page19~21 이후.
- Page25: Installer/Distribution. clean package hygiene는 선행 가능, full productization은 후순위.
- Page26: Dashboard. Page21 축소판 이후.
- Page27: Data Foundry. 즉시 선행.
- Page28: Measured Learning. 즉시 선행.

## 7. 우선순위 로드맵

1. Phase17-to-Phase18 Transition Master Plan 확정
2. Page18~28 Traceability Matrix 확정
3. North Star Alignment Audit 확정
4. Stage243 Scope Definition 확정
5. corpus_ko01 / Scripts / seqcard metadata-only inventory
6. 4070_oneclick measured learning registry
7. Preference Pair Builder I1~I5
8. Season Wiring Orchestrator preflight
9. Narrative State Graph serialization
10. Season Writer Planner
11. Page18 Boundary Hardening
12. Value Proof Preflight
13. Demo Writer Studio
14. Stage243 explicit approval review

## 8. Stage243 기본 정의

Stage243은 Page18 live generation stage가 아니다. 권장 정의는 다음이다.

> Stage243 = Season Wiring + Data/Learning Bridge Stage

Stage243에서 수행할 수 있는 일:

- corpus/seqcard metadata inventory
- preference pair builder invariants
- 4070 learning effect registry
- season wiring preflight
- narrative state graph serialization
- Page18 opening checklist

Stage243에서 금지되는 일:

- live provider generation
- output capture start
- canonical mutation
- runtime training
- adapter promotion
- raw text export
- raw vector export
- Stage244 automatic creation

## 9. 고정 안전 불변식

```json
{
  "provider_default_calls": 0,
  "runtime_training_enabled": false,
  "canonical_mutation_allowed": false,
  "raw_text_exported": false,
  "raw_vectors_exported": false,
  "token_exported": false,
  "adapter_committed": false,
  "page18_runtime_opened": false,
  "stage243_created": false
}
```

## 10. 최종 원칙

GPT V1700은 Claude를 따라가는 모델이 아니다. Claude가 데이터화한 장점은 흡수하되, GPT V1700의 독자 authority, metadata-only 경계, Page18 통제, Value Proof 원칙 안에서 자율 문학 생성 OS로 발전한다.
