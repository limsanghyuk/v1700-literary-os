# 드라마 분석 권위 인덱스

Document status: **AUTHORITATIVE ENTRYPOINT / V3 CANDIDATE BRANCH**  
Version: 3.4-candidate  
Updated: 2026-07-16 (Asia/Seoul)

이 디렉터리는 한국 드라마 원본을 직접 읽어 Stage01~04 분석 산출물을 만들고, 검증된 결과를 `seqcard_ko` 데이터베이스에 편입하는 권위 문서군의 단일 진입점이다.

## 1. 새 대화창 최소 시작 세트

1. 이 `README.md`
2. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md`
3. `SCHEMA_CONTRACTS_V2.md`
4. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json`
5. 장편·업그레이드·속도 운영 시 `DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md`

## 2. 권위 순서

1. `SCHEMA_CONTRACTS_V2.md` — Stage01~04 exact schema·enum·ID·FK·불변식
2. `DRAMA_ANALYSIS_CURRENT_OPERATING_SUPPLEMENT_2026-07-15.md` — 현재 작업 단위·DB 삽입·EXT6 보류
3. `DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md` — 새 대화창 실행 절차
4. `DRAMA_DIRECT_READING_AND_BLOCK_EXECUTION_SUPPLEMENT_V3.md` — 직접독해·블록 속도·중단 복구·SourceLock 정규 저장
5. `DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md` — 앙상블 폭·LocalEdge 선별·후보 전수 처분
6. `DRAMA_CLOSE_READING_MASTER_PROTOCOL_V3.md` — 직접독해·내용 깊이
7. `DRAMA_VALIDATION_AND_RELEASE_GATES_V3.md` — fail-closed 강검증
8. `DRAMA_LINEAGE_PACKAGE_HANDOFF_V2.md` — SourceLock·계보·ZIP·허브 편입
9. `DRAMA_SESSION_EXECUTION_SAFETY_V1.md` — 세션 한도·체크포인트·중단 복구
10. `EXT6_DEFERRED_SIDECAR_POLICY_V1.md` — EXT6/HXT6 보류·보존
11. `DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-16.json` — 최신 DB 상태
12. 최신 `docs/sessions/*drama*/README.md` — 실제 산출물·SHA·handoff

## 3. 기본 파이프라인

```text
original_extracted/{작품명}/ 원본 TXT 저장
→ SourceLock
→ 회차 Q1→Q4 직접독해
→ Stage01 SceneCard
→ Stage02 SequenceBlueprint·EpisodeArc
→ Stage03 CharacterArc·RelationshipArc·LocalEdge·PayoffCandidate
→ 회차 경량 게이트
→ 약 8회차 블록 강검증
→ 전 시즌 Stage01~03 강검증
→ Stage04 후보 100% disposition
→ CrossEpisodeEdge·FullSeriesArc
→ 독립 ZIP
→ DB 삽입
→ 전체 DB validator·ZIP fresh extraction
```

## 4. 고정 운영 규칙

- Python·템플릿 의미 생성 금지
- 기존 정상 자산은 유지하고 의미 결함 범위만 재저작
- 기존 SceneCard는 색인, 원본은 최종 증거
- Stage03는 회차별 수직 처리
- 회차별 의미 강검증 반복 금지
- 기본 전달·검증 블록은 약 8회차
- 변화 없는 인물·관계 수량 채우기 금지
- LocalEdge는 동일 회차·gap 0만 허용
- 회차 간 연결은 Stage04 CrossEpisodeEdge만 사용
- PayoffCandidate disposition 100%
- 이전 회 마지막→다음 회 첫 장면 자동 브리지 0
- QuarterAudit 사후 일괄 생성 금지
- 사용자 승인 전 CANONICAL 금지

## 5. 원본·디렉터리 표준

