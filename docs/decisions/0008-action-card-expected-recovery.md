# 0008: Action Card "Expected recovery" at P50 and P75

- **Status:** PROPOSED
- **Decided by:** 
- **Proposed by:** Claude Code, 2026-11-10, answering DQ-4 ("take it from the mockup's behaviour", owner: Claude Code drafts, Rey approves). Rey sets ACCEPTED.
- **Requirement IDs:** R22, BE-10, AC-1
- **Supersedes / overrides:** none. The spec names the figure (`upstream/design-pack/03-product-spec-v0.4.md:523`) but gives no formula.

## Context

Each Action Card's body has an **Expected recovery** column: "¥ and UV if the stage reached P50, then P75" (`upstream/design-pack/03-product-spec-v0.4.md:523`). The design brief says "extra buyers and ¥" (`upstream/design-pack/01-design-brief.md:123`).

Decision 0004 says the mockup's behaviour wins where the spec is silent. The mockup gives no formula, but it does show concrete numbers. The figures on board "1.4 Session drawer — Action Cards" (`project/Session-drawer-Action-Cards.dc.html`, session S00234, graded against Thorne × Douyin × All types) are reproduced exactly by one formula: move the stage's rate to the target, then carry the extra people through **the session's own downstream rates** to paid buyers, and multiply by the session's GMV per buyer.

Evidence note: the artifact read on 2026-11-10 served version `1793933571-41ce`, not the pinned `1794210096-60c6` (`upstream/PIN.md`). The board's numbers are fixed values in its source, not computed there, so they show the *behaviour*, not code. Everything in the cross-check below is recomputed from those values.

## Decision (proposed)

The full rule is **ALG-40** in [algorithm-spec.md](../algorithm-spec.md). In short, for a graded stage s with session rate `r_s` and target `T ∈ {P50, P75}` of the grading group:

```
if r_s > T: status "above"   (UI: "Already above P50/P75")   no figures
if r_s = T: status "at"      (UI: "At P50/P75")              no figures
else:
  extra_out    = input_uv(s) × (T − r_s)                       # extra people passing stage s
  extra_buyers = extra_out × r_{s+1} × … × r_④                 # stages ①–③: carried to paid buyers
               = extra_out                                     # stage ④: its output is paid buyers
  extra_kept   = paid_buyers × (T − r_⑤)                       # stage ⑤: buyers kept instead of refunded
  extra_gmv    = extra_buyers (or extra_kept) × gpb            # gpb as in ALG-25
```

- Rates are the 4-dp rates (ALG-03). The figures are rounded once each to 2 dp.
- Same group, window and GMV per buyer as recoverable revenue (ALG-25). Same stage minimums as the stage tier (ALG-20): no tier, no figures.
- **Zero downstream conversion.** If any downstream rate is 0 (for example a session with no buyers), the figure is not shown as "+0". It returns `status = "no_downstream_conversion"` and no figures. **Rey decides** (see Open questions).

## Consequences

- Score: one pure function per (session, stage, target), returning `status`, `extra_out_uv`, `extra_buyers` and `extra_gmv`. It sits beside recoverable revenue but is a separate answer (AGENTS.md rule 8).
- BE-10 / contract: each card carries both targets.
- The Action Card text (AC-1) may cite these numbers but never compute them (AGENTS.md rule 9).
- Tests: the ALG-40 worked examples become golden cases, plus the S00234 cross-check as a regression case on synthetic data.

## Evidence

- Cross-check against board 1.4 (S00234: entered 19,672, product-exposed 3,064, clicks 334, buyers 23, refunding 7, GMV ¥48,934.61 → GMV per buyer ¥2,127.59). Mockup value vs this rule:

| Stage | Target | Mockup | This rule |
|---|---|---|---|
| ① | P50 / P75 | Already above / Already above | above / above |
| ② | P50 0.3124 | +23.1 buyers · about +¥49.2K | 23.14 · 49,223.66 |
| ② | P75 0.8120 | +96.9 buyers · about +¥206.2K | 96.95 · 206,261.61 |
| ③ | P50 0.1250 | +3.4 · +¥7.2K | 3.38 · 7,186.47 |
| ③ | P75 0.1984 | +18.9 · +¥40.1K | 18.87 · 40,154.43 |
| ④ | P50 0.0689 | At P50 | at |
| ④ | P75 0.1064 | +12.5 · +¥26.7K | 12.53 · 26,648.06 |
| ⑤ | P50 0.8165 | +2.8 kept buyers · +¥5.9K | 2.78 · 5,911.30 |
| ⑤ | P75 0.9056 | +4.8 kept buyers · +¥10.3K | 4.83 · 10,271.37 |

- The last-digit differences (96.95 vs 96.9, ¥206.3K vs ¥206.2K, ¥40.2K vs ¥40.1K, ¥26.6K vs ¥26.7K) come from this rule using the 4-dp rates of ALG-03, while the mockup appears to have used unrounded rates. Either way the rule is the same.
- `upstream/design-pack/02-prototype-data.json` › `featured_sessions.influencer_example.action_cards` (generator output, against the Influencer group) follows the same propagation. Example: ② to P50 0.2711 → 17.0 buyers. Its values are not expected outputs (`tests/golden/README.md`).

## Open questions

1. **Zero downstream conversion** (a session with 0 buyers, or 0 clicks). Options:
   - a) status `no_downstream_conversion`, no figures (proposed);
   - b) show +0;
   - c) substitute the group's P50 for the missing downstream rates.

   (a) is honest. (c) invents conversion the session never showed. The session-level banner (recoverable revenue, ALG-25) still covers these sessions through the median GMV per buyer.
2. **Display.** The mockup shows buyers to 1 dp and ¥ in K. Score returns 2 dp, and FE formats per locale (R41). Confirm.
