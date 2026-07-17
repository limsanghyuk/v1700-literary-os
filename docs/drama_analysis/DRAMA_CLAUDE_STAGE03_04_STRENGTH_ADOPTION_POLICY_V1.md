# Claude Stage03~04 장점 선택적 채택 정책 v1

- Document ID: `DRAMA-CLAUDE-STAGE03-04-STRENGTH-ADOPTION-POLICY-V1`
- Status: `AUTHORITATIVE_COMPANION`
- Updated: 2026-07-17
- Execution authority: `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`
- Exact schema authority: `SCHEMA_CONTRACTS_V2.md`
- Governance authority: `DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json`
- Scope: 신규 드라마 Stage03~04 의미 저작의 밀도·근거성·앙상블 폭 향상

## 0. 결론

Stage03~04의 순수한 독해·이해·의미 설명 밀도에서는 Claude 방식의 완성 작품군이 우수한 부분이 분명히 관찰됐다. 그러나 Claude 방식 전체를 그대로 채택하지 않는다.

```text
Claude식 의미 밀도·앙상블 독해·구체적 evidence
+
현행 GPT식 직접독해·선택성·CandidateDisposition·SourceLock·검증·패키징
```

이 결합이 신규 작품 분석의 공식 적용 원칙이다.

다음 두 문장을 혼동하지 않는다.

```text
Claude의 Stage03~04 의미 설명 밀도가 더 높은 사례가 많다.
≠
Claude의 전체 분석 시스템과 최종 패키지가 항상 더 우수하다.
```

## 1. 비교 감사에서 확인된 경향

동일 작품·동일 장면의 블라인드 A/B 실험은 아니며, 서로 다른 작품군과 여러 run이 혼합된 결과 비교다. 따라서 모델 자체의 절대 우열이 아니라 작업 체계와 산출물 경향을 비교한 근거로 사용한다.

비교 감사에서 관찰된 Stage03~04 의미 필드 평균 길이:

| 필드 | GPT 비교본 | Claude 비교본 |
|---|---:|---:|
| CharacterArc `evidence` | 43.1자 | 80.0자 |
| RelationshipArc `evidence` | 39.1자 | 79.3자 |
| LocalEdge `note` | 42.1자 | 81.0자 |
| CrossEpisodeEdge `note` | 64.2자 | 92.9자 |

문자 수 자체를 품질 목표로 사용하지 않는다. 이 수치는 Claude 우수 사례가 다음 의미 요소를 더 자주 함께 설명했다는 관찰 지표다.

- 실제 사건
- 인물의 선택
- 선택 전후 상태 변화
- 신뢰·권력·정보·의존 조건의 이동
- source와 target 사이의 중간 인과 메커니즘
- plant가 중간 회차에서 보존·변형된 방식
- payoff가 인물·관계·주제에 미친 결과

## 2. 평가 축별 결합 원칙

| 평가 축 | 채택 정책 |
|---|---|
| CharacterArc 변화 설명 | Claude식 구체성·선택·후속 영향 채택 |
| RelationshipArc 조건 해석 | Claude식 다축 관계 해석 채택 |
| LocalEdge 사건 근거 | Claude식 원인→메커니즘→결과 설명 채택 |
| CrossEpisodeEdge 회수 설명 | Claude식 plant→변형→payoff→영향 채택 |
| 조연·조직·앙상블 폭 | Claude식 폭넓은 스캔 채택 |
| 작품 전체 완결성 | 현행 Stage01~04 완료 게이트 유지 |
| Candidate 처리 | 현행 100% disposition 원장 유지 |
| 후보→Edge 계보 | 현행 resulting edge·기각 이유 ledger 유지 |
| SourceLock·checkpoint | 현행 재현성 계약 유지 |
| LocalEdge·Stage04 선택성 | 현행 반사실·과밀·자동 패턴 차단 유지 |

## 3. 채택하는 Claude 장점

### 3.1 의미 필드의 설명 밀도

한 단어 상태명이나 추상 감정으로 끝내지 않고 다음을 연결한다.

