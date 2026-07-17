# 드라마 분석 권위 인덱스 v4

- Status: `SUPERSEDED`
- Updated: 2026-07-17
- Superseded by: `DRAMA_ANALYSIS_AUTHORITY_INDEX_V5.md`

이 문서는 V2 실행 가이드와 V4 manifest 시기의 역사 권위 인덱스다. 신규 작품 분석과 새 대화창 온보딩에는 사용하지 않는다.

현재 권위는 다음을 따른다.

```text
DRAMA_ANALYSIS_AUTHORITY_INDEX_V5.md
DRAMA_NEW_CONVERSATION_EXECUTION_GUIDE_V3.md
DRAMA_ANALYSIS_PROTOCOL_MANIFEST_V5.json
DRAMA_ANALYSIS_DATABASE_STATUS_V12.json
```

V4 시기 핵심 파이프라인과 경량/강검증 분리 원칙은 보존되지만, 다음 V5 보강이 우선한다.

- 구조 PASS와 의미 품질 PASS 분리
- speed anomaly audit
- exact·masked semantic repetition 강화
- 신규 작품 semantic-quality report 필수화
- Claude Stage03~04 장점의 선택적 채택
- 완료 시 개별 작품 ZIP과 최신 전체 DB ZIP 동시 제공

상세 신규 작품 해설은 `DRAMA_NEW_WORK_DETAILED_PLAYBOOK_V2.md`, Claude 장점 채택은 `DRAMA_CLAUDE_STAGE03_04_STRENGTH_ADOPTION_POLICY_V1.md`를 사용한다.
