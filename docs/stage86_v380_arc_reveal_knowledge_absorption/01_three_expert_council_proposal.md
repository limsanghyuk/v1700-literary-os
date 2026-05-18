# Stage86 3인 협의회 제안서

작성일: 2026-05-13

## 1. 제안 배경

Stage85는 새 문학 기능을 크게 늘린 단계가 아니라, 기존 로직의 생존 여부를 증명하는 단계였다.

확인된 Stage85 기준선:

```text
pytest: 72 passed
GitNexus: 435 files, 3624 nodes, 5769 edges, 42 clusters, 166 flows
Symbol-to-Branchpoint entries: 12
P0 coverage: 100%
P1 coverage: 100%
provider_default_calls: 0
node2_raw_reveal_access_count: 0
stage85_release_gate: pass
main_release_gate: pass
```

따라서 Stage86은 Stage85가 만든 안전장치를 실전으로 사용하는 첫 단계가 되어야 한다.

사용자가 제공한 추가 평가의 핵심은 다음이다.

```text
Stage85는 개발 안전성 강화 단계다.
다음은 V380의 Arc-Reveal-Knowledge 기능을 흡수하여 다시 문학 기능으로 돌아가야 한다.
```

3인 협의회는 이 판단을 수용한다.

## 2. 최고 수석 아키텍트 의견

아키텍트 관점에서 Stage86의 본질은 장편 드라마의 시간축, 복선축, 인물 지식축을 하나의 운영 계층으로 묶는 것이다.

흡수해야 할 V380 장점:

- `SeriesArcPlanner`: 16부작 또는 24부작 시즌 아크의 자동 배치
- `CausalPlotGraph`: 에피소드 간 인과, 복선, 콜백, 감정 상승 엣지
- `EpisodeRevealBudget`: 사실/비밀 공개 정책을 episode 단위로 제어
- `CharacterKnowledgeProseBridge`: 인물별 지식 상태를 산문 렌더링 제약으로 연결

아키텍트 판단:

```text
Stage86은 단순한 모듈 추가가 아니다.
V1700의 macro/micro hierarchy에 Arc, Reveal, Knowledge라는 세 축의 장기 기억을 결합하는 단계다.
```

필수 권위 구조:

```text
GraphNexus = 내부 권위 그래프
BranchpointLogicGraph = 과거 로직 생존 판정
StageLineageGraph = 단계 계보
V380AbsorptionAdapter = 외부 구조 흡수 계층
```

금지 사항:

- Claude V380 구조를 wholesale copy하지 않는다.
- V1700의 Stage80 Korean drama hierarchy를 대체하지 않는다.
- Node2에 raw reveal 권한을 주지 않는다.
- GitNexus를 런타임 필수 의존성으로 만들지 않는다.

## 3. 최고 수석 컴파일러 의견

컴파일러 관점에서 Stage86은 다음 4개 컴파일 단위로 나누어야 한다.

| 컴파일 단위 | 역할 |
| --- | --- |
| `arc` | season/episode arc, causal edge, tension curve |
| `reveal_budget` | reveal policy, delay/block/foreshadow gate |
| `knowledge_bridge` | character knowledge state and prose rendering constraint |
| `stage86_gate` | Stage85 traceability와 Stage86 장편 기능의 통합 검증 |

컴파일러 판단:

```text
V380의 장점은 테스트 가능한 작은 규칙으로 코드화되어 있다는 점이다.
V1700은 이를 adapter와 contract로 흡수해야 한다.
```

구현 원칙:

- 새 기능은 `src/v1700/arc_reveal_knowledge/` 하위에 격리한다.
- 기존 Stage84/85 API는 깨지지 않는다.
- 모든 V380 흡수 개념은 `symbol_to_branchpoint_trace_manifest`에 추가한다.
- 모든 reveal/knowledge 위반은 예외 또는 gate issue로 표면화한다.
- 산문 렌더러는 enriched contract만 받으며 raw reveal store에 직접 접근하지 않는다.

## 4. 공동 제안

Stage86 공식 목표:

```text
V380의 장편 아크, 복선 예산, 인물 지식 제약을 V1700 Branchpoint OS에 흡수한다.
```

성공 조건:

- `SeriesArcPlanner` 대응 모듈 구현
- `CausalPlotGraph` 대응 모듈 구현
- `EpisodeRevealBudget` 대응 모듈 구현
- `CharacterKnowledgeProseBridge` 대응 모듈 구현
- KnowledgeStatus 5상태 구현
- RevealPolicy 4상태 구현
- Stage85 traceability 확장
- Stage86 release gate 추가
- provider_default_calls 0 유지
- Node2 raw reveal access 0 유지
- Stage85 release gate 후퇴 없음

## 5. 제안 결론

Stage86은 다음 진화 단계로 타당하다.

이유:

```text
Stage85가 안전망을 만들었다.
V380은 장편 문학 기능의 실질적 근육을 제공한다.
따라서 Stage86은 안전망 위에 Arc-Reveal-Knowledge 근육을 올리는 단계여야 한다.
```