```text
이전 조건
→ 실제 trigger
→ 인물 또는 관계의 선택·반응
→ 새 조건
→ 이후 행동·사건에 미치는 영향
```

### 3.2 회차별 앙상블 폭

주인공·대립자뿐 아니라 다음을 모두 스캔한다.

- 핵심 조력자·경쟁자
- 조직 의사결정자
- 반대 진영 기능 인물
- 반복 실무자·가족·동료
- 사건축을 바꾼 단역
- 동맹·경쟁·상하·거래·은폐·공모 관계

검토 범위는 넓히되 실제 변화가 있는 대상만 레코드화한다.

### 3.3 관계의 다축 이해

관계를 단일한 호감·신뢰 축으로 축소하지 않는다.

```text
신뢰
권력
정보 비대칭
의존
적대
거래
은폐
공모
보호
통제
상하관계
```

한 회차에서 서로 반대 방향의 축이 동시에 이동할 수 있다.

```text
개인적 신뢰 하락
+ 수사적 의존 상승
+ 정보 비대칭 감소
+ 권력 우위 재조정
```

### 3.4 인과의 중간 메커니즘

LocalEdge note는 단순히 “앞 장면이 뒤 사건을 일으킨다”라고 쓰지 않는다.

```text
구체적인 source 행동·정보·선택
→ 상대 또는 제도의 대응 전략 변화
→ target 사건이 발생한 구체적 메커니즘
```

### 3.5 장거리 회수의 서사적 변형

CrossEpisodeEdge note는 단순 회차 대응이 아니라 다음을 설명한다.

```text
무엇이 심어졌는가
→ 당시 어떤 기능과 의미였는가
→ 중간 회차에서 어떻게 보존·은폐·변형됐는가
→ target에서 무엇으로 회수됐는가
→ 회수 뒤 인물·관계·주제가 어떻게 달라졌는가
```

## 4. 채택하지 않는 Claude 방식

비교 코퍼스에서 의미 밀도와 별개로 다음 위험이 확인됐다.

- Stage03 작성 범위가 전체 회차에 비해 제한적
- CrossEpisodeEdge 완성 작품 비율이 낮음
- 과도한 LocalEdge
- 바로 다음 장면 연결 편향
- 회차 간 LocalEdge
- 미처리 PayoffCandidate
- 레코드 수량을 품질처럼 사용하는 경향

따라서 다음은 금지한다.

```text
등장인물 전원 CharacterArc화
모든 관계쌍 RelationshipArc화
고정 Arc·Edge·Candidate 수량
모든 장면 next-scene 연결
같은 시퀀스라는 이유의 LocalEdge
회차 간 LocalEdge
후보 disposition 누락
후보 일괄 CrossEpisodeEdge 승격
```

## 5. CharacterArc 저작 강화

### 5.1 약한 방식

```text
도찬은 위기를 겪으며 더 단단해진다.
```

문제:

- 이전 상태 불명
- trigger 불명
- 실제 선택 불명
- 새 행동 조건 불명
- 다른 작품에도 적용 가능한 추상문

### 5.2 채택 방식

```text
도찬은 검찰 대역을 끝내려 했으나 남승태의 죽음과 소금창고 납치를 목격한 뒤,
개인적 복수와 사기꾼의 생존 논리를 넘어 백준수의 수사를 자기 책임으로
계속하기로 선택한다.
```

### 5.3 필드 역할

```text
state_label
= 회차 종료 상태를 짧게 압축

state_delta
= 이전 상태 → trigger → 선택 → 새 상태

evidence
= 실제 사건·행동·대사 맥락·선택·후속 영향의 근거
```

### 5.4 필수 의미 요소

CharacterArc는 가능한 범위에서 다음을 포함한다.

1. 회차 입구 상태
2. trigger 사건
3. 인물의 선택 또는 거부
4. 회차 출구 상태
5. 다음 행동 가능성에 미친 영향

모든 요소를 기계적 문장 틀로 반복하지 않는다. 짧게 써도 구체적이면 통과할 수 있으며, 길어도 사건 나열뿐이면 실패다.

## 6. RelationshipArc 저작 강화

### 6.1 약한 방식