```text
seqcard_ko/                              의미 데이터·규격 문서
seqcard_ko/original_extracted/{작품명}/ 작품별 UTF-8 TXT
seqcard_ko/source_lock/                  단일 SourceLock 루트
seqcard_ko/AUTHORED_WORK_INDEX_V7.json  51작품 분석 계층 전수 인덱스
tools/                                   실행 검증기
validation/                              검증 결과·휴대형 검증기
upgrade_audit/                           감사·이전 판본·lineage
provenance/                              입수 원본·변환 이력
```

`seqcard_ko` core에는 Python·ZIP·TMP·BAK·LOG를 두지 않는다. `_quarantine`, 독립 `docs`, 독립 `quarter_audits`, 독립 `source_alignment`, 중복 `source_lock`은 core 최상위에 만들지 않는다. EXT6/HXT6 관련 `_ext6_audit`은 보존한다.

## 6. 현재 데이터베이스 상태

```text
artifact: seqcard_ko_developer_release_51works_50complete_utf8_repaired_v7.zip
SHA256: 8a27d901d7122a1d9aebcadde459864adffd56c31553931327652744662e851f
works: 51
episodes: 970
SceneCard: 60,875
authored files: 1,994
analysis-layer files: 7,790
Stage01~04 complete: 50
remaining: 최강칠우 / SOURCE_HOLD_EXPERIMENTAL
CANONICAL promoted: 14
```

검증:

```text
ZIP CRC PASS
fresh extraction PASS
SHA256 ledger 9,742 / mismatch 0
filename mojibake 0
invalid UTF-8 text 0
U+FFFD files 0
JSON/JSONL parse errors 0
analysis files missing versus V6 0
errors 0 / warnings 0
```

V6은 한글 ZIP 경로 인코딩 결함으로 폐기한다. 분석 파일 삭제는 없었으며, V4→V5/V6에서 제거된 11개는 build script·dump·temporary validator·cache뿐이다.

대용량 ZIP과 raw script는 허브에 커밋하지 않는다. 허브에는 파일명·SHA·count·validation·lineage·handoff만 기록한다.

## 7. 개와늑대의시간 보강

16회 숫자행 레거시 EpisodeArc를 원본 TXT·SceneCard·SequenceBlueprint 직접 검토를 거친 exact ARC13으로 교체했다.

```text
EpisodeArc 16/16 ARC13
scenes 880
sequences 143
legacy numeric remaining in canonical 0
legacy numeric preserved for lineage 16
Python semantic generation false
errors 0 / warnings 0
```

상세 handoff:

```text
docs/sessions/2026-07-16-drama-db-clean-tree-wolf-arc13/README.md
docs/sessions/2026-07-16-drama-db-v7-utf8-repair/README.md
```

## 8. CANONICAL 승격 상태

사용자 명시 승인에 따라 다음 14작품만 CANONICAL 상태다.

```text
W, 경성스캔들, 미안하다사랑한다, 밀회,
더킹투하츠, 뉴하트, 킬미힐미, 하얀거탑,
마왕, 스카이캐슬, 궁, 카인과아벨, 싸인, 모래시계
```

이번 DB 정리·개와늑대의시간 ARC13 보강·V7 문자열 복구는 `PASS_CANDIDATE`이며 CANONICAL 승격을 수행하지 않았다.

## 9. EXT6/HXT6

EXT6/HXT6은 `DEFERRED_OPTIONAL_SIDECAR`다.

- 신규 분석 기본 범위에서 제외
- Stage01~04 완료 판정과 무관
- 기존 파일럿·감사 폴더 보존
- 별도 승인·파일럿·lineage 없이는 활성화하지 않음

## 10. 최소 개발자 보고

```text
작품·범위·계층 수량
최종 상태 / errors / warnings
독립 작품 ZIP SHA256
전체 DB ZIP SHA256
완료작·잔여작 수
SourceLock·원본 폴더 상태
문자열·파일명 UTF-8 상태
CANONICAL 승격 여부
```
