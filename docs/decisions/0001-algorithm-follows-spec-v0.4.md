# 0001: The scoring algorithm follows spec v0.4 rules (no empirical-Bayes smoothing)

- **Status:** ACCEPTED
- **Decided by:** Rey, 2026-11-09
- **Proposed by:** Rey (recorded by Claude Code from Rey's bootstrap instructions, 2026-11-09)
- **Requirement IDs:** R9, R10, R13, R17, R18
- **Supersedes / overrides:** spec 5.3 rule 5 and Q6 (empirical-Bayes smoothing listed as an option); spec 5.3 rule 2's "confirm in Q5" (settled: CVR quartile)

## Context

The spec still leaves smoothing (Q6, `upstream/design-pack/03-product-spec-v0.4.md:1040`) and the session-tier rule (Q5, `upstream/design-pack/03-product-spec-v0.4.md:291`) open. The BE needs one fixed algorithm to build and test against.

## Decision

1. **Session tier** = quartile of the session's **CVR** (paid buyers ÷ entered) within its benchmark group (spec 5.3 rule 2, `upstream/design-pack/03-product-spec-v0.4.md:291`). The five-stage harmonic composite is not used.
2. **Stage tier** = the session's **raw** stage rate against the group's P25 / P50 / P75 for that stage (spec 5.3 rule 1, `upstream/design-pack/03-product-spec-v0.4.md:290`).
3. **No empirical-Bayes smoothing**, anywhere. This overrides the spec, which still lists it as an option (`upstream/design-pack/03-product-spec-v0.4.md:294`, `upstream/design-pack/03-product-spec-v0.4.md:1040`).
4. **Recoverable revenue** per spec 5.1 (`upstream/design-pack/03-product-spec-v0.4.md:261`): Σ per session of Entered × max(0, P75 CVR − CVR) × GMV per buyer, **including zero-buyer sessions**, whose GMV per buyer is the **group's median GMV per buyer**.
5. **No traffic-quality flag.**
6. **Weakest stage** = the stage with the lowest tier; ties go to the stage with more UV lost (spec 5.1, `upstream/design-pack/03-product-spec-v0.4.md:263`).

## Consequences

- Score computes raw rates only; the Benchmark drawer shows no smoothed rate.
- Health tier (rules 1–2) and recoverable revenue (rule 4) are separate outputs (AGENTS.md rule 8).
- Golden tests encode these rules ([tests/golden/README.md](../../tests/golden/README.md)); details such as rounding and percentile method are in [0004](0004-hifi-wins-and-resolved-rules.md).
- Not yet specified here (goes into [algorithm-spec.md](../algorithm-spec.md)): the exact "median GMV per buyer" population (which sessions, window) — follows the group and window of the session being scored (UNVERIFIED reading of `upstream/design-pack/03-product-spec-v0.4.md:261`).

## Evidence

- Rey's instruction, bootstrap prompt, 2026-11-09.
- Spec lines cited above.

## Open questions

- None raised by Rey. Interpretation points found while writing the algorithm spec go to [decision-queue.md](../decision-queue.md).
