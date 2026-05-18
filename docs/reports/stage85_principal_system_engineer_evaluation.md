# Stage85 최고 시스템 프린시펄 엔지니어 평가 보고서

작성일: 2026-05-13

## 1. 평가 대상

평가 대상은 최신 GPT 진영 모델인 `V1700 Stage85 - GitNexus Density Upgrade and Symbol-to-Branchpoint Traceability`이다.

평가 근거:

- `package_manifest.json`
- `release/current/stage85_developer_handoff_report.md`
- `release/current/stage85_gitnexus_index_quality_report.json`
- `release/current/stage85_zip_probe_report.md`
- `manifests/symbol_to_branchpoint_trace_manifest.json`
- `tests/test_stage85_traceability.py`
- Claude 로컬 참고 자료: `C:\AI_Codex\codex-work\claude\literary_os_v380_release.zip`
- Gemini 로컬 참고 자료: `C:\AI_Codex\codex-work\gemini`
- 외부 문학 생성/작문 도구 공개 문서: Sudowrite, NovelAI, Squibler

## 2. 최종 판정

```text
V1700 Stage85는 아직 일반 사용자용 완성 앱은 아니다.
그러나 검증 가능한 장편 문학 생성 OS 코어로서는 상위권 구조를 갖춘 개발자용 릴리즈 후보 수준이다.
```

정량 판정:

| 평가 영역 | 점수 | 판정 |
| --- | ---: | --- |
| 시스템 아키텍처 | 8.7 / 10 | GraphNexus, BranchpointLogicGraph, StageLineage, release gate가 유기적으로 연결됨 |
| 장편 구조 설계 | 8.2 / 10 | 16/24부작, macro/micro hierarchy, episode/sequence/scene 개념이 살아 있음 |
| 검증 가능성 | 8.1 / 10 | 72 passed, Stage85 gate pass, ZIP probe pass |
| 계보/패치 추적성 | 8.5 / 10 | symbol-to-branchpoint trace coverage 100% |
| 문체/독자 표면 | 7.1 / 10 | KoreanAntiLLMFilter, StyleDNA, ClosedLoopRenderer는 있으나 대규모 실제 산문 평가가 부족 |
| 제품 설치/사용성 | 5.8 / 10 | ZIP 검증은 통과했으나 사용자 UX, 설치 자동화, 샘플 실행 안내가 부족 |
| 상용 앱 경쟁력 | 5.5 / 10 | Sudowrite/Squibler 수준의 편집 UI와 워크플로우는 아직 없음 |
| 개발자 인계 가능성 | 8.0 / 10 | 문서, 매니페스트, 테스트, 리포트는 갖췄으나 GitHub/CI 정식화가 더 필요 |

종합 점수:

```text
엔진 코어 관점: 8.2 / 10
문학 생성 모델 관점: 7.2 / 10
일반 사용자 제품 관점: 5.8 / 10
상용화 직전 릴리즈 후보 관점: 6.7 / 10
```

## 3. Stage85의 현재 강점

### 3.1 검증 가능한 문학 OS 코어

Stage85의 가장 큰 강점은 “그럴듯한 생성기”가 아니라 “검증 가능한 운영체계”라는 점이다.

확인된 근거:

```text
pytest: 72 passed
GitNexus: 435 files, 3624 nodes, 5769 edges, 42 clusters, 166 flows
symbol_to_branchpoint_trace_gate: pass
gitnexus_index_quality_gate: pass
stage85_release_gate: pass
main release_gate: pass
ZIP extraction probe: pass
provider_default_calls: 0
node2_raw_reveal_access_count: 0
```

이것은 일반적인 프롬프트 기반 생성기와 구분되는 지점이다. V1700은 단순히 문장을 생성하는 것이 아니라, 생성 전후에 구조, 계보, 금지 reveal, provider 호출, branchpoint 생존 여부를 검사한다.

### 3.2 사용자 철학의 코드 생존성

Stage85는 사용자가 지속적으로 제기한 문제, 즉 “과거 패치의 장점이 현재 코어 어디에 살아 있는가”를 정면으로 다룬다.

새 매트릭스:

```text
literary branchpoint -> code symbol -> test -> release gate -> GitNexus evidence
```

현재 trace coverage:

```text
P0 coverage: 1.0
P1 coverage: 1.0
overall coverage: 1.0
```

