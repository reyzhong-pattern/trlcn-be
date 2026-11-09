# 0002: v1 landing uses the Compass room export only

- **Status:** PROPOSED
- **Decided by:** —
- **Proposed by:** Rey's bootstrap instructions, written up by Claude Code, 2026-11-09
- **Requirement IDs:** LAND-1, R8–R13, R17, R24–R25
- **Supersedes / overrides:** none

## Context

Compass offers a **room export** (one row per live session) and a **product export** (live room × product). The spec's v1 needs session-level funnel, order and GMV data (`upstream/design-pack/03-product-spec-v0.4.md:951`, `upstream/design-pack/03-product-spec-v0.4.md:957`); SKU-level sales are listed as not available yet (`upstream/design-pack/03-product-spec-v0.4.md:958`).

## Decision (proposed)

v1 lands **only the room export**. The product export is later.

## Consequences

- LAND-1 covers the room export only; [data-model/room-export.md](../data-model/room-export.md) is the only landing model.
- Any feature needing product-level data waits.
- Kept buyers / refunds for stage ⑤ must be derived from room-export columns (open; see [data-model/room-export.md](../data-model/room-export.md)).

## Evidence

- Rey's bootstrap instructions, 2026-11-09. Room-export columns: UNVERIFIED (no file read).

## Open questions

- Rey to accept or reject.
