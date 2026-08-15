# 한국 드라마 분석 현행 실행 방법 — V9.2 Deep Semantic + Thread R1

원본 대본과 SourceLock이 최상위 의미 권위다. 모델이 원문을 순차 직접독해하고 의미를 저작하며 Python은 추출·정규화·해시·직렬화·검증·비교·결정적 파생·패키징에만 사용한다.

Stage01~04 exact schema는 V10.1을 유지한다. THICK exact schema도 변경하지 않는다. LocalEdge는 동일 회차 causal / `gap_episodes=0`이고 회차 간 연결은 Stage04 CrossEpisodeEdge다.

THICK는 원문 재독해 독립 저작이다. Stage01/02 exact reuse, generic cast, 동일 시퀀스 역할복제는 blocking이다. Thread Continuity R1을 적용하고 Claude의 40%/30% 수치는 진단선일 뿐 hard correctness gate가 아니다.

## V9.2 필수 Deep-Semantic Gate
신규 작품과 보강 작품은 구조·해시·Q25 PASS만으로 CANONICAL 승격하지 않는다. 작품 완료 후 다음을 추가로 통과한다.

1. **owner-congruence**: `cast.character`와 `desire_or_function`의 실제 행동·욕망·기능 주체를 SOURCE에서 확인한다. 타인 이름이 문장에 등장한다는 이유만으로 자동 오류 처리하지 않으며 alias·반응 기능은 직접 판정한다.
2. **raw dialogue / script fragment**: 대사·지문·SOURCE whole/tail이 cast 기능문을 대신하지 않는지 검사한다. 분석문 뒤의 짧은 SOURCE tail도 검사한다.
3. **generic / aggregate payload**: 구조 템플릿이나 여러 인물·장면을 한 cast 기능문에 집계한 payload를 차단한다. 단어 하나만으로 자동 판정하지 않고 전체 표현과 SOURCE를 본다.
4. **실제 SOURCE 3점 표본**: 최소 초반·중반·최종회에서 실제 SOURCE excerpt가 들어 있는 표본을 모델이 직접 읽어 owner/function, raw contamination, generic/aggregate, info/payoff grounding을 판정한다.
5. **자동수정 금지**: owner 이름 prefix 일괄 제거, metric 맞추기용 문장 팽창, 의미 유사도 기반 thread 자동 병합을 금지한다.
6. THICK 수정 후 해당 R5/R8을 future-blind / deterministic 규칙으로 다시 생성하고 전체 scene parity를 재검사한다.

## 실행 모델
Block-Atomic V2를 유지한다. 최대 8회 연속 Block이며 응답당 고정 Sequence 수 제한은 없다. 각 Sequence는 `CHECKPOINT_LOCKED` 후 다음으로 이동한다. 과거 고정 3 Sequence hard cap은 폐기 상태다.

현재 26작 권위:
- THICK: `DB98_THICK_26WORK_QUALITY_THREAD_R1_DEEP_SEMANTIC_CANONICAL_AUTHORITY_20260815_V1`
- Planner/Runtime: `DB98_PLANNER_RUNTIME_26WORK_QUALITY_THREAD_R1_DEEP_SEMANTIC_PROFILE_V1_1_AUTHORITY_20260815_V1`
- THICK records: 3,883
- R5: 470
- R8: 470 / 29,628 scenes

새 세션은 정적 번들보다 live Hub `main`을 항상 우선한다.