```text
하라는 도찬을 더 신뢰하게 된다.
```

### 6.2 채택 방식

```text
하라는 도찬의 백준수 사칭 때문에 수사 파트너로서의 신뢰를 철회하지만,
도찬이 조성두를 살리기 위해 자기 신분과 도주 가능성을 포기하는 장면을 확인한 뒤
도덕적 불신과 수사적 의존을 분리하기 시작한다.
```

### 6.3 필드 역할

```text
relation_state
= 회차 종료 시 관계가 작동하는 조건

relation_delta
= 신뢰·권력·정보·의존·적대·거래 중 이동한 축

evidence
= 두 인물의 실제 상호작용과 변화가 이후 선택을 바꾸는 근거
```

### 6.4 다축 기록

관계가 단순히 좋아지거나 나빠졌다고 쓰지 않는다. 필요한 경우 모순된 축을 함께 설명한다.

- 신뢰는 하락했지만 의존은 상승
- 정보 비대칭은 감소했지만 권력 통제는 강화
- 적대는 유지되지만 거래 조건은 안정
- 보호가 강화되지만 자율성은 축소

## 7. LocalEdge note 강화와 선택성

### 7.1 약한 note

```text
이 장면이 다음 사건을 일으킨다.
```

### 7.2 채택 note

```text
도찬이 바하마 계좌 명의자를 공개적으로 추궁하자 금태웅 측은 자금 흐름을
대통령에게 연결한 것처럼 조작할 시간이 부족해지고, 그 결과 특검을 강탈해
증거 자체를 통제하는 전략으로 전환한다.
```

### 7.3 필수 구조

```text
source의 구체 행동·정보·선택
→ 중간 대응·제약·전략 변화
→ target의 구체 결과
```

### 7.4 반사실 게이트

```text
source가 없었다면 target이 발생하지 않거나 실질적으로 다른 사건이 되었는가?
```

아니면 LocalEdge가 아니다.

### 7.5 선택성 통제

- 단순 인접 제외
- 같은 시퀀스 이유 제외
- 유사 감정·주제 제외
- 중간 절차 전달 제외
- 회차 간 LocalEdge 0
- `LocalEdge / SceneCard > 0.10` 수동 감사
- adjacent-target 비율 `>0.50` 수동 감사

`스위치` 전반부에서 LocalEdge를 180건에서 80건으로 줄인 사례는 다음 결합 원칙의 적용 사례다.

```text
Claude식 근거 밀도
+
GPT식 선택성 통제
```

## 8. PayoffCandidate 강화

PayoffCandidate는 단순 미결 사건 목록이 아니다. description 또는 별도 후보 원장에 다음을 구체적으로 남긴다.

```text
심어진 요소
당시 장면의 기능과 의미
예상 가능한 변형 방식
관련 인물·관계 궤적
후속 확인 지점
```

단, 예상은 확정이 아니다. 후속 원본 확인 전 CrossEpisodeEdge로 승격하지 않는다.

제외:

- 다음 장면에서 닫히는 문제
- 일반적 대사
- 회말이라는 이유만의 훅
- 장르 관습만으로 추정한 복선
- 수량을 맞추기 위한 후보

## 9. Stage04와 CrossEpisodeEdge 강화

### 9.1 유지하는 GPT식 운영 체계

- PayoffCandidate 전수 목록
- 후보별 disposition
- source·target 장면 번호
- 승격·기각 이유
- resulting edge ID
- 같은 회차 해결 분류
- 근거 부족 기각
- source mismatch 기각
- 자동 회차 브리지 금지
- target 집중 감사

### 9.2 강화하는 CrossEpisodeEdge note

```text
plant의 원래 기능
→ 중간 회차의 보존·은폐·변형
→ target 장면의 구체적 payoff
→ 인물 상태·관계 조건·주제에 미친 결과
```

### 9.3 Stage04 금지

- 미처리 후보 1건 이상
- 이전 회 마지막→다음 회 첫 장면 자동 브리지
- 규칙적 `EP n → EP n+2` 자동 배치
- 소수 target 장면에 Edge 집중
- 모든 후보 승격 또는 모든 후보 동일 이유 기각
- note가 candidate description의 복사

