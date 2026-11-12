# 0011: Two time bases: T-1 data and the 90-day benchmark

- **Status:** PROPOSED (decided by Rey in writing; Rey sets ACCEPTED, AGENTS.md rule 2)
- **Decided by:** Rey, 2026-11-12 (DQ-24; DQ-33 in part)
- **Proposed by:** Claude Code (step-05 algorithm spec, DQ-24 and DQ-33), decided by Rey
- **Requirement IDs:** R4, R14, BE-04, BE-13, BE-16
- **Supersedes / overrides:** the step-05 recommendation for DQ-33 ("the latest complete export day from the file log")

## Context

- The spec says presets are relative to a time range (`upstream/design-pack/03-product-spec-v0.4.md:195`) but not what they end on (DQ-24), and not how the data-as-of date is set (DQ-33).

## Decision

1. **Data is T-1.** `as_of` is **yesterday** (the UTC+8 calendar day before today).
2. **Every time range ends on `as_of`.** "Last 7 days" = the 7 days ending yesterday. A custom end after `as_of` is clamped to `as_of`.
3. **Benchmark = [as_of − 89, as_of].** All tiers (STAR / GOOD / MID / WEAK) and the Action Card P50 / P75 come from it. **Nothing else does.** In particular the Reach × AOV tag thresholds come from the range, not the benchmark (decision 0010).

## Consequences

- C4, ALG-12, ALG-13 and ALG-38 state the rule. BE-04 and BE-13 cite it.
- Sessions dated today are not used by Score until `as_of` moves.

## Evidence

- Rey's "locked rules" of 2026-11-12, copied by Claude Code on 2026-11-12.

## Open questions

- DQ-33 (rest): what Serve returns when yesterday's files have not landed by the time a user opens the app.
