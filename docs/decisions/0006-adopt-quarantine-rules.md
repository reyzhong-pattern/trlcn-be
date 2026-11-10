# 0006: Adopt quarantine rules Q-1 to Q-8

- **Status:** PROPOSED
- **Decided by:** 
- **Proposed by:** Rey's call in chat, 2026-11-10 (DQ-2: "adopt quarantine rules Q-1 to Q-8"); written up by Claude Code, 2026-11-10. Rey sets ACCEPTED.
- **Requirement IDs:** LAND-1, BE-02, R35
- **Supersedes / overrides:** none

## Context

LAND-1 cannot be accepted without quarantine rules (DQ-2). The rules are in [data-model/quarantine-rules.md](../data-model/quarantine-rules.md).

## Decision

1. Rules **Q-1 to Q-8** in [quarantine-rules.md](../data-model/quarantine-rules.md) are adopted as written.
2. A row breaking any rule is landed as `quarantined` with every broken rule ID as its reason, and is excluded from all aggregates, benchmarks, tiers and recoverable revenue. It is never deleted or silently corrected.
3. **Zero paid buyers is not a Q-8 breach** (the refund fraction is undefined, and stage ⑤ is not graded below 3 paid buyers, `upstream/design-pack/03-product-spec-v0.4.md:274`). This is the recommendation in quarantine-rules.md; Rey's reply did not name it, so **Rey confirms or strikes this item in review**.

## Consequences

- Land: BE-02 implements Q-1…Q-8 and stores reasons.
- Tests: one synthetic row per rule, plus a zero-buyer row that stays `ok`.

## Evidence

- [data-model/quarantine-rules.md](../data-model/quarantine-rules.md).
- Rey's reply in chat, 2026-11-10, copied by Claude Code: "DQ-2: adopt quarantine rules Q-1 to Q-8."

## Open questions

- Null / blank / non-numeric cells: still TBD (quarantine-rules.md notes). Decide when the real room-export header is checked (DQ-27, DQ-28).
