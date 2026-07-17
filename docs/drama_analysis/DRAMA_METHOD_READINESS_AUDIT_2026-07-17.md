# 드라마 분석 방법·새 대화창 실행 준비도 감사

## 판정

```text
기존 V2 가이드 + Schema V2: 구조와 실행 cadence는 충분
스타일 V1 사고 방지 능력: 불충분
V3 가이드 + Schema V2 + 최신 DB 상태: 즉시 분석 가능
V3 + 상세 플레이북 V2 + Claude 장점 채택 정책: 처음 적용하는 모델도 상세 의미 저작 가능
```

## 조사 대상

- 허브 V2·V3 실행 가이드
- Schema Contracts V2
- 검증·세션 효율 정책 V1
- Protocol Manifest V4·V5
- 신규 작품 상세 플레이북 V2
- Claude Stage03~04 장점 선택적 채택 정책 V1
- 드라마 분석 방법 조사·절차·팁
- 스타일 V1 품질감사 및 V2 재저작 검증기
- GPT·Claude Stage03~04 비교 감사 결과

## 기존 자료의 장점

- Stage01~04 키·enum·ID·FK가 명확하다.
- Quarter→Episode→Block→Full Series 순서가 명확하다.
- 경량검증과 강검증이 분리돼 있다.
- SourceLock, checkpoint, lineage, Fresh Extraction 규칙이 있다.
- LocalEdge와 CrossEpisodeEdge 경계가 명확하다.
- 새 대화창 최소 로드가 두 권위 문서로 축소돼 있다.

## 발견한 결함

1. 구조 PASS와 의미 품질 PASS가 별도 권위 상태로 강제되지 않았다.
2. 반복 템플릿·문법 붕괴·원문 파편형 제목 차단 규칙이 충분히 구체적이지 않았다.
3. 분석 속도 이상을 산출물 계보와 고유성으로 감사하는 규칙이 없었다.
4. 신규 작품의 semantic-quality current report를 DB registry가 필수로 요구하지 않았다.
5. 작품 완료 시 개별 ZIP과 갱신 전체 DB ZIP을 함께 제공하는 규칙이 없었다.
6. 고정 Arc 수량, 규칙적 n→n+2 CrossEdge, 소수 target 집중 감사가 약했다.
7. CharacterArc·RelationshipArc·Edge note의 의미 밀도와 중간 메커니즘 기준이 분산돼 있었다.
8. Claude 방식의 장점과 과밀·미완결 위험을 분리한 선택적 채택 정책이 없었다.

## V3 보강 결과

- 완료 권위를 structural + semantic + package 3축으로 변경
- 속도 이상 감사 trigger 추가
- exact/masked 반복 임계값 추가
- 인물·관계 trigger grounding 명시
- Stage04 규칙적 자동 배치와 target 집중 감사 추가
- 신규 DB 편입 시 semantic report 필수화
- 완료 시 개별 작품 ZIP + 전체 DB ZIP 동시 제공 기본값 확정

## Claude 장점 채택 보강

채택:

- CharacterArc의 이전 상태→trigger→선택→새 상태→후속 영향
- RelationshipArc의 신뢰·권력·정보·의존·적대·거래·은폐·공모 다축 해석
- LocalEdge의 source→중간 인과 메커니즘→target 설명
- CrossEpisodeEdge의 plant→중간 변형→payoff→인물·관계·주제 결과
- 주인공 외 조직·가족·팀·경쟁 진영의 넓은 앙상블 스캔

배제:

- 기계적 전 인물·전 관계 Arc화
- 고정 수량
- 과도한 LocalEdge와 인접 장면 자동 연결
- 회차 간 LocalEdge
- 미처리 후보
- 일부 깊은 레코드만 있고 작품 전체 Stage03~04가 미완성인 상태

공식 결합:

```text
Claude식 의미 밀도·앙상블 독해
+
현행 GPT식 직접독해·선택성·CandidateDisposition·SourceLock·검증·패키징
```

비교 감사는 동일 작품 블라인드 A/B가 아니므로 모델 절대 우열을 선언하지 않는다. 관찰된 저작 기술만 채택한다.

## 새 대화창 최소 입력

1. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md`
2. `SCHEMA_CONTRACTS_V2.md`
3. 최신 DB 상태 또는 작품 인덱스
4. 원본 아카이브

처음 체계를 적용하거나 상세 의미 저작이 필요한 경우:

```text
DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md
DRAMA_CLAUDE_STAGE03_04_STRENGTH_ADOPTION_POLICY_V1.md
```

이 입력이면 과거 대화 전체를 읽지 않고 작품 선정, SourceLock, Quarter 분할, Stage01~04 작성, 구조·의미 이중 검증, 패키징, DB 편입까지 실행할 수 있다.

## 최종 판정

V3 이후에는 새 대화창이 최소 권위 문서만으로 즉시 분석을 시작할 수 있다. 처음 적용하는 모델은 상세 플레이북과 Claude 장점 채택 정책을 추가로 읽으면 Stage03~04 evidence 밀도와 선택성까지 바로 적용할 수 있다.

구조 validator만으로 완료를 선언해서는 안 되며 신규 작품마다 의미 품질 보고서와 최종 Fresh Extraction을 반드시 함께 남겨야 한다.
