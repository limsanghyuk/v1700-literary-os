# 26작 CANONICAL 품질 균질성 정밀 감사 — 2026-08-14

## 최종 판정
**STRUCTURAL_CANONICAL_PASS / QUALITY_HOMOGENEITY_FAIL**

현재 26작은 semantic-independence V3, exact/provenance, PlannerInput R5/Runtime R8 구조 게이트는 26/26 PASS다.
그러나 동일 품질이라고 보기는 어렵다. 같은 평가표로 전수 재측정하면:

- A_STABLE: 7작 — 가을동화, 건빵선생과별사탕, 검사프린세스, 구해줘, 국희, 닥터챔프, 돌아온일지매
- B_REVIEW_VARIANCE: 11작 — 결혼못하는남자, 굿캐스팅, 궁, 그저바라보다가, 난폭한로맨스, 내여자친구는구미호, 내이름은김삼순, 대물, 더킹투하츠, 도깨비, 드림
- C_REPAIR_REQUIRED: 8작 — 101번째프로포즈, 강남엄마따라잡기, 개와늑대의시간, 경성스캔들, 공주가돌아왔다, 너의목소리가들려, 녹두꽃, 뉴하트
- 기존 15작 Q25 하한 4지표를 모두 통과: 16/26
- 하나 이상 미달: 10/26
- SourceLock direct_reading_attested=true: 14/26
- 직접독해 attestation 미복구/retroactive: 12/26

## 핵심 발견
1. **Stage01 skin 품질 편차가 가장 크다.** 권위 정의상 skin은 장소·시간·표면행동·소품의 구체성을 담아야 한다. 그런데 녹두꽃은 1,636/1,636장이 동일 문구, 너의목소리가들려는 99.7%, 경성스캔들은 91.2% exact 반복이다.
2. **THICK cast 기능 반복을 기존 strict gate가 일부 놓친다.** 인물명 prefix를 제거하면 공주가돌아왔다 16.7%, 뉴하트 13.8%, 강남엄마따라잡기 10.0%가 동일 시퀀스 안에서 같은 기능 본문을 서로 다른 인물에게 공유한다.
3. **THICK 밀도도 균일하지 않다.** 기존 Q25 4지표 전부를 통과하는 작품은 16/26이다. 개와늑대의시간은 1/4, 공주가돌아왔다·너의목소리가들려·101번째프로포즈·결혼못하는남자는 2/4다.
4. **Stage02 의미 필드 밀도 하위권이 별도로 존재한다.** 개와늑대의시간과 너의목소리가들려는 sequence_intent+goal+obstacle 평균 총량이 각각 약 54.8자, 57.5자로 26작 최하위다.
5. **계보/세션 차이와 품질 편차가 상관한다.** direct_reading_attested=true 14작의 Q25 평균 통과 수는 3.71/4, attestation 미복구 12작은 3.00/4다. Stage01 skin 반복률도 각각 18.3% 대 35.4%다. 다만 인과관계 단독 증명은 아니다.

## C_REPAIR_REQUIRED 직접 표본 확인

### 101번째프로포즈
직접 표본에서 cast 기능에 원문 대사·지문이 길게 혼입되고 '이 시퀀스에서는' 템플릿이 보임. info 0.70, plant/payoff 0.72로 기존 Q25 하한 미달, Stage01 skin 반복 42.2%.

### 강남엄마따라잡기
동일 시퀀스 내 서로 다른 인물의 cast 기능 본문 반복이 약 10.0%. 예: EP01 S01 서상원·이미경에 동일 본문. plant/payoff 1.06으로 기존 Q25 하한 1.17 미달.

### 개와늑대의시간
직접 표본에서 cast desire_or_function이 '지우: 조심해요!', '수현: 머리 숙여!' 등 원문 대사/행동 조각 수준으로 남아 기능 서술 품질이 낮음. Q25 4지표 중 1개 통과, Stage02 의미필드 총길이 최저.

### 경성스캔들
Stage01 skin exact 반복 91.2%(주로 '시대극 로맨스/멜로/스릴러'). THICK cast 평균 51.95자로 기존 Q25 하한 54.85 미달.

### 공주가돌아왔다
동일 시퀀스에서 서로 다른 인물에게 동일 cast 기능 본문을 부여한 비율 16.7%. EP01 S01에서 장공심·차도경 기능문이 사실상 동일. event 평균 79.54자, info 0.95.

### 너의목소리가들려
Stage01 skin 1,080장면 중 1,028장이 동일 '법정스릴러/초능력로맨스'. THICK cast 기능 본문 exact 반복 45.5%. 첫 표본은 event에 '첫사랑 존재 공개'가 있으나 info_shift 0으로 정보변화 포착 누락 신호.

### 녹두꽃
Stage01 skin 1,636/1,636이 동일 '사극대서사/동학농민운동'으로 현행 skin 정의와 불일치. THICK 자체는 밀도와 출처 근거가 강해 Stage01 중심 보강이 적절.

### 뉴하트
동일 시퀀스 내 cast 기능 본문 중복 13.8%. 예: EP17 S01에서 최강국·김정길에 같은 사건문을 각각 부여. THICK 전체 밀도는 높아 해당 cast 기능 중심 선택 보강이 적절.

## 보강 원칙
- **26작 전체를 처음부터 재분석하지 않는다.**
- 기존 26작 정본은 보존하고 별도 quality-repair staging에서 작업한다.
- 문제 필드만 원문을 다시 직접 읽어 선택 재저작한다.
- Stage01이 바뀌면 SceneCard hash에 의존하는 THICK source_hash를 재결속하고 downstream R8까지 stale 여부를 재검증한다.
- THICK cast/info/event가 바뀌면 해당 episode R8을 재생성한다.
- 각 작품은 repair 전/후 동일 평가표와 직접-source sample gate를 통과한 뒤에만 quality-equalized authority로 승격한다.
- 기존 strict validator에 `character-prefix-stripped cast duplicate`, `Stage01 skin specificity/repetition`, `Q25 all-work parity` 검사를 추가해야 한다.

## 결론
현재 26작은 **파일·스키마·provenance closure 측면에서는 정본이지만, 의미 저작 품질이 동일한 수준으로 균질화됐다고 말할 수 없다.**
사용자가 지적한 “세션마다 방법을 다시 학습하고 서로 다른 lineage가 누적되는 구조”는 실제 데이터의 author lineage와 품질 편차에서 상관 신호가 확인된다.
