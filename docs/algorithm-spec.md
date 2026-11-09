# Algorithm spec (Score layer)

- **Status:** TEMPLATE — to be filled in the next step by Claude Code, then approved by Rey. Nothing below is a rule yet except where it cites an ACCEPTED decision.
- **Sources (in order):** spec v0.4 (`upstream/design-pack/03-product-spec-v0.4.md`) → decisions [0001](decisions/0001-algorithm-follows-spec-v0.4.md), [0004](decisions/0004-hifi-wins-and-resolved-rules.md) → contract.
- **Every rule** cites a spec line or decision. Anything inferred from the mockup names version 1794210096-60c6. Anything else is UNVERIFIED.
- Health tier and recoverable revenue are separate outputs (AGENTS.md rule 8).

## 1. Inputs

<!-- Session record fields used (from docs/data-model/room-export.md). Valid / quarantined / live status. -->
TBD

## 2. Rates

<!-- Stage ①–⑤ and CVR formulas; zero denominators; rounding to 4 decimals before grading (0004). Kept buyers derivation (open DQ-3). -->
TBD

## 3. Benchmark groups and window

<!-- Brand × Platform × {Self-operated, Influencer, All types (pooled)} (0004). Window ends on data-as-of date, recalculated daily (0004). Window length 90 days, min 20 sessions (spec 5.2). Session in its own population (0004). Stage minimums (spec 5.2). -->
TBD

## 4. Percentiles

<!-- P25/P50/P75 by linear interpolation (0004): exact formula, worked example. -->
TBD

## 5. Tiers

<!-- Stage tier (0001), session tier = CVR quartile with entered ≥ 30 (0001, 0004), thresholds ≥P75 STAR, ≥P50 GOOD, ≥P25 MID (0004). Not enough data / Building. Aggregate tier (spec 5.3 rule 3). No smoothing (0001). -->
TBD

## 6. Weakest stage

<!-- Lowest tier; ties → more UV lost (0001). Behaviour when no stage is graded. -->
TBD

## 7. Recoverable revenue

<!-- Spec 5.1 incl. zero-buyer sessions at the group's median GMV per buyer (0001). Annualised value. -->
TBD

## 8. Action Card expected recovery

<!-- P50 / P75 formula from the mockup's behaviour (DQ-4). -->
TBD

## 9. Host tags

<!-- Spec section 8 (0004): inputs, eligibility, borderline, hysteresis. -->
TBD

## 10. Worked examples (synthetic)

<!-- Small synthetic cases that become tests/golden fixtures. -->
TBD
