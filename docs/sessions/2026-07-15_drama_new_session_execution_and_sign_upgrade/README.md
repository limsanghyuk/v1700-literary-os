# 2026-07-15 드라마 새 세션 실행 체계·싸인 업그레이드 핸드오프

- Status: `COMPLETE_HANDOFF`
- Date: 2026-07-15
- Scope: 새 대화창 즉시 실행 문서, 앙상블 방법 채택, 싸인 Stage01~04, CANONICAL 승격, DB 상태 갱신

## 1. 이번 세션의 권위 결정

1. 새 대화창은 프로젝트 전체를 전수 조사하지 않는다.
2. 최소 네 문서만 읽고 실행을 시작한다.
3. 클로드식 앙상블 인물·관계 추적 폭을 Stage03에 채택한다.
4. 과도한 LocalEdge·인접 장면 자동 연결·회차 간 LocalEdge는 배제한다.
5. 모든 PayoffCandidate는 Stage04에서 100% 개별 처분한다.
6. EXT6은 계속 비활성 sidecar다.
7. 사용자 승인 대상 13작품을 CANONICAL로 승격한다.

## 2. 신규·갱신 허브 문서

신규:

- `docs/drama_analysis/DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1.md`
- `docs/drama_analysis/DRAMA_ENSEMBLE_TRACKING_AND_EDGE_SELECTIVITY_POLICY_V1.md`
- 이 세션 README

갱신:

- `docs/drama_analysis/README.md`
- `docs/drama_analysis/DRAMA_ANALYSIS_AUTHORITY_INDEX_V3.md`
- `docs/drama_analysis/DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V3.json`
- `docs/drama_analysis/DRAMA_ANALYSIS_DATABASE_STATUS_2026-07-15.json`

## 3. 싸인 분석 결과

```text
status: CANONICAL_STAGE01_04
episodes: 20
SceneCard: 1,358
EpisodeMeta: 20
SequenceBlueprint: 235
EpisodeArc: 20
CharacterArc: 100
RelationshipArc: 80
LocalEdge: 60
PayoffCandidate: 40
CandidateDisposition: 40
CrossEpisodeEdge: 36
FullSeriesArc: 1
errors: 0
warnings: 0
auto boundary bridge: 0
EXT6: false
```

앙상블 적용:

- 회차당 CharacterArc 5건
- 회차당 RelationshipArc 4건
- LocalEdge는 회차당 3건 수준으로 선별
- 후보 40건 전수 처분

이 수치는 다른 작품의 고정 할당량이 아니라 적용 사례다.

싸인 독립 artifact:

```text
싸인_stage01_04_upgraded_full_series_v1.zip
SHA256 b62649d0e0f48d0a75ba2269ca97c82cff8358386ed63124f3eb39d9c3b85a79
```

## 4. CANONICAL 승격 13작품

사용자 승인 근거: `USER_APPROVED_AFTER_HUB_AUTHORITY_LOAD`

| 작품 | artifact SHA256 |
|---|---|
| W | `3970923a69c196686a655bac625d393111353428d245e60ab7575c6507ac5f00` |
| 경성스캔들 | `8160135dd048f6c589006b249ddd5a76d2b5e5348f7a1a7f742e2c8a298dcabe` |
| 미안하다사랑한다 | `4ea4cf68855d1c6678f85a36b5aa11b31dcd12ce89cab40461a42b957e6dc93f` |
| 밀회 | `70905d4d721baf421231bca1917f379ff2b0333e2839478cc8dda409c7f619e9` |
| 더킹투하츠 | `d2351d8aa924295488388195dd4422a7f2fbc0c8cc7bcf25abdcdc9e1db04a10` |
| 뉴하트 | `a21da3734355b0986d31f169f774556e41cd412fb418b32ec2a4fe0f9dd203e3` |
| 킬미힐미 | `9e99ad30a51f493bb4f930de8fe627d1f2c6e829701e4089dece002aade1dfa0` |
| 하얀거탑 | `ea586d28c40ee8d593cc1a901b5b32bc92d697ae2161d222c0fa5e65ee61d479` |
| 마왕 | `3492e02b46a146a64eea770b6e29dfd4f90bcc9fbf5bf506bc2059e03def964e` |
| 스카이캐슬 | `6bb3b2be722c13ddcc73d06777eefe773df4e31a080d840d7837e783a0d51663` |
| 궁 | `7561c9c1688e6e13d8374b6faaeead6893af34ebd1e928a3a789ea1c3ee900e0` |
| 카인과아벨 | `80f67b0e0bb471a444185e9f3cf44c83ffdb730a9a7ae585598bd0997d324bbf` |
| 싸인 | `b62649d0e0f48d0a75ba2269ca97c82cff8358386ed63124f3eb39d9c3b85a79` |

승격 범위에 EXT6은 포함하지 않는다.

## 5. 오늘 연속 업그레이드 결과

이번 진행 계보에서 새로 완료한 작품:

```text
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

초기 상태 34완료에서 최종 43완료로 증가했다.

## 6. 최종 데이터베이스

```text
works: 49
episodes: 938
SceneCard: 58,945
Stage01~04 complete: 43
remaining: 6
```

artifact:

```text
seqcard_ko_stage04_progress_W_dream_gangnam_gyeongseong_misa_milhwe_theking_newheart_killme_whitetower_mawang_skycastle_gung_kain_sign_v1.zip
SHA256 2c1059eeecec38961f8e15ba68240bf4217b3996cf9318d5e29795b7a44932a6
```

검증:

```text
modified scope errors: 0
modified scope warnings: 0
ZIP CRC: PASS
internal SHA256: PASS
fresh extraction: PASS
```

기존 `개와늑대의시간` EpisodeArc 숫자 행 레거시는 이번 변경 범위 밖의 관찰로 보존한다.

## 7. 남은 6작품

| 작품 | 상태 | 다음 조건 |
|---|---|---|
| 공주의남자 | 정상 후보 | 원본·Stage01/02 preflight 후 진행 |
| 녹두꽃 | 정상 후보 | 원본·Stage01/02 preflight 후 진행 |
| 모래시계 | 정상 후보 | 원본·Stage01/02 preflight 후 진행 |
| 역전의여왕 | Stage02 재저작 필요 | 31회를 8회차 블록으로 계획 |
| 최강칠우 | SOURCE_HOLD | 실제 EP03 정본 확보 |
| 대장금 | 최종 장편 | 사용자 지시대로 가장 마지막, 8회차 블록 |

## 8. 최강칠우 복구 경계

허용:

- 실제 EP03 정식 대본 확보
- 합법적 방송본·자막 기반 `RECONSTRUCTED_SOURCE_CANDIDATE` 별도 계보

금지:

- 중복 EP02를 EP03으로 사용
- EP02와 EP04 사이를 추정·창작
- 줄거리만으로 SceneCard 생성

## 9. 새 대화창 다음 진입점

```text
README
→ DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V1
→ SCHEMA_CONTRACTS_V2
→ DATABASE_STATUS
→ 공주의남자/녹두꽃/모래시계 중 한 작품 preflight
```