## 10. 의미 밀도 품질 감사

문자 수를 하드 쿼터로 사용하지 않는다. 다음 의미 구성요소로 감사한다.

### CharacterArc

```text
이전 상태 / trigger / 선택 / 새 상태 / 후속 영향
```

### RelationshipArc

```text
이전 관계 조건 / 상호작용 / 이동 축 / 새 관계 조건 / 후속 선택 영향
```

### LocalEdge

```text
source / 중간 메커니즘 / target / 반사실 근거
```

### CrossEpisodeEdge

```text
plant / 당시 기능 / 중간 변형 / payoff / 인물·관계·주제 결과
```

다음은 의미 품질 실패 신호다.

- 감정 형용사 하나로 상태 변화 종료
- “신뢰가 깊어진다” 같은 축 없는 관계 문장
- “이 장면이 다음 사건을 일으킨다” 같은 메커니즘 없는 note
- 회차 번호 대응만 있는 CrossEdge
- 동일 evidence·note 골격 반복
- 길지만 사건만 나열하고 선택·조건 변화가 없음

## 11. 완결성과 재현성 우선

비교 코퍼스에서 Claude Stage03 작성 범위는 전체 781회 중 약 17%, CrossEpisodeEdge 완성 작품은 40작품 중 5작품 수준이었다. 이 수치는 해당 코퍼스의 관찰값이며 Claude 모델의 절대 한계를 뜻하지 않는다.

신규 작품에서는 다음을 반드시 유지한다.

```text
전 회차 Stage03 완료
전 후보 disposition 100%
전 작품 Stage04 완료
SourceLock·QuarterAudit·checkpoint
structural + semantic dual pass
개별 작품 Fresh Extraction
전체 DB 증분 편입·전역 gate
```

깊은 일부 레코드보다 작품 전체의 일관된 완결성과 검증 가능성이 우선한다.

## 12. 동일 작품 A/B 한계

현재 비교는 동일 작품·동일 장면·동일 schema의 독립 블라인드 A/B가 아니다. 따라서 다음을 주장하지 않는다.

```text
Claude 모델이 모든 작품에서 GPT 모델보다 정확하다.
```

현재 정책이 채택하는 것은 모델 브랜드가 아니라 관찰된 저작 기술이다.

- 구체적 상태 변화
- 다축 관계 해석
- 중간 인과 메커니즘
- plant의 변형과 payoff 결과
- 넓은 앙상블 스캔

## 13. 신규 작품 적용 순서

```text
1. V3·Schema·DB status 로드
2. SourceLock·Quarter 분할
3. Stage01·02 직접독해
4. 회차별 앙상블 전체 스캔
5. 실제 변화 인물·관계만 Arc화
6. CharacterArc evidence를 상태→trigger→선택→새 상태→영향으로 작성
7. RelationshipArc evidence를 관계 조건·이동 축·후속 선택으로 작성
8. LocalEdge를 반사실로 선별하고 cause→mechanism→result로 note 작성
9. PayoffCandidate에 plant 의미·변형 가능성·확인 지점 기록
10. block semantic gate에서 반복·누락·과밀 감사
11. Stage04에서 후보 100% disposition
12. CrossEdge note를 plant→변형→payoff→영향으로 작성
13. structural + semantic + package 3축 통과
```

## 14. 최종 원칙

```text
앙상블 검토 폭은 넓게 한다.
레코드는 실제 변화만 만든다.
의미 설명은 상태·선택·조건·영향까지 구체화한다.
문장 길이는 품질 목표가 아니다.
LocalEdge는 적게 만들기 위해 줄이는 것이 아니라 인과가 아닌 것을 제거한다.
CrossEpisodeEdge는 회차 대응이 아니라 plant의 변형과 결과를 설명한다.
모든 후보는 100% disposition한다.
Claude식 의미 밀도는 채택한다.
Claude식 과밀·불완결·미처리 후보는 채택하지 않는다.
현행 SourceLock·ledger·검증·패키징 체계를 유지한다.
```
