# 0009: "Biggest difference" sentences in the comparison panel

- **Status:** PROPOSED
- **Decided by:** 
- **Proposed by:** Claude Code, 2026-11-10, answering DQ-30 (owner: Claude Code drafts, Rey approves). Rey sets ACCEPTED.
- **Requirement IDs:** R15, R28, R39, R43, BE-24
- **Supersedes / overrides:** none. The spec asks for computed sentences but gives no rule.

## Context

- **Channel comparison:** "One computed sentence names the largest difference (never hard-coded text)" (`upstream/design-pack/03-product-spec-v0.4.md:430`).
- **Host comparison:** "1–3 sentences computed from the numbers, from per-language templates" (`upstream/design-pack/03-product-spec-v0.4.md:653`).
- Generated text comes from per-language templates, never from translating English output (`upstream/design-pack/03-product-spec-v0.4.md:177`).

**What the mockup shows** (verified 2026-11-12 against artifact `Y6meVMkfzS7bB1NL7mszHB` at version `1794283411-4173`, as in `upstream/PIN.md`; both sentences are the same as in the 2026-11-10 read of a different artifact, `1793933571-41ce`). Both sentences are **fixed strings**, not computed:
- Board 1.1 Overview, channel comparison (`project/Main.dc.html`): "self-operated rooms convert entrants about 10× better (CVR 2.23% vs 0.22%), while influencer sessions bring in 2.8× the entry rate and 2.1× the GMV per session."
- Board 1.9 Comparison panel, 4 hosts (`project/Comparison-panel.dc.html`): "Thorne悦恩运动极限海外店 converts entrants 7–12× better than the three influencers (CVR 1.99% vs 0.17–0.30%). LisaWang（15号悦恩活动） brings the largest basket (AOV ¥2,115) and the most GMV (¥1.04M)."

**No single rule reproduces both sentences.** The channel sentence leaves out AOV, where influencers lead 3.7×, a bigger gap than the 2.8× and 2.1× it names. The host sentence names AOV and Total GMV but not GMV per session, which is the biggest gap at 10.6×.

So decision 0004 ("the mockup's behaviour wins") gives the **shape** to keep: CVR first, then what the other side is best at, with ratios. The selection rule below is new and needs Rey's approval.

## Decision (proposed)

The full rule is **ALG-41** in [algorithm-spec.md](../algorithm-spec.md). In short:

1. **Candidate metrics, in this order:**
   - CVR; ①–⑤; AOV; Avg GMV / session.
   - Host comparison adds Total GMV and Avg exposure / session.
   - Sessions is never a candidate.
   - These are the comparison's own rows and tiles (`upstream/design-pack/03-product-spec-v0.4.md:428`, `:651`).
2. **Measure: ratio, not pp.** For each metric, the leader is the highest value. `ratio = leader ÷ runner-up`. The fact also carries the range against every other series: `leader ÷ max(others)` to `leader ÷ min(others)`.
3. **A fact is kept only when `ratio ≥ 1.20`.** It is skipped when the top two values tie, the runner-up is 0, or fewer than 2 series have a value.
4. **Selection:**
   - Sentence 1 is the CVR fact, if kept.
   - Each next sentence goes to the leader with the largest remaining ratio who **has not been named yet**, with up to 2 of that leader's facts (largest ratio first).
   - Channel comparison: at most 2 clauses, joined into one sentence with "while" (spec: one sentence).
   - Host comparison: at most 3 sentences.
5. **No fact kept:** one fallback sentence, "No large differences: every compared value is within 20%."
6. **Eligible values:**
   - A series' rate counts only when its pooled input meets the ALG-22 minimum.
   - A host greyed as "Not enough data" (ALG-30, `upstream/design-pack/03-product-spec-v0.4.md:618`, `:944`) is left out of the facts.
7. **Ratio shown:** 1 dp below 10, whole number at 10 or more, half up (ALG-03). A range collapses to one number when both ends are equal.
8. **Who does what:**
   - Score/Serve returns the **facts**: metric, leader, values, ratio, range and template key (BE-24).
   - The sentence is rendered from per-language templates (R39) with locale formatting (R41).
   - No LLM writes or changes these sentences (AGENTS.md rule 9).

**Templates** (en; zh for operator review with spec Q15):

| Key | en | zh |
|---|---|---|
| `cmp.cvr` | "{leader} converts entrants {ratio}× better than {others} (CVR {v_leader} vs {v_others})" | "{leader}的进房成交转化率是{others}的{ratio}倍（{v_leader} vs {v_others}）" |
| `cmp.lead1` | "{leader} brings {ratio}× the {metric} of {others} ({v_leader})" | "{leader}的{metric}是{others}的{ratio}倍（{v_leader}）" |
| `cmp.lead2` | "{leader} brings {ratio1}× the {metric1} and {ratio2}× the {metric2} of {others}" | "{leader}的{metric1}是{others}的{ratio1}倍，{metric2}是{ratio2}倍" |
| `cmp.join` (channel only) | "{clause1}, while {clause2}." | "{clause1}；{clause2}。" |
| `cmp.none` | "No large differences: every compared value is within 20%." | "差异不大：各项对比数值相差均在20%以内。" |

`{others}` is the other series' name when there are 2, else "the other {k} hosts" / "其他{k}位主播". `{ratio}` is the formatted range.

## Consequences

- Score: one pure function from the comparison's values to an ordered list of facts. Golden tests use the ALG-41 examples.
- Contract (BE-24): a `facts[]` array plus template keys; no free text.
- The results differ from the mockup's illustrative wording; see the examples below.

## Evidence

Output of this rule on the mockup's own numbers:

- **Channel (board 1.1):** "Self-operated converts entrants 10× better than Influencer (CVR 2.23% vs 0.22%), while Influencer brings 3.7× the AOV and 2.8× the entry rate of Self-operated."
  - The mockup named entry rate and GMV per session instead; this rule picks AOV because its gap is bigger.
- **Host (board 1.9):** "Thorne悦恩运动极限海外店 converts entrants 6.6–12× better than the other 3 hosts (CVR 1.99% vs 0.17–0.30%). LisaWang（15号悦恩活动） brings 11–13× the GMV per session and 7.1–7.9× the AOV of the other 3 hosts."
  - The mockup said "7–12×" (it rounded 6.6 up) and named Total GMV instead of GMV per session.

## Open questions

1. **Threshold 1.20.** Lower it and small differences make it in; raise it and the fallback appears more often. Rey decides.
2. **Which metrics.** GMV per session and Total GMV usually move together. Should Total GMV be dropped from the candidates?
3. **Wording** of the zh templates, for operator review (spec Q15).
