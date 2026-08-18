# Drama Analysis EpisodeSynopsisPlan Handoff Manual R5 — CURRENT 2026-08-18

## 0. Current authority

- Stage01–04 corpus: **98 works**
  - 97 `V10_1_EQUIVALENT_CANONICAL`
  - 1 `SOURCE_HOLD_FAIL_CLOSED` (`최강칠우`)
- CANONICAL THICK / Boundary-qualified cohort: **38 works**
- Stage02 = THICK membership: **6,357 = 6,357**
- EpisodeSynopsisPlan: **38 works / 714 episodes / 6,357 Sequence allocations**
- Active schema: **EpisodeSynopsisPlan.v0.3-r1**
- R5 PlannerInput: **714**
- R8 Runtime: **714 / 46,078 scenes**
- Deep Semantic R2 reinforcement is current for:
  `개인의취향`, `수호천사`, `미안하다사랑한다`, `미생`.
- `미생` enhanced integrated scope in the supplied reinforced package is **EP01–EP11 only**.
- CT-13 R3 formal verdict: **UNDECLARED**.
- CT-13 diagnostic result: **strong PASS-like incremental utility support**.
- Autonomous forward EpisodePlan generation/control: **EXPERIMENTAL_HOLD**.

## 1. EpisodeArc and EpisodeSynopsisPlan are different layers

`EpisodeArc` is retrospective structural description of what the episode became.
`EpisodeSynopsisPlan` is the explicit episode-design decision layer that explains:

1. which dramatic axes move **now**;
2. why those axes move in this episode;
3. what must be deferred;
4. which inherited debts are paid / escalated / carried / retired;
5. what terminal regime is targeted;
6. what exit state must be handed to the next episode;
7. which Sequence owns each planned function.

Do not collapse EpisodeSynopsisPlan into an EpisodeArc paraphrase.

## 2. Mandatory information-cut rule for an existing broadcast drama

For every episode N:

1. Before reading target episode N, freeze `EpisodePlanningContext.R1` using only information available through N-1.
2. Then directly read N SOURCE and execute Stage01 → Stage02+Boundary → Stage03 → Stage04 → THICK.
3. After target N has been analyzed, author a `REVERSE_ENGINEERED_CASE` EpisodeSynopsisPlan.
4. The reverse-engineered plan may explain the episode that was actually observed, but the frozen N-1 planning context must never be retroactively contaminated.
5. Never put future payoff dates, post-N facts, target-episode SOURCE prose, or retrospective THICK payoff prose into planner-visible N-1 input.
6. Python may extract/hash/serialize/validate. Python may not invent episode axes, deferral reasons, debt meaning, terminal rationale, or dramatic design logic.

## 3. Required semantic responsibilities

A canonical reverse-engineered plan must contain meaningful, episode-specific decisions for:

- `episode_axis`
- `why_this_episode`
- `deferred`
- `debt_ledger_delta`
- `terminal_design`
- `exit_state_target`
- `sequence_allocation`

The text must not be a stock template with names substituted.
Corpus medians are diagnostics, never targets.

## 4. Hard gates

- EP0 — N-1 information cutoff / planning-context purity.
- EP3 — exact adjacent handoff when both neighboring plans exist.
- EP6 — every inherited active debt is accounted for.
- EP8 — every current Stage02 Sequence is owned exactly once by the plan allocation.
- Exact schema / ID / episode continuity.
- Stage02↔THICK↔Plan allocation parity.
- R5 debt parity.
- No future-information leakage in planner-visible input.

HOOK frequency, equal-cut suspicion, Sequence count, turning-point position, and debt volume are review priors only.

## 5. Boundary interaction

If Stage02 Sequence membership changes:

`SOURCE re-read → BoundaryEvidenceR1 → Stage02 change → EpisodeArc/Stage03/Stage04 semantic impact audit → THICK re-author/rebind as needed → EpisodeSynopsisPlan allocation/reasoning re-audit → R5/R8 rebuild → Thread/Subplot/Deep Semantic → fresh extraction`.

Never preserve an old plan allocation merely because the plan still parses.

## 6. Current 4-work R2 reinforcement rule

For `개인의취향`, `수호천사`, `미안하다사랑한다`, `미생`:

- Stage01–04 and Sequence membership remained unchanged during R2 reinforcement.
- THICK semantic prose was reinforced.
- selected EpisodePlan prose/debt parity was reinforced.
- R5/R8 were rebuilt from final THICK.
- one real integration defect was found and repaired:
  `미안하다사랑한다 EP16 / MISA_MUHYEOK_MINJU_REVENGE_SEDUCTION → PAID`.
- after repair, EpisodePlan self-check is **714 plans / HARD 0**.

## 7. CT-13 R3 scientific boundary

The external Claude renderer produced 48/48 sealed outputs.
Same-session robustness diagnostics strongly favored the work-specific C plan over B and mismatched N.
However preregistration required genuinely separated blind scorer sessions.
Therefore:

- formal verdict = **UNDECLARED**
- reverse-engineered 38-work EpisodePlan corpus = **CANONICAL**
- autonomous forward-generation causal-control claim = **NOT CERTIFIED**
- forward plan generation remains **EXPERIMENTAL_HOLD**

Do not rerun or mutate the sealed renderer merely to obtain a favorable verdict.

## 8. New-work promotion

A genuinely new drama may be promoted only after:

`SourceLock → Stage01 → Stage02+Boundary → Stage03 → Stage04 → THICK → EpisodeSynopsisPlan → R5/R8 → exact/provenance → Semantic V3 → Owner/Grounding → Depth → Thread R2 → Subplot distinctness → Deep Semantic DS1–DS4 → artifact hash → fresh extraction`.

For an already broadcast work, EpisodeSynopsisPlan is authored after SOURCE analysis while preserving the pre-read N-1 planning-context freeze.
For original creation, `FORWARD_GENERATED` EpisodeSynopsisPlan remains experimental until a separate blind forward-plan experiment proves the planner can create a good plan from N-1 state alone.