이 점에서 Stage85는 단순 개발 산출물이 아니라, 사용자의 장기 창작기 철학을 보존하는 계보 관리 시스템으로 진화했다.

### 3.3 GitNexus optional sidecar 균형

Stage85는 GitNexus를 적극 활용하지만, 필수 런타임 의존성으로 만들지 않았다.

판정:

```text
개발자는 GitNexus로 영향 분석을 수행할 수 있다.
일반 사용자는 GitNexus 없이도 실행할 수 있다.
GraphNexus는 내부 권위 그래프로 남는다.
Python fallback은 필수 안전망으로 남는다.
```

이 균형은 제품 안정성 관점에서 옳다. GitNexus를 필수화하면 개발자 도구는 강해지지만 사용자 설치성이 떨어진다.

## 4. 다른 문학 창작기와의 비교

### 4.1 Claude Literary OS V380/V381 계열

Claude V380은 로컬 자료 기준으로 다음 모듈을 갖는다.

- `SeriesArcPlanner`: 16부작 아크 자동 생성
- `CausalPlotGraph`: 에피소드 간 인과/복선/감정 상승 그래프
- `EpisodeRevealBudget`: ALLOW, FORESHADOW_ONLY, DELAY, BLOCK 정책
- `CharacterKnowledgeProseBridge`: 인물 지식 상태를 산문 렌더 제약으로 연결
- V380 총 테스트: `2015 PASS / 2 SKIP / 0 FAIL`

사용자 제공 V381 GitNexus 참고값:

```text
332 files
10443 nodes
21487 edges
361 clusters
140 flows
```

비교 판정:

| 항목 | V1700 Stage85 | Claude V380/V381 | 판정 |
| --- | ---: | ---: | --- |
| 테스트 규모 | 72 passed | 2015 pass | Claude 우위 |
| GitNexus 심볼 밀도 | 3624 nodes | 10443 nodes | Claude 우위 |
| 실행 흐름 | 166 flows | 140 flows | V1700 우위 |
| 계보/branchpoint 추적 | 강함 | 중간 | V1700 우위 |
| 산문 표면 모듈 | V370 흡수 | V370/V380 확장 | Claude 우위 |
| 사용자 철학 보존 | 매우 강함 | 상대적으로 약함 | V1700 우위 |

결론:

```text
Claude 계열은 코드 밀도, 테스트 규모, 산문 제약 계층이 강하다.
V1700은 전체 운영 권위, stage lineage, branchpoint survival, release governance가 강하다.
```

다음 단계에서 V1700이 흡수해야 할 Claude 핵심은 V380의 `SeriesArcPlanner`, `EpisodeRevealBudget`, `CharacterKnowledgeProseBridge`이다.

### 4.2 Gemini/Aether 계열

Gemini 로컬 자료는 거대 컨텍스트를 기반으로 한 통합 서사 운영 체계를 지향한다.

확인된 핵심:

- 단일화된 컨텍스트 브레인
- Shadow Run 및 인과 시뮬레이션
- Python State Inference Engine
- Gemini API structured output
- DRSEGraph 기반 SSOT
- rollback/live promotion 개념

비교 판정:

| 항목 | V1700 Stage85 | Gemini/Aether | 판정 |
| --- | --- | --- | --- |
| 거대 컨텍스트 운영 | 중간 | 강함 | Gemini 우위 |
| 로컬 검증 게이트 | 강함 | 개념상 강하나 현재 제품화 낮음 | V1700 우위 |
| Structured Output | 일부 | 강함 | Gemini 우위 |
| 패키지/릴리즈 검증 | 강함 | 낮음 | V1700 우위 |
| Shadow Run 철학 | 일부 계승 | 핵심 철학 | Gemini 우위 |

결론:

```text
Gemini 계열은 큰 기억과 상태 시뮬레이션 철학이 강하다.
V1700은 그 철학을 실제 릴리즈 게이트와 패키징 구조로 닫는 능력이 강하다.
```

V1700이 다음에 흡수해야 할 부분은 “거대 컨텍스트 자체”가 아니라, shadow run 후보 생성, rollback, live promotion의 명시적 트랜잭션화다.

### 4.3 Sudowrite

Sudowrite는 Story Bible, Outline, Write, Rewrite, Quick Edit 등 작가 UX 중심의 기능이 강하다. 공식 문서 기준으로 Story Bible은 synopsis, outline, chapter, scenes, style을 연결하는 작가용 작업대 역할을 한다.

