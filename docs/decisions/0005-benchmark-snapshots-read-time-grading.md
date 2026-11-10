# 0005: Store daily benchmark snapshots; grade at read time (option C)

- **Status:** PROPOSED
- **Decided by:** 
- **Proposed by:** Rey's call in chat, 2026-11-10 (DQ-1: "C, hybrid"); written up by Claude Code, 2026-11-10. Rey sets ACCEPTED.
- **Requirement IDs:** R9, R11, BE-15
- **Supersedes / overrides:** reads spec "recalculated live" (`upstream/design-pack/03-product-spec-v0.4.md:294`) as read-time grading against the current daily snapshot

## Context

The spec says benchmarks follow the filters and are recalculated live (`upstream/design-pack/03-product-spec-v0.4.md:270`, `:294`), and also that a daily job computes P25/P50/P75 per group and stores them with window dates (`:953`). Decision 0004 item 1 recalculates the window daily. The options are laid out in [algorithm-spec.md › Stored or computed](../algorithm-spec.md#stored-or-computed).

## Decision

Option C, hybrid:

1. A **daily job** writes one **benchmark snapshot** per (`as_of`, brand × platform × type group): window dates, n included / excluded / hosts, P25/P50/P75 per metric, metric status, median GMV per buyer.
2. The daily job also writes **tag history** (ALG-37), which hysteresis needs.
3. Snapshots and tag history are **append-only**: never overwritten or deleted.
4. **Tiers, weakest stage and recoverable revenue are computed at read time** from session values plus the snapshot for the filtered group and `as_of`.
5. A past grade = f(session version at that time, snapshot for that `as_of`) and must reproduce exactly (BE-15).

## Consequences

- Score: snapshot and tag-history tables; grading is a pure function shared by the step-06 reference implementation and the BE.
- Serve: every graded response names the snapshot (`as_of`, group) it used.
- Land: session versions are kept (DQ-29), so step 5 holds when an export is re-landed.
- Tests: golden tests call the pure grading function with a fixed snapshot.

## Evidence

- `docs/algorithm-spec.md` › Stored or computed (options A, B, C and the recommendation).
- Rey's reply in chat, 2026-11-10, copied by Claude Code: "DQ-1:C, hybrid."

## Open questions

- None new.
