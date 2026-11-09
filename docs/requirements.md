# Requirements

## Source list

**Spec section 15 is the requirement list:** R1–R45 in `upstream/design-pack/03-product-spec-v0.4.md:972-1021`. They are not copied here; cite them by ID and line.

- There is no **R23** in the spec (the table goes R22 → R24, `03-product-spec-v0.4.md:999-1000`). Do not invent one.
- Where an ACCEPTED decision changes a requirement, the decision wins (e.g. R10 is settled by [decision 0001](decisions/0001-algorithm-follows-spec-v0.4.md); R9's "recalculated live" interacts with an open queue item).
- BE-relevant subset (for orientation, not a re-scoping): R4, R8, R9, R10, R11, R13, R17, R18, R25, R29, R30, R31, R32, R35, R36, R37. Everything is in scope as the spec says; FE-only items (e.g. R1, R33, R45) need no BE work beyond the contract.

## Added by this repo

Only these three are added.

### LAND-1 — Room-export landing

- **What:** land Compass **room-export** files (one row per live session) handed over by Fetch into session records ([decision 0002](decisions/0002-v1-landing-room-export-only.md), PROPOSED).
- **Includes:**
  - column mapping per [data-model/room-export.md](data-model/room-export.md) (entered_uv per [decision 0003](decisions/0003-entered-uv-definition.md));
  - **quarantine**: rows failing [data-model/quarantine-rules.md](data-model/quarantine-rules.md) are kept with their reason and excluded from all aggregates (spec `03-product-spec-v0.4.md:939`);
  - **ratio cross-checks**: recompute and compare with Compass's own ratio columns (曝光-观看率(人数), 观看成交率(人数), 商品点击成交率(人数)); tolerance and action on mismatch TBD;
  - lineage from each session record to its source file and row; idempotent re-landing.
- **Excludes:** Fetch; the product export; any platform-UI automation.
- **Priority:** P0 (UNVERIFIED — not stated by the spec; set by Rey).

### AC-1 — Action Cards via MCP + RAG

- **What:** Action Cards (spec R22, `03-product-spec-v0.4.md:999`; card layout `03-product-spec-v0.4.md:519-523`) are built with MCP + RAG over a reference set of **plays**.
- **Rules:**
  - the reference set of plays **is not designed yet**;
  - **numbers come only from the pipeline** (Score). The LLM never computes or changes a number (AGENTS.md rule 9);
  - card text **cites play IDs**;
  - "Expected recovery at P50/P75" formula: open ([decision-queue.md](decision-queue.md)).
- **Priority:** TBD (Rey).

### AUTH-1 — Allowlist, then Okta; brand access in the database

- **What:** spec 9.1 / 9.2 (`03-product-spec-v0.4.md:742-780`).
  - Phase 1: admin-managed allowlist.
  - Phase 2: Okta OIDC sign-in + SCIM user sync.
  - Users and user–brand access stored in Supabase.
  - **Brand access enforced in the database** (every read path, including API and shared links — R30), not only in application code.
- **Open:** Okta details ([decision-queue.md](decision-queue.md)); Okta groups → brands mapping (spec Q10).
- **Priority:** phase 1 P0 with R29/R30; phase 2 P1 with R32.