비교 판정:

| 항목 | V1700 Stage85 | Sudowrite | 판정 |
| --- | --- | --- | --- |
| 사용자 UX | 낮음 | 매우 강함 | Sudowrite 우위 |
| 즉시 쓰기/리라이트 | 중간 | 강함 | Sudowrite 우위 |
| 내부 검증 투명성 | 강함 | 공개적으로 제한적 | V1700 우위 |
| 장편 인과 게이트 | 강함 | 사용자 도구 중심 | V1700 우위 |
| 설치형/소스 제공 | 강함 | SaaS 중심 | V1700 우위 |

결론:

```text
Sudowrite는 작가가 바로 쓰는 제품이다.
V1700은 아직 작가 앱이 아니라 검증 가능한 장편 생성 엔진이다.
```

### 4.4 NovelAI

NovelAI는 storytelling에 맞춘 모델, prose augmentation, text adventure, 긴 컨텍스트 기반의 창작 경험이 강하다.

비교 판정:

| 항목 | V1700 Stage85 | NovelAI | 판정 |
| --- | --- | --- | --- |
| 창작 몰입감 | 중간 | 강함 | NovelAI 우위 |
| 모델 기반 즉흥성 | 중간 | 강함 | NovelAI 우위 |
| 구조 검증/게이트 | 강함 | 공개적으로 제한적 | V1700 우위 |
| 장편 제작 통제 | 강함 | 사용자 프롬프트/설정 의존 | V1700 우위 |
| 개발자 검증 가능성 | 강함 | 낮음 | V1700 우위 |

결론:

```text
NovelAI는 창작 플레이그라운드로 강하고,
V1700은 장편 구조 통제와 검증 가능한 제작 파이프라인으로 강하다.
```

### 4.5 Squibler

Squibler는 AI story/novel writer, outline, chapter management, export 등 사용자가 바로 책/시나리오 작업을 진행하는 워크플로우가 강하다.

비교 판정:

| 항목 | V1700 Stage85 | Squibler |
| --- | --- | --- |
| 일반 사용자 제품성 | 낮음 | 강함 |
| 챕터/원고 관리 UX | 낮음 | 강함 |
| 내부 인과 검증 | 강함 | 공개적으로 제한적 |
| 개발자 수정 가능성 | 강함 | 낮음 |

결론:

```text
Squibler는 제품이고, V1700은 제품이 되기 전의 고급 엔진 코어다.
```

## 5. 현재 약점

### 5.1 독자 체감 문체 평가가 아직 부족함

Stage84에서 KoreanAntiLLMFilter, StyleDNA, ReaderSurfaceScorer, ClosedLoopRenderer가 들어왔지만, 아직 대규모 산문 샘플에 대한 반복 평가가 부족하다.

문제:

```text
시스템은 글을 안전하게 만들 수 있다.
그러나 사용자가 “와, 이건 작가 같다”고 느끼는 수준을 지속적으로 보장하는 데이터는 아직 부족하다.
```

### 5.2 V380급 장편 아크/지식 브리지 미흡

Claude V380은 `SeriesArcPlanner`, `EpisodeRevealBudget`, `CharacterKnowledgeProseBridge`를 명시 모듈로 갖는다. V1700은 철학과 계보는 강하지만, 이 세 모듈의 코드화는 아직 흡수 전이다.

### 5.3 상용 UX 부재

V1700은 개발자용 ZIP, 테스트, 매니페스트는 갖췄지만 작가가 바로 쓰는 인터페이스는 약하다.

부족한 것:

- 프로젝트 생성 마법사
- Story Bible형 입력 화면
- episode/sequence/scene 편집 UI
- 생성 결과 비교 화면
- rewrite/expand/continue 버튼
- export 기능

### 5.4 실제 장편 생성 증거 부족

Stage83에서 3부작/30씬 증거가 있으나, 완전한 16부작 또는 24부작 전체 생성의 endurance proof는 아직 부족하다.

## 6. 다음 진화 방향

### Stage86: Reader-Facing Quality Loop

목표:

```text
사용자가 직접 느끼는 문장 표면, 감정 접근성, 자연스러움, 작가적 말맛을 강화한다.
```

필수 구현:

- 실제 산문 30~100씬 생성 세트
- pure GPT direct mode 대비 블라인드 평가
- KoreanAntiLLMFilter v2
- StyleDNA v2
- ReaderSurfaceScorer v2
- 대사 맛, 여운, 간접 감정, 상투성 제거 축 추가
- trace dataset 자동 축적

