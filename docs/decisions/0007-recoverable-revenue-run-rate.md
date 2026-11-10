# 0007: Recoverable revenue inputs, and annualised value as a run-rate

- **Status:** PROPOSED
- **Decided by:** 
- **Proposed by:** Rey's call in chat, 2026-11-10 (DQ-16, DQ-17: option B, run-rate with guards); written up by Claude Code, 2026-11-10. Rey sets ACCEPTED.
- **Requirement IDs:** R13, R16, BE-09
- **Supersedes / overrides:** spec "annual GMV from the platform MCP" (`upstream/design-pack/03-product-spec-v0.4.md:261`, `:952`) for v1; ALG-27's "null until DQ-17"

## Context

The spec names an annual-GMV input for the hover value but gives no formula, and no such input exists in this repo (ALG-27, DQ-5). Option B needs only data already landed.

## Decision

**Session and aggregate recoverable (DQ-16).** As written in ALG-25 and ALG-26: eligible sessions are `ok` with `entered_uv > 0`; `cvr` is the 4-dp CVR; P75 CVR and the zero-buyer median GMV per buyer come from the grading group's current window, own session included; the median needs ≥ 20 sessions; null when the group is Building. Rey's reply named DQ-16 together with DQ-17; this decision records the ALG-25/26 recommendation for DQ-16, and **Rey confirms in review**.

**Annualised recoverable (DQ-17), option B, run-rate.**

```
days_in_range = (range_end − range_start) + 1      # after clamping range_end to as_of (ALG-38)
annualised    = round2( aggregate_recoverable × 365 ÷ days_in_range )   if days_in_range ≥ 28
              = null, reason "range_too_short"                          if days_in_range < 28
              = null                                                    if aggregate_recoverable is null
```

- **Guard.** Ranges shorter than 28 days show **"Range too short to annualise"** instead of a number. Last 30 days, Last 90 days, Last month and This quarter (once ≥ 28 days in) pass; Last 7 days is blocked; This month is blocked until its 28th day.
- **Label** on every annualised value: **"Run-rate: this period's pace × 365. Not seasonally adjusted."**
- It is a directional ceiling, not a forecast, and stays a separate answer from the tier (AGENTS.md rule 8).

## Consequences

- Score: ALG-27 implements the formula and guard; returns `annualised`, `days_in_range`, and `null_reason`.
- Serve / contract: the hover carries the value or the "Range too short" message, plus the label text from a template (R39), never from an LLM.
- DQ-17 no longer depends on DQ-5.
- Tests: golden cases for 30 days (value), 28 days (value), 27 days (null, range_too_short), and a null aggregate.

## Evidence

- `docs/algorithm-spec.md` ALG-25, ALG-26, ALG-27.
- Rey's reply in chat, 2026-11-10, copied by Claude Code: "DQ-16,17-B, the run-rate: recoverable × 365 ÷ days in the range … ranges shorter than 28 days show 'Range too short to annualise' … The label reads 'Run-rate: this period's pace × 365. Not seasonally adjusted.'"

## Open questions

- Seasonality: run-rate over a peak period (e.g. Double 11) overstates the year. Accepted as labelled; revisit if an approved annual-GMV source arrives (DQ-5).
