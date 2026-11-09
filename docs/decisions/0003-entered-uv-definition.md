# 0003: entered_uv := room-export column 观看人数

- **Status:** ACCEPTED
- **Decided by:** Rey, 2026-11-09
- **Proposed by:** Rey (recorded by Claude Code from Rey's bootstrap instructions, 2026-11-09)
- **Requirement IDs:** LAND-1, R7, R8, R10
- **Supersedes / overrides:** none

## Context

Stage ① (Entry rate = Entered ÷ Exposed) and CVR (Paid buyers ÷ Entered) need one definition of "entered" (`upstream/design-pack/03-product-spec-v0.4.md:231`, `upstream/design-pack/03-product-spec-v0.4.md:253`).

## Decision

- `entered_uv` := the room-export column **观看人数**.
- Compass definition, **copied by Rey from Compass help on 2026-11-09**: "直播间观看人数指进入直播间观看的去重人数".
  - De-duplicated users who entered the room; repeat entries count once.
  - Not additive across traffic channels.
  - Attributed by entry time.
- UI label: **进房人数** (matches `upstream/design-pack/05-terminology-zh-en.md:23`).

## Consequences

- Land maps 观看人数 → `entered_uv` ([data-model/room-export.md](../data-model/room-export.md)).
- Because it is de-duplicated, entered UV is never summed across traffic channels; session-level values are summed across sessions only as the spec's pooled formulas do (Σ Entered).

## Evidence

- Definition text: copied by Rey from Compass help, 2026-11-09 (not independently checked by an agent).
- Column presence in an actual room-export file: UNVERIFIED (no file read in bootstrap).

## Open questions

- None.