성공 기준:

```text
V1700 prose average >= pure GPT + 1.0
reader_surface_average >= 8.5
anti_llm_score >= 8.5
dialogue_taste >= 8.0
emotion_indirection >= 8.0
```

### Stage87: Claude V380 Arc Absorption

목표:

```text
V380의 장편 아크, reveal budget, 인물 지식 브리지를 V1700 권위 체계 안으로 흡수한다.
```

흡수 대상:

- SeriesArcPlanner
- CausalPlotGraph
- EpisodeRevealBudget
- CharacterKnowledgeProseBridge
- KnowledgeLeakageError
- RevealBlockedError

주의:

```text
Claude 구조를 그대로 복사하지 않는다.
GraphNexus, BranchpointLogicGraph, StageLineageGraph 권위 아래에 V380 기능을 adapter로 흡수한다.
```

### Stage88: Product Runtime & Author UX

목표:

```text
개발자용 엔진을 사용자가 실행 가능한 창작 제품으로 바꾼다.
```

필수 구현:

- `python -m v1700.cli new-project`
- `python -m v1700.cli generate --episodes 3`
- Story Bible 입력 파일
- episode/sequence/scene 출력 구조
- Markdown/Docx export
- sample project walkthrough
- Windows 설치 가이드

### Stage89: Full Season Endurance Proof

목표:

```text
16부작 또는 24부작 장편 생성의 구조 붕괴 여부를 검증한다.
```

필수 구현:

- 16부작 arc plan
- episode reveal budget ledger
- character invariant ledger
- relation change ledger
- sequence/scene count adaptive generation
- 3부작 단위 progression gate
- 16부작 전체 continuity audit

### Stage90: External Model Adapter Governance

목표:

```text
GPT, Claude, Gemini, local model을 비용과 역할에 따라 안전하게 분담한다.
```

필수 구현:

- provider role matrix
- cost budget policy
- local-first fallback
- external call dry-run
- prompt provenance ledger
- output contract validator

## 7. 최종 평가

V1700 Stage85는 지금 “완성된 문학 제품”은 아니다. 하지만 “검증 가능한 장편 문학 생성 OS”라는 관점에서는 이미 평범한 AI 글쓰기 도구와 다른 레벨에 올라와 있다.

최고 시스템 프린시펄 엔지니어의 최종 판정:

```text
Stage85는 상용 작가 도구보다 UX는 약하다.
Claude V380보다 코드/테스트 밀도는 약하다.
Gemini/Aether보다 거대 컨텍스트 운영은 약하다.

그러나 V1700은 계보, 검증, 권위 분리, 비용 통제, 장편 구조 철학의 통합성에서 가장 균형 잡힌 코어다.
다음 승부처는 더 많은 철학이 아니라, 독자가 읽고 감탄할 실제 문장 품질과 16부작 endurance proof다.
```

따라서 다음 단계 우선순위는 다음과 같다.

```text
1순위: Stage86 Reader-Facing Quality Loop
2순위: Stage87 Claude V380 Arc Absorption
3순위: Stage88 Product Runtime & Author UX
4순위: Stage89 Full Season Endurance Proof
5순위: Stage90 External Model Adapter Governance
```

## 8. 참고 출처

- Local Stage85 evidence: `release/current/stage85_gitnexus_index_quality_report.json`
- Local Stage85 handoff: `release/current/stage85_developer_handoff_report.md`
- Local Stage85 ZIP probe: `release/current/stage85_zip_probe_report.md`
- Local Claude V380 archive: `C:\AI_Codex\codex-work\claude\literary_os_v380_release.zip`
- Local Gemini workspace: `C:\AI_Codex\codex-work\gemini`
- Sudowrite Story Bible documentation: https://docs.sudowrite.com/using-sudowrite/1ow1qkGqof9rtcyGnrWUBS/what-is-story-bible/jmWepHcQdJetNrE991fjJC
- Sudowrite features documentation: https://docs.sudowrite.com/getting-started/dQph1snuwbfMWG9wRjsNug/features/dq7YUMNy5ZMvKUJiRAisyT
- NovelAI text model documentation: https://docs.novelai.net/en/text/models/
- Squibler AI Novel Writer: https://www.squibler.io/ai-novel-writer/

