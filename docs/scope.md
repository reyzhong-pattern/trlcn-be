# Scope: the four layers

```
[Fetch — out of scope, not in this repo]
   │  raw files + file log
   ▼
 Land ──► Score ──► Serve ──► Access (wraps Serve)
```

Storage: the existing Supabase project in Pattern's account. Which schemas the new build uses is **TBD** (decided during building).

## Fetch (out of scope)

- Gets files from Compass. **Not in this repo**, and no agent automates Compass or any platform UI (AGENTS.md rule 7).
- **Hand-over to Land:** raw files (room export for v1) **plus a file log**. File log fields: TBD (at minimum each file's name, brand, platform, export date range and a checksum would let Land de-duplicate — UNVERIFIED, to agree with the Fetch owner).
- Where the files are dropped (bucket, path): TBD.

## Land

Owns: turning raw room-export files into session records. Requirement LAND-1.

- Read a file named in the file log; reject files already landed (by checksum, TBD).
- Map columns to the room-export model ([data-model/room-export.md](data-model/room-export.md)).
- Apply quarantine rules ([data-model/quarantine-rules.md](data-model/quarantine-rules.md), PROPOSED); keep quarantined rows with their reason.
- Cross-check against Compass's own ratio columns.
- Record lineage: each session record points to its source file and row.
- Does **not** compute benchmarks, tiers or revenue.
- Storage tables / schema: TBD.

## Score

Owns: every number the product shows. Requirements R8–R10, R13 (recoverable), R17–R18, R25 (tags).

- Benchmarks per group and window, stage tiers, session tier, weakest stage, recoverable revenue, host tags — per [algorithm-spec.md](algorithm-spec.md) and decisions 0001 and 0004.
- Health tier and recoverable revenue are separate outputs.
- Stored by a daily job or computed at read time: **open** ([decision-queue.md](decision-queue.md)).
- No LLM computes anything here.

## Serve

Owns: the UI API that FE calls, defined in [contract/openapi.yaml](../contract/README.md) (v1 pending).

- Reads Score outputs (and session records) and shapes them for views: Overview, Live Funnel, Sessions, drawers, Hosts, Settings.
- Action Cards (AC-1): text may be LLM-generated with MCP + RAG over the play set, but every number in a card comes from Score, and text cites play IDs.
- Framework, hosting: TBD.

## Access

Owns: who can sign in and which brands they see. Requirements AUTH-1, R29, R30, R32.

- Phase 1: admin-managed allowlist. Phase 2: Okta OIDC + SCIM (spec 9.2).
- Users and user–brand access stored in Supabase; **brand access enforced in the database** (e.g. row-level security), not only in the API. Exact mechanism: TBD.
- Okta details: open ([decision-queue.md](decision-queue.md)).
