# 《궁》 EXT6 EP02 원문–Stage01 순서 충돌 감사

Status: `SOURCE_ORDER_CONFLICT_HOLD`

## 권위

- Method: `EXT6_SINGLE_AUTHORITY_V1_2`
- Schema: `EXT6_EXACT_SCHEMA_REGISTRY_V1_1`
- Gold anchor: 《비밀의숲》
- Trusted baseline: `DB90_EXT6_14WORKS_WINDOWS_COMPATIBLE_FIXED_20260730.zip`
- Baseline SHA256: `901b266b696dc683cd95eeaeb5ca9e0233ce93a054a52c2f2c993564abcdb829`

## 발견 사항

《궁》 EP02의 원문 물리 순서는 다음과 같다.

```text
Scene 30: L1571
Scene 42: L1604–1753
Scene 43: L1754–1798
Scene 44: L1799–1951
Scene 31: L1952–1966
Scene 32 이후
```

Stage01 ordinal은 다음과 같다.

```text
30 → 31 → 32 → ... → 41 → 42 → 43 → 44
```

따라서 Stage01을 byte-exact로 보존하면 Scene 42~44가 Scene 31보다 앞선 원문 구간을 참조하게 되어 V1.2의 source fragment 증가·비중첩 규칙을 위반한다.

기존 자동 alignment checkpoint는 Scene 42~44를 L2261–2428의 가족 장면에 강제 귀속했다. 이 근거는 장면 의미와 일치하지 않으므로 EP02 checkpoint는 승격 금지·무효 처리한다.

## 상태

- 24회 alignment checkpoint: 생성됐으나 최종 승격 전 상태
- EP02 checkpoint: `INVALIDATED_NOT_PROMOTED`
- Stage01~04 변경: 0
- EXT6 완료 패키지: 생성하지 않음
- DB 편입: 수행하지 않음
- 신뢰 EXT6 완료 작품 수: 14 유지

## 해결 조건

1. core Stage01 거버넌스에서 EP02 ordinal과 정본 원문 중 어느 계보가 권위인지 확정한다.
2. Stage01 ordinal 교정이 승인되면 EXT6가 아니라 core 계층에서 supersession을 기록한다.
3. 권위 충돌 해소 후 EP02 alignment와 파생 계층만 다시 생성한다.
4. 다른 회차 checkpoint는 블록 강검사 후 재사용한다.

EXT6 내부에서 장면 번호를 임의 재배열하거나 무관한 원문 줄에 근거를 제조하지 않는다.
