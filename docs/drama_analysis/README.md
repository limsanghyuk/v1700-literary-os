# 드라마 분석 권위 인덱스

Document status: **AUTHORITATIVE ENTRYPOINT / V3 CANDIDATE BRANCH**  
Version: 3.1-candidate  
Updated: 2026-07-15 (Asia/Seoul)

이 디렉터리는 한국 드라마 원본을 직접 읽어 Stage01~04 분석 산출물을 만들고, 검증된 결과를 `seqcard_ko` 데이터베이스에 편입하는 권위 문서군의 단일 진입점이다.

## 1. 새 대화창 최소 시작 세트

새 대화창은 다음 네 문서를 순서대로 읽으면 바로 분석을 시작할 수 있다.

1. 이 `README.md`
2. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md`
3. `SCHEMA_CONTRACTS_V2.md`
4. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json`

프로젝트 전체 소스와 과거 세션 문서를 매번 전수 조사할 필요는 없다.

## 2. 전체 권위 순서

1. `SCHEMA_CONTRACTS_V2.md` — Stage01~04 exact schema·enum·ID·FK·불변식
2. `DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md` — 현재 작업 단위·DB 삽입·EXT6 보류
3. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md` — 새 대화창 즉시 실행 통합 절차
4. `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md` — 앙상블 폭 채택·LocalEdge 선별·후보 전수 처분
5. `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` — 직접독해·내용 깊이
6. `DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md` — fail-closed 강검증
7. `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` — SourceLock·계보·ZIP·허브 편입
8. `DRAMA_SESSION_EXECUTION_SAFETY_V1.md` — 세션 한도·원자 체크포인트·중단 복구
9. `EXT6_DEFERRED_SIDECAR_POLICY_V1.md` — EXT6 별도 보류
10. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json` — 현재 완료·잔여 상태
11. 최신 `docs/sessions/*drama*/README.md` — 실제 작업·SHA·다음 진입점

과거 클로드 방법론 문서는 역사·비교 자산이다. 현행 exact schema와 충돌하면 위 권위 순서를 적용한다.

## 3. 현재 분석 방법의 핵심

```text
원본 직접독해
회차별 Q1→Q2→Q3→Q4
Stage01 SceneCard
Stage02 SequenceBlueprint
Stage03 앙상블 CharacterArc·RelationshipArc
선별적 LocalEdge
PayoffCandidate
전 작품 Stage01~03 강검증
Stage04 후보 100% disposition
CrossEpisodeEdge
FullSeriesArc
독립 ZIP + 전체 DB ZIP
```

### 클로드 방식에서 채택한 장점

- 회차별 인물 변화 추적의 폭
- 조직·가족·팀·경쟁 진영의 관계망 추적
- 주인공 외 실제 변화가 있는 조연·기능 인물 포착

### 채택하지 않는 방식

- 과도한 LocalEdge
- 장면 인접성 자동 연결
- 회차 간 LocalEdge
- 미처리 PayoffCandidate
- 수량을 품질로 간주하는 방식

세부 정책은 `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md`를 따른다.

## 4. 현재 데이터베이스 상태

```text
작품: 49
회차: 938
SceneCard: 58,945
Stage01~04 완료: 43
업그레이드 잔여: 6
CANONICAL 승격: 13작품
```

최신 개발자 데이터베이스:

```text
seqcard_ko_stage04_progress_W_dream_gangnam_gyeongseong_misa_milhwe_theking_newheart_killme_whitetower_mawang_skycastle_gung_kain_sign_v1.zip
SHA256 2c1059eeecec38961f8e15ba68240bf4217b3996cf9318d5e29795b7a44932a6
```

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 파일명·SHA·count·validation·lineage만 기록한다.

## 5. 사용자 승인에 따른 CANONICAL 승격

```text
W
경성스캔들
미안하다사랑한다
밀회
더킹투하츠
뉴하트
킬미힐미
하얀거탑
마왕
스카이캐슬
궁
카인과아벨
싸인
```

EXT6은 승격 범위에 포함하지 않는다.

## 6. 남은 6작품

```text
공주의남자
녹두꽃
모래시계
역전의여왕
최강칠우
대장금
```

운영 우선순위:

1. 정상 원본·Stage01/02 후보: `공주의남자`, `녹두꽃`, `모래시계`
2. Stage02 재저작 장편: `역전의여왕`
3. 원본 복구 후: `최강칠우`
4. 최종 장기 블록: `대장금`

`최강칠우`는 실제 EP03 원본이 없으므로 `SOURCE_HOLD`다. `대장금`은 사용자 지시에 따라 가장 마지막에 8회차 블록으로 나누어 진행한다.

## 7. 안전 작업 단위

```text
의미 저작: quarter
원자 잠금: episode
개발자 전달: 8 episodes
Stage04: full-series fan-in
```

한 실행에서 여러 회차를 의미 생성하지 않는다.

## 8. 절대 금지

- Python·템플릿으로 의미 필드 생성
- 키워드 조각·참조 표식·반복 골격
- 회차 요약을 CharacterArc/RelationshipArc에 복사
- 실제 변화 없는 인물·관계를 수량 채우기로 생성
- LocalEdge에 회차 간 연결 저장
- 모든 장면을 다음 장면에 자동 연결
- 전 회차 Stage01~03 검증 전 Stage04 확정
- 이전 화 마지막 → 다음 화 첫 장면 자동 브리지
- 후보 미처리·일괄 disposition
- report PASS로 data FAIL을 덮기
- 원본 누락을 추정·창작으로 보완

## 9. EXT6

EXT6은 `DEFERRED_OPTIONAL_SIDECAR`다.

- 신규 분석 기본 범위에서 제외
- Stage01~04 완료 판정과 무관
- 기존 파일럿은 보존
- 별도 승인·파일럿·lineage 없이는 활성화하지 않음

## 10. 새 세션 시작 절차

```text
1. README
2. DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1
3. SCHEMA_CONTRACTS_V2
4. DATABASE_STATUS JSON
5. 완료 작품 제외 또는 신규 작품 확인
6. source inventory·SourceLock
7. 작품 분류: NEW / NORMAL_UPGRADE / STAGE02_REAUTHOR / SOURCE_HOLD
8. EP01 Q1 직접독해
9. 회차별 체크포인트
10. 전 작품 Stage01~03 강검증
11. Stage04 fan-in
12. 독립 ZIP·전체 DB ZIP
```

## 11. 최소 개발자 보고

```text
작품 / 범위 / 각 계층 레코드 수
최종 상태 / errors / warnings
독립 작품 ZIP SHA256
전체 DB ZIP SHA256
현재 완료작·잔여작 수
```

상세 판단과 교정 이력은 패키지 report·ledger·validation에 기록한다.
