# EXT6 기계적 의미 저작 재감사

감사일: 2026-07-29  
대상: `101번째프로포즈`, `W`, `강남엄마따라잡기`  
상태: `QUALITY_HOLD_REVIEW_REQUIRED`

## 결론

포함된 도구에서 CharacterArc·RelationshipArc를 자동 생성하는 Stage03 의미 생성 코드는 발견되지 않았다. 추가 레코드에는 exact duplicate가 없고 대부분 원본 사건과 대응한다.

그러나 기계적 의미 저작이 없었다고 확정할 증거도 없다.

- 세 작품 SourceLock은 모두 `direct_reading_attested: false`다.
- 의미 레코드의 `by`는 직접 재독해를 주장하지만 독립적인 동시대 독해 원장이 없다.
- supplemental holdout 질문은 추가 Arc의 인물·사건 표현을 직접 재사용한다.
- holdout 평가기는 target identity 자체에 가산점을 주므로 새 레코드 존재 여부를 사실상 재확인한다.
- 따라서 `independent_question_design: true`와 보조 Recall@5 `0.0→1.0`은 독립 품질 증거로 무효다.
- `W` EP09 S060 오성무–진범 RelationshipArc는 trigger CastPresence에 진범이 없어 참여자 게이트를 위반한다.
- `강남엄마따라잡기`의 채택 17건이 EP16~18에 집중돼 전 시즌 균형 감사가 부족하다.

## 작품별 판정

| 작품 | 추가 Arc | exact duplicate | trigger 참여자 실패 | 판정 |
|---|---:|---:|---:|---|
| 101번째프로포즈 | 5 | 0 | 0 | HOLD |
| W | 18 | 0 | 1 | HOLD |
| 강남엄마따라잡기 | 17 | 0 | 0 | HOLD |

## 허용되는 기계적 계층

다음은 위험 신호용 sidecar이므로 규칙 기반 생성이 가능하다.

- SourceSceneAlignment
- CastPresence 후보 추출
- CharacterLoad
- CastCoverageLedger

다음은 의미 권위이므로 자동 파생만으로 승인할 수 없다.

- CharacterArc
- RelationshipArc
- state_delta
- relation_delta
- 독립 holdout 질문·정답

## 교정 절차

1. 세 작품의 완료 상태를 의미 품질 `HOLD`로 내린다.
2. 기존 supplemental holdout 결과를 폐기한다.
3. 후보 Arc를 보지 않은 별도 감사 run에서 질문 세트를 먼저 고정한다.
4. 각 Arc에 이전 상태 근거, trigger 원문 fragment, 참여자, 기존 Stage03 비중복을 기록한다.
5. `W` EP09 레코드는 trigger를 재지정하거나 기각한다.
6. `강남엄마따라잡기` EP01~15를 다시 표본 감사한다.
7. 재감사가 끝날 때까지 `개와늑대의시간`을 시작하지 않는다.
