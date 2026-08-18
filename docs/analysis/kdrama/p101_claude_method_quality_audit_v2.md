# 101번째프로포즈 EP01~EP15 — Claude 방식 독립 품질 감사 v2

## 최종 판정

`FAIL_STRICT_CLAUDE_GATE_REPAIR_REQUIRED`

- Canonical 승격: **금지**
- 종합 점수: **77/100**
- 내용 품질: **B+ — Stage01·03은 대체로 강하고 원문 근거가 양호함**
- 계약·증거 품질: **C — Stage02 결정적 매핑 실패와 Stage04 보정·증거 계약 경고가 남음**

## 감사 범위

- Stage01 SceneCard: 1,125
- Stage02 SequenceBlueprint: 184
- CharacterArc: 120
- RelationshipArc: 104
- LocalEdge: 182
- PayoffCandidate: 68
- CrossEpisodeEdge: 38

## 통과한 부분

1. Stage01 title·intent_gist 완전 동일 중복 0.
2. 15개 회차의 첫·중앙·마지막 장면 총 45건을 원문과 직접 대조했으며 사실 모순 0건.
3. 미치환 템플릿 변수 0, 의미 필드의 `[EPxx-Sxx]` 표식 0, 반복 4-gram 임계 위반 0.
4. CharacterArc 120건과 RelationshipArc 104건은 인물·관계쌍×회차 렛저이며 같은 회차 evidence 복사 0.
5. Scene coverage, sequence coverage, core_mix 근거, runtime_share, 전역 ID 고유성 통과.
6. CrossEpisodeEdge 38건 모두 source 장면에 대응하는 PayoffCandidate가 존재.
7. 최종 ZIP에는 checkpoint evidence 244개와 quarter/order 관련 파일 61개가 실제 포함됨.
8. ZIP 무결성과 내부 `SHA256SUMS.txt` 검증 통과.

## Hard failure 1 — Stage02 명시 매핑 위반

Claude 설명서의 결정적 매핑과 충돌하는 레코드가 **34건**이다.

- `PUNISH → RISE`
- `REVERSAL/ORACLE/REVELATION → REVEAL`
- `HOOK/CONFLICT → STALL`

기존 validator는 `turn_class`가 4개 버킷 중 하나인지만 확인하고, `turn_type`에서 올바르게 파생됐는지는 검사하지 않았다. 따라서 기존 PASS는 strict Claude gate 기준으로 거짓 양성이다.

## Hard failure 2 — 공개 매핑으로 검증할 수 없는 Stage02 레코드

`REUNION, RESCUE, PERIL, ROMANCE, DESIRE, RELIEF, INTRO`를 `turn_type`으로 사용한 레코드가 **35건**이다. 공개된 매핑표가 이 값을 다루지 않으므로 현재 계약만으로는 `turn_class`의 정당성을 결정적으로 검증할 수 없다.

해결은 둘 중 하나다.

1. `turn_type`을 현재 검증 가능한 레지스트리로 제한한다.
2. 전체 매핑표를 공식 확장하고 양·음성 fixture를 추가한다.

## Stage04 주요 경고

1. CrossEpisodeEdge 38건의 confidence가 전부 `0.98`이다. 근거 강도 차이를 반영하지 않은 상수값이다.
2. `x012`, `x014`, `x033`은 장거리 callback/payoff보다 다음 회차로 직접 이어지는 causal bridge에 가까워 Stage03 gap=1 LocalEdge 재분류 검토가 필요하다.
3. PayoffCandidate 추정 유형과 최종 CrossEpisodeEdge 유형이 달라진 사례 4건에 promotion rationale ledger가 없다.
4. EP11~EP15 PayoffCandidate 수가 회차당 2~5건 권장 범위를 초과한다: EP11 6, EP12 6, EP13 6, EP14 7, EP15 9.

## 연속성·증거 평가

최종 ZIP에 증거가 없다는 이전 초안 판단은 잘못이었다. 실제로 다음이 포함돼 있다.

- `checkpoint_evidence/` 파일: **244개**
- quarter/order 관련 파일: **61개**
- checkpoint evidence 고유 해시: **73개**

다만 244개 중 238개가 67개 중복 그룹에 속한다. 동일 증거가 여러 회차 폴더에 반복 복제돼 있고, 후반 quarter audit는 scene span·hash·PASS 선언 중심이라 anti-gaming·partial Stage02·repair 지표가 충분하지 않다. 따라서 증거는 **존재하지만 단일 계약으로 정규화되지 않았고 과도하게 중복**돼 있다.

## SourceLock 경고

EP01~EP15에서 SourceLock 스키마가 3종으로 갈린다.

- EP01~06: 회차 원본 SHA 중심
- EP07~08: `scene_sha256` dict
- EP09~15: `scene_sha16` list

`source_sha256`는 원본 CP949 바이트 해시로 추정되지만, 최종 패키지 계약에 hash basis가 명시돼 있지 않다. `original_encoding`, `original_bytes_sha256`, `normalized_utf8_sha256`을 분리해야 한다.

## 단계별 평가

| 영역 | 점수 | 판정 |
|---|---:|---|
| Stage01 장면 근거·반게이밍 | 94 | PASS |
| Stage02 시퀀스 계약 | 56 | FAIL |
| Stage03 회차·인물·관계·인과 | 91 | PASS |
| Stage04 전 시즌 fan-in | 69 | CONDITIONAL FAIL |
| 출처·연속성·이식 가능한 증거 | 78 | PASS WITH WARNINGS |

## 필수 수정 순서

1. Stage02 명시 매핑 위반 34건을 sequence별로 다시 읽어 수정한다.
2. 미정의 turn_type 35건은 레지스트리를 제한하거나 공식 매핑을 확장한다.
3. 인접화 causal 3건을 LocalEdge로 옮기거나 Stage04 승격 근거를 기록한다.
4. candidate→cross-edge promotion ledger와 근거별 confidence 정책을 추가한다.
5. SourceLock v2 단일 스키마와 hash basis를 확정한다.
6. checkpoint 증거를 batch 단위로 한 번만 저장하고 quarter audit 필드를 통일한다.
7. 수정 후 사람용 보고서·manifest·validation을 동시에 갱신하고 기존 PASS를 superseded 처리한다.

## 결론

이 패키지는 전량 폐기 대상이 아니다. Stage01과 Stage03은 강한 기반이며 연속 checkpoint 증거도 최종 ZIP에 포함돼 있다. 그러나 Claude strict gate를 적용하면 Stage02의 결정적 매핑 위반과 Stage04의 보정·승격 근거 부족 때문에 **현재 상태로 canonical corpus에 편입할 수 없다.**
