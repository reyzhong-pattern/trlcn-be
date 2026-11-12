# 0004: Hi-fi wins over older methods; mockup behaviour fills spec gaps

- **Status:** ACCEPTED
- **Decided by:** Rey, 2026-11-09
- **Proposed by:** Rey (recorded by Claude Code from Rey's bootstrap instructions, 2026-11-09)
- **Requirement IDs:** R8, R9, R10, R11, R25
- **Supersedes / overrides:** any older algorithm or method (including `upstream/design-pack/generate_demo_data.py`); spec 5.2's "No pooled All types group" fallback (`upstream/design-pack/03-product-spec-v0.4.md:276`)

## Context

The spec, the hi-fi mockup (claude.ai artifact Y6meVMkfzS7bB1NL7mszHB, version 1794283411-4173, reference only — [upstream/PIN.md](../../upstream/PIN.md)) and older methods (the staging app, the demo generator) differ in places.

## Decision

**Rule:** where the spec / hi-fi conflicts with any older algorithm or method, **the hi-fi wins**. Where the spec is silent, **the mockup's behaviour wins**.

**Resolved under this rule:**

1. **Window:** the rolling window **ends on the data-as-of date** and is **recalculated daily** (not the window ending the day before each session).
2. **Own population:** a session **is in its own benchmark population** (not excluded from it).
3. **Session tier minimum:** session tier needs **entered ≥ 30**; below that, "Not enough data".
4. **Rounding:** rates are **rounded to 4 decimals before grading**.
5. **Thresholds:** **≥ P75 → STAR, ≥ P50 → GOOD, ≥ P25 → MID**, else WEAK.
6. **Percentiles:** **linear interpolation**.
7. **All types group:** a **pooled All types group** (all valid sessions of both types) per spec 5.2 (`upstream/design-pack/03-product-spec-v0.4.md:269`).
8. **Type mapping:** room-export 自营 → **Self-operated**, 合作 → **Influencer**.
9. **Host tags:** per spec section 8 (`upstream/design-pack/03-product-spec-v0.4.md:661` onward).

## Consequences

- The demo generator differs on items 1, 2, 3 and 7 (it uses the 90 days before each session, excludes the session itself, has no All types group, and grades session tier when entered > 0: `upstream/design-pack/generate_demo_data.py:209`, `:237`). Its outputs are never expected values ([tests/golden/README.md](../../tests/golden/README.md)).
- "Linear interpolation" is the definition behind e.g. numpy's default `percentile` method; the exact formula is written into [algorithm-spec.md](../algorithm-spec.md).
- Claims about the mockup's behaviour must name artifact Y6meVMkfzS7bB1NL7mszHB at version 1794283411-4173 (as in [upstream/PIN.md](../../upstream/PIN.md)) or be marked UNVERIFIED. *(Citation corrected 2026-11-12: the earlier ID KrA5rxAQxzQhpCdtjwfyHU was a different artifact. The decision itself is unchanged.)*

## Evidence

- Rey's instruction, bootstrap prompt, 2026-11-09.
- Spec and generator lines cited above.

## Open questions

- Whether tiers are stored by a daily job or computed at read time ([decision-queue.md](../decision-queue.md)) — item 1 says the window is recalculated daily; spec 5.2 says values follow the filters "recalculated whenever the filters change" (`upstream/design-pack/03-product-spec-v0.4.md:270`).
