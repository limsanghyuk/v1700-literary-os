# CT-13 R3 최종 연구 Closure — 2026-08-18

## 결론

**Formal preregistered verdict: `UNDECLARED`**

이유는 결과가 약해서가 아니다. 봉인된 Claude renderer 48건에 대해 현재 GPT 세션 내부에서
세 가지 독립적 채점 엄격도(strict / semantic-lenient / conservative)로 반복 판정했을 때
EpisodeSynopsisPlan을 받은 C팔은 B와 N을 강하게 이겼다.

### 내부 강건성 수치

| 대비 | P1 | P2 | P3 | 방향 일치도 |
|---|---:|---:|---:|---:|
| C vs B | p=.0078125 | p=.0009766 | p=.0004883 | 0.9722 |
| C vs N | p=.0019531 | p=.0019531 | p=.0004883 | 1.0000 |

- C>B: 세 지표 모두 유의.
- C>N: P1/P2/P3 모두 유의.
- preregistered numeric PASS 조건은 모두 충족하는 패턴.
- post-N 고특이도 leakage 진단: 명시적 신호 0.

## 왜 PASS라고 인증하지 않는가

R3 preregistration §7은 planner/plan-author, renderer, scorer, custodian, unblinding을 논리적으로 분리하고
**단일 assistant session은 PASS를 인증할 수 없다고 명시**한다.

현재 renderer는 Claude 외부 6세션으로 독립됐지만,
3명의 scorer를 서로 다른 GPT 세션으로 실제 실행할 수 있는 도구가 이 런타임에 없다.
따라서 같은 GPT 세션 안의 3회 재채점 결과를 '3 independent scorers'라고 바꾸어 부르면 연구 규약 위반이다.

## 무엇까지 증거가 강한가

현재 데이터는 다음 명제를 강하게 지지한다.

> **좋은 work-specific EpisodeSynopsisPlan을 renderer에 공급하면,
> 계획이 없는 A/B와 작품이 틀린 N에 비해
> 유예 정책, debt 처리, exit-state 목표 달성 품질이 크게 좋아진다.**

하지만 다음 명제는 CT-13 R3만으로 증명되지 않는다.

> **N-1 상태만 보고 자율 planner가 그 수준의 EpisodeSynopsisPlan 자체를 생성할 수 있다.**

그것은 별도의 blind forward-plan 시험이 필요하다.

## DB 정책

- 38작 reverse-engineered EpisodeSynopsisPlan corpus: **CANONICAL 유지**
- 기존 분석 데이터 롤백: **불필요**
- EpisodeSynopsisPlan을 자율 생성 제어층으로 '과학적으로 증명 완료'라고 표기: **금지**
- autonomous forward generation: **EXPERIMENTAL_HOLD**

따라서 연구 과제는 '효과 없음'으로 끝난 것이 아니라,
**효과는 강하게 관찰됐으나 사전등록의 독립성 조건 때문에 formal verdict는 UNDECLARED**로 마감한다.
외부 GPT-family scorer 3세션이 동일 봉인 출력물을 채점하면 현재 수치 패턴을 정식 PASS로 승격할 수 있다.
