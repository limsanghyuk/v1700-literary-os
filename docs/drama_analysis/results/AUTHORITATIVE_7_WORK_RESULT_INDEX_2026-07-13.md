# GPT 드라마 7작품 authoritative 결과 인덱스

Updated: 2026-07-13  
Status: **PASS_CANDIDATE_AUTHORITATIVE_V3**  
Purpose: 새 세션과 개발자가 7작품의 실제 데이터 규모·패키지·보강 이력·재사용 경계를 빠르게 확인하기 위한 결과 인덱스

## 1. 전체 누적

| 항목 | 합계 |
|---|---:|
| 작품 | 7 |
| 회차 | 115 |
| SceneCard | 7,518 |
| SequenceBlueprint | 1,043 |
| EpisodeArc | 115 |
| CharacterArc | 787 |
| RelationshipArc | 757 |
| LocalEdge | 1,634 |
| PayoffCandidate | 580 |
| CrossEpisodeEdge | 301 |
| QuarterAudit | 460 |
| FullSeriesArc | 7 |

## 2. 작품별 결과

| 작품 | 회차 | Scene | Sequence | CharArc | RelArc | Local | Payoff | Cross | Quarter |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 101번째프로포즈 | 15 | 1,125 | 184 | 120 | 104 | 182 | 68 | 35 | 60 |
| 결혼못하는남자 | 16 | 1,250 | 189 | 89 | 92 | 128 | 38 | 13 | 64 |
| 공주가돌아왔다 | 16 | 1,117 | 160 | 147 | 152 | 477 | 94 | 33 | 64 |
| 시티헌터 | 20 | 1,356 | 171 | 156 | 153 | 463 | 140 | 55 | 80 |
| 내여자친구는구미호 | 16 | 793 | 105 | 96 | 80 | 128 | 80 | 55 | 64 |
| 좋은사람 | 16 | 938 | 114 | 99 | 96 | 128 | 80 | 55 | 64 |
| 파라다이스목장 | 16 | 939 | 120 | 80 | 80 | 128 | 80 | 55 | 64 |

## 3. authoritative v3 패키지

| 작품 | 패키지 | SHA256 |
|---|---|---|
| 101번째프로포즈 | `p101_stage01_04_authoritative_final_v3.zip` | `9fb78c7a95dcf775f70fbeaf99c5f218e5534380e92a27940ba4cec80c0da338` |
| 결혼못하는남자 | `kmn_stage01_04_authoritative_final_v3.zip` | `79a8641abab51eb0f8a72896be8b096474e2224589d374af3556c54bff142f06` |
| 공주가돌아왔다 | `princess_stage01_04_authoritative_final_v3.zip` | `f0c682369dfed99ea9eb8621b7ebe7823f127ea091acc5329bd303f2d3e6de93` |
| 시티헌터 | `cityhunter_stage01_04_authoritative_final_v3.zip` | `871e1abf26256b797e8813768b46423aa2c45afc091f73fd413ce1e23f370414` |
| 내여자친구는구미호 | `gumiho_stage01_04_authoritative_final_v3.zip` | `6d64412f088aa24303a85a0e27abd5d215295ac529692dd4bd06e7ec4a8adfb3` |
| 좋은사람 | `goodperson_stage01_04_authoritative_final_v3.zip` | `e5b8fa92f32172a348737d4d80d99e642cfc4832ca495a7104a74b58519589bd` |
| 파라다이스목장 | `paradise_stage01_04_authoritative_final_v3.zip` | `b5720d6074eae96840d4904065023873227f3eb3a6617b54f9c6339d67b58f50` |

## 4. 작품별 핵심 구조적 가치

### 101번째프로포즈

- 장기 반복 구애가 자기존중·직업 성장·능동적 선택으로 전환되는 멜로드라마 궤적
- 청혼·반지·굽은 나무·기술대회 등 장거리 회수의 복합 사례
- 인물명 정규화와 과거 규약 복구 사례를 포함

### 결혼못하는남자

- 독립과 고립, 생활 규칙과 관계 조정의 차이를 장면·관계 아크로 축적
- 초기 metadata-derived Stage03/04를 폐기하고 인물×회차·관계쌍×회차로 재저작한 대표 복구 사례
- runtime_share·turn registry·Local/Cross 분리를 검증한 앵커

### 공주가돌아왔다

- 경쟁·계급 상처·첫사랑·가족 책임이 우정과 자발적 약속으로 재배열되는 구조
- 높은 LocalEdge 밀도와 다중 관계망을 가진 장르 비교 자산
- 회차 간 bridge 22건을 제거해 계층 경계를 바로잡은 대표 사례

### 시티헌터

- 살인 복수를 공개·원상회복·법적 책임으로 전환하는 정치 액션 시즌 구조
- 20회, 1,356장면의 장기 분석과 140개 후보 전수 disposition 사례
- 국가 범죄·부자 갈등·연애·수사 그래프의 복합 앵커

### 내여자친구는구미호

- 인간화 규칙·생명 교환·차이를 감당하는 사랑의 판타지 로맨스
- 여우구슬·꼬리·100일 계약의 반복 plant-payoff 사례
- marker가 없는 대본에서 재현 가능한 블록 경계를 SourceLock으로 잠근 사례

### 좋은사람

- 정체 교환·친부 살해·형제 경쟁·경찰 수사를 거쳐 혈연보다 윤리적 선택을 택하는 멜로드라마
- 출생 비밀과 회중시계, 조직 잠입, 프레임업의 장거리 회수 사례
- 총 938장면의 identity/revelation 중심 자료

### 파라다이스목장

- 이혼 부부의 목장 소유권·기업 개발·새 연애·가족 상처가 재결합 선택으로 수렴하는 로맨틱 비즈니스 드라마
- EP09~EP16 460장면을 후속 세션에서 직접독해해 전 시즌 완결
- 전 시즌 939장면, 120 Sequence, 80 후보 disposition, 55 CrossEdge의 최신 완료 사례

## 5. 공통 검증 결과

```text
7/7 PASS_CANDIDATE_AUTHORITATIVE_V3
errors 0
warnings 0
```

공통 확인:

- source fidelity
- exact schemas and enums
- sequence coverage/partition/count/runtime/density
- trigger participant presence
- LocalEdge same-episode gap0 causal
- CrossEpisodeEdge full-season fan-in
- PayoffCandidate disposition 100%
- FullSeriesArc actual counts
- QuarterAudit completeness
- fresh extraction
- ZIP CRC and internal SHA
- portable validator
- no raw script export
- no Python semantic generation

## 6. 재사용 경계

이 인덱스는 상위 탐색용이다. 다음 작업에서는 반드시 원 패키지의 장면·시퀀스·아크·엣지로 내려가 근거를 확인한다.

금지:

```text
이 인덱스만으로 장면 의미 생성
작품 간 장면 ordinal 혼합
서로 다른 판본의 Stage 계층 혼합
PASS_CANDIDATE를 사용자 승인 없이 CANONICAL로 승격
```

## 7. 다음 작품

신규 선정에서 위 7작품을 제외한다.

```text
한국드라마04 archive inventory
→ 원본 안정성 평가
→ 다음 미분석 작품 1편 선정
→ SourceLock v2
→ EP01 Q1
```
