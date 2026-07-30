# 굿캐스팅 EXT6 품질 동급성 재감사

- 기준 권위: `EXT6_SINGLE_AUTHORITY_V1_2`
- exact schema: `EXT6_EXACT_SCHEMA_REGISTRY_V1_1`
- gold anchor: `비밀의숲`
- 판정: `QUALITY_HOLD_REAUDIT_REQUIRED`

## 확인된 통과 범위

- SourceSceneAlignment 1,020 / 1,020
- CastPresence 2,702
- schema violation 0
- alignment overlap 0
- source evidence mismatch 0
- evidence outside alignment 0
- evidence cross-scene reuse 0
- alias collision self-report 0
- baseline modification 0
- ZIP CRC / Fresh Extraction PASS

이는 구조와 원문 근거 containment가 통과했다는 뜻이다.

## 기준작과 동급 판정을 막는 결손

V1.2 단일 권위는 EntityRegistry, EntityBridge, SourceHeadingRegistry, SourceSceneAlignment, CastPresence, CastCoverageLedger, CharacterLoad뿐 아니라 RiskAudit, SelectiveAppendLedger, FunctionalHoldout 또는 승인된 대체 수동 의미 게이트까지 요구한다.

현재 굿캐스팅 완료 요약에는 다음 증빙이 없다.

1. RiskAudit 후보 수와 고위험 후보별 직접 독해 판정
2. accepted / rejected / unresolved disposition
3. SelectiveAppendLedger와 기존 Stage03 비중복성 검사
4. 독립 FunctionalHoldout 또는 수동 Source Evidence Semantic Gate
5. 위험 presence mode와 generic entity를 대상으로 한 독립 의미품질감사

## 이상 신호

- empty-cast scenes: 176 / 1,020 = 17.25%
- entity registry: 196
- REFERENCED_ONLY: 598 / 2,702 = 22.13%
- CastPresence per scene: 2.65

비교값:

- 비밀의숲: 3,763 / 1,037 = 3.63 CastPresence per scene; RiskAudit 55, accepted 22, rejected 33
- W: 3,063 / 1,220 = 2.51; RiskAudit 30, accepted 17, rejected 13
- 강남엄마따라잡기: 5,117 / 1,246 = 4.11; RiskAudit 34, accepted 17, rejected 17
- 개와늑대의시간: 3,087 / 880 = 3.51; RiskAudit accepted 8, rejected 9
- 구해줘: empty-cast 28 / 903 = 3.10%
- 국희: empty-cast 82 / 1,287 = 6.37%

굿캐스팅의 CastPresence 밀도 자체는 W 범위와 유사하므로 단독 실패 근거가 아니다. 그러나 빈 장면 비율, 높은 entity 수, 높은 REFERENCED_ONLY 비중은 수동 재감사 우선순위가 높다는 신호다.

## 결론

현재 패키지는 `STRUCTURAL_EVIDENCE_PASS`이다. `FULL_V1_2_EXT6_COMPLETE`는 아니다.

14작품 통합 승인을 철회하고 13작품 정본으로 롤백한다. 다음 작품 궁은 굿캐스팅이 아래를 통과할 때까지 진행하지 않는다.

- 176개 empty-cast 장면의 speaker-turn 전수 확인
- 196개 entity의 alias / generic noun / role split 감사
- VOICE_ONLY, PHONE_OR_REMOTE, ARCHIVAL_OR_MEMORY, REFERENCED_ONLY 위험 표본 직접 대조
- RiskAudit 전 시즌 작성
- accepted / rejected / unresolved disposition
- SelectiveAppendLedger 또는 전건 REJECT 원장
- 최종 record freeze 후 감사 재계산
- 작품 단위 Fresh Extraction
