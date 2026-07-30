# 《궁》 EXT6 EP02 원문–Stage01 순서 차이 감사

Status: `RESOLVED_WITH_PHYSICAL_SOURCE_ORDER_SERIALIZATION`

## 권위

- Method: `EXT6_SINGLE_AUTHORITY_V1_2`
- Schema: `EXT6_EXACT_SCHEMA_REGISTRY_V1_1`
- Gold anchor: 《비밀의숲》
- Baseline: `DB90_EXT6_14WORKS_WINDOWS_COMPATIBLE_FIXED_20260730.zip`
- Baseline SHA256: `901b266b696dc683cd95eeaeb5ca9e0233ce93a054a52c2f2c993564abcdb829`

## 발견 사항

EP02 원문 물리 순서:

```text
Scene 30: L1571
Scene 42: L1604–1753
Scene 43: L1754–1798
Scene 44: L1799–1951
Scene 31: L1952–1966
Scene 32 이후
```

Stage01 scene ID 순서:

```text
30 → 31 → ... → 41 → 42 → 43 → 44
```

최초 자동 checkpoint는 단조 scene_no를 강제하면서 Scene 42~44를 L2261–2428의 무관한 가족 장면에 잘못 귀속했다. 이 intermediate checkpoint는 superseded 처리했다.

## 해결 방식

Stage01을 수정하거나 scene_no를 재발번하지 않았다.

- SourceSceneAlignment JSONL을 **원문 물리 순서**로 직렬화했다.
- 각 레코드의 immutable `scene_no`는 그대로 보존했다.
- Scene 42~44와 Scene 31의 차이는 `LOGICAL_REHEADING` 또는 `MERGED_SOURCE_HEADINGS_WITH_LOGICAL_REHEADING`, `VERIFIED_MANUAL_OVERRIDE`, alignment note로 기록했다.
- validator는 JSONL의 물리 source offset 증가·비중첩과 scene_no의 전집합 유일 귀속을 각각 검사했다.

## 검증 결과

- SceneCard/alignment: 1,089/1,089
- source offset 역행: 0
- source interval 중첩: 0
- evidence mismatch: 0
- 장면 밖 evidence: 0
- 장면 간 동일 evidence 재사용: 0
- Stage01~04 변경: 0
- 허위 근거 귀속: 0

## 최종 상태

- 《궁》 EXT6 V1.2 전체 계층: PASS
- individual package: `궁_EXT6_APPEND_ONLY_EVIDENCE_FIXED_20260730.zip`
- integrated database: `DB90_EXT6_15WORKS_WINDOWS_COMPATIBLE_FIXED_20260730.zip`
- 버전 상승: 없음
- 자동 CANONICAL 승격: 없음
