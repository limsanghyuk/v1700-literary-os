# R21 Pure GPT → Literary OS Sequence Planning Ablation — Final Report

**Date:** 2026-08-19 KST  
**Final status:** `PARTIAL_SUPPORT_PRIMARY_PREREG_GATE_FAIL`  
**Scientific class:** internal blind-forward ablation; not independent causal certification.

## 1. Why this experiment was run
The prior V2 benchmark used a B baseline that already received Literary OS PlanningContext/R5/THICK and an explicit Sequence schema. Therefore B=71 could not be interpreted as a pure generic-GPT baseline.

This experiment added the missing baseline and progressively layered the system:
- **A0 Pure GPT:** plain EP08 recap only; generic instruction to design 5–10 next-episode sequences. No THICK/R5/thread/debt/Boundary/schema/EpisodePlan/retrieval.
- **A1 Rich State, no grammar:** richer N-1 facts flattened into ordinary prose; still no Literary OS field names or design grammar.
- **B Literary OS state + Sequence grammar:** N-1-safe PlanningContext/R5 + EP08 THICK tail + explicit dominant transaction/goal/obstacle/turn/value-shift/state/terminal grammar.
- **C Hierarchical:** B plus self-authored EpisodeSynopsisPlanLite before SequencePlan.
- **D Retrieval + Hierarchical:** C plus five distinct cross-work EpisodePlan cases, abstracted to design patterns.

Fresh holdouts: `난폭한로맨스 EP09`, `닥터챔프 EP09`, `드림 EP09`.
All 15 outputs were frozen by SHA256 before target EP09 EpisodeArc/EpisodePlan/THICK were opened.

## 2. Neutral 100-point semantic rubric
- causal continuation plausibility: 20
- dramatic progression / escalation: 20
- character & relationship progression: 15
- information / unresolved-problem management: 15
- episode architecture / terminal pressure: 15
- sequence-to-sequence causality: 10
- originality / leakage: 5

The evaluator scores semantic quality, not the presence of Literary OS field labels.

## 3. Results

| Target | A0 Pure | A1 rich state | B LOS grammar | C hierarchy | D retrieval |
|---|---:|---:|---:|---:|---:|
| 난폭한로맨스 EP09 | 65 | 81 | 82 | **84** | 83 |
| 닥터챔프 EP09 | 73 | 76 | 80 | **82** | **82** |
| 드림 EP09 | 65 | **75** | 73 | **75** | **75** |
| **Median** | **65** | **76** | **80** | **82** | **82** |
| Mean | 67.7 | 77.3 | 78.3 | 80.3 | 80.0 |

Median increments:
- A1 − A0 = **+11**
- B − A1 = **+4**
- C − B = **+2**
- D − C = **0**
- D − A0 = **+17**

## 4. Preregistered gate
Rules:
1. B >= A0 + 8 → **PASS** (80 vs 65)
2. C >= B + 3 → **FAIL** (+2 only)
3. D >= C − 1 → **PASS**
4. D >= A0 on all 3 targets → **PASS**

Overall preregistered primary gate: **FAIL (3/4 conditions pass)**.
This is not a failed project result. It means the strongest claim—every planned layer adding the preregistered minimum—did not reproduce.

## 5. Interpretation
### Can generic GPT reach around 71?
Yes, on some episodes. With only a plain recap, `닥터챔프 EP09` scored **73** because EP08 strongly implies the next dramatic direction: confession → rehabilitation → return attempt. So a 71-level result is not inherently impossible for a strong base model.

But across three fresh works, A0 median was **65**, not 71. The earlier B=71 was also not pure GPT; it was already Literary-OS enhanced.

### Where did Literary OS add the most value?
The largest gain was **rich state representation**: A0 65 → A1 76 (**+11** median). Correctly preserving character states, relationship deltas, and unresolved problems mattered more than any later single layer in this sample.

Adding structured Literary OS state/THICK and explicit Sequence grammar gave another **+4** median (A1 76 → B 80). This supports added value, but B−A1 is not a pure grammar-only effect because B also changes representation structure and adds THICK-tail information.

### Did EpisodeSynopsisPlan-first hierarchy replicate the prior +5?
Not fully. C−B was **+2**, positive but below the preregistered +3 threshold. The previous +5 internal signal should not be treated as a stable effect size yet.

### Did retrieval help?
No measurable aggregate gain here: D−C = **0** median. Retrieval remained safe—no high-specificity story/dialogue copying—but did not improve target design selection.

## 6. Most important failure: 드림 EP09
The Literary OS arms saw the open `도필 vs 장석`, injury-risk, market-control, and licensing threads and built a coherent episode around a dangerous official match.

The canonical episode made a different and stronger choice: **the monopoly organization cancels the tournament and removes the athletes' right to compete.** The episode becomes a market-power / survival-alliance story, not a dangerous-match story.

This reveals a key bottleneck:
> More correct state information can make the wrong plan more confidently structured if the system selects the wrong episode axis or escalation level.

Therefore the next priority is not adding more fields. It is learning **which active thread should dominate now, which should be suppressed/deferred, and at what escalation level the episode should operate**.

## 7. Deterministic diagnostics
Canonical Sequence counts: 10 / 7 / 7.
Mean absolute count error:
- A0: **1.00**
- A1: **1.33**
- B: **1.33**
- C: **1.33**
- D: **1.33**

This experiment did **not** reproduce a Sequence-count advantage for Literary OS. Count remains a prior/diagnostic, not a quota.

No clear target-only future phrase leakage was found in frozen outputs, and D had no high-specificity copied names/dialogue/events from retrieved works.

## 8. Scientific limits
1. Generator and semantic evaluator are the same assistant session; no independent scorer.
2. Base-model pretraining knowledge of broadcast dramas cannot be excluded.
3. A0 is not zero-processing raw SOURCE: it receives a short plain recap distilled from EP08 EpisodeArc. It tests removal of Literary OS planning grammar, not raw-script summarization quality.
4. Only three works.
5. Input information volume differs by arm; A1−A0 is deliberately the state-representation effect, not a same-token control.
6. Retrieval is a simple current-case search, not a learned ranker.

## 9. Final interpretation
- Base GPT next-sequence planning: **REAL BUT VARIABLE**.
- Rich N−1 state representation: **STRONG POSITIVE INTERNAL SIGNAL**.
- Literary OS structured representation + Sequence grammar beyond rich prose: **POSITIVE INTERNAL SIGNAL (+4 median)**.
- EpisodePlan hierarchy: **WEAK/MODERATE POSITIVE, PRIOR +5 NOT REPLICATED (+2)**.
- Retrieval: **NO AGGREGATE INCREMENT IN THIS RUN**.
- Full stack vs plain recap: **+17 median internal difference**, but not formal causal certification.

### Next experiment
Focus on **Episode Axis Selector / Escalation-Level Predictor / Thread Suppression-Deferral policy**. Then rerun this exact A0→A1→B→C→D ablation on a larger fresh set with independently blinded scorers.