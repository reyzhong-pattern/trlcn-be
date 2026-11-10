# BE requirements

- **Status: DRAFT for Rey's approval** (step 05). Agents propose; only Rey accepts (AGENTS.md rule 2).
- **Scope:** backend only, the four layers in [scope.md](scope.md): Land → Score → Serve → Access. FE/UI requirements are not restated; they stay in spec section 15 (`spec:972-1021`). Fetch is out of scope (AGENTS.md rule 7, [scope.md](scope.md)). The brief's "D-10" has no decision record.
- **Shorthand:** `spec:N` = `upstream/design-pack/03-product-spec-v0.4.md` line N. `ALG-n` = a rule in [algorithm-spec.md](algorithm-spec.md). `DQ-n` = an item in [decision-queue.md](decision-queue.md).
- **Priority** comes from the spec R-IDs traced: the highest one wins; P0 = first release (`spec:974`). Where no R-ID applies, the priority is **TBD (Rey)**.
- **Verification:**
  - **Golden**: golden test against the step-06 reference implementation on synthetic inputs ([tests/golden/README.md](../tests/golden/README.md)).
  - **Contract**: contract test against `contract/openapi.yaml`.
  - **DB**: database test, e.g. row-level security.
  - **Land**: landing test with synthetic room-export fixtures.
  - **UAT**: Rey or an operator checks it in the product.
- **Earlier IDs:** LAND-1 = BE-01…BE-04. AC-1 = BE-10 + BE-21. AUTH-1 = BE-28 + BE-29 + BE-30.

## Land

| ID | Requirement | Priority | Trace | ALG | Verify |
|---|---|---|---|---|---|
| BE-01 | Land each room-export file named in the file log into **session records** (ALG-01 fields), with lineage to file and row. Re-landing the same file is a no-op. A newer export of the same session replaces the current version and the history is kept (DQ-29). | P0 (feeds every P0 view) | R8, `spec:951`, `spec:957`; decision 0002 (Rey accepted 2026-11-10; status set in review); 0003 | ALG-01 | Land |
| BE-02 | Set `status` ∈ {ok, live, quarantined} and the quarantine reasons. Apply the quarantine rules Q-1…Q-8 ([quarantine-rules.md](data-model/quarantine-rules.md), decision 0006). Live detection per DQ-28. | P0 | R35, R20, `spec:938-939`, `spec:249` | ALG-02 | Land |
| BE-03 | Cross-check counts against Compass's ratio columns (曝光-观看率(人数), 观看成交率(人数), 商品点击成交率(人数)) and record mismatches as findings. Tolerance is TBD; findings do not quarantine unless Rey decides otherwise. | TBD (Rey) | [room-export.md](data-model/room-export.md) | ALG-03, ALG-04, ALG-05 | Land |
| BE-04 | Record the **data-as-of date** and the last sync time per brand × platform (DQ-33). Serve exposes them (BE-16). | P0 | R4, R35 ("freshness"), `spec:942` | C4, ALG-12 | Land, Contract |

## Score

| ID | Requirement | Priority | Trace | ALG | Verify |
|---|---|---|---|---|---|
| BE-05 | Compute session-level rates and pooled aggregates exactly, with the rounding rule. | P0 | R7, R12, R13, R17, `spec:229-235`, `spec:247-263` | ALG-03…ALG-10 | Golden |
| BE-06 | A daily job builds a **benchmark snapshot** for every (as_of, brand, platform, type_key ∈ {Self-operated, Influencer, All types}). Each holds window dates, n included / excluded / hosts, group status (ready / Building), and per metric: status, P25 / P50 / P75 and the population values (for the drawer histogram). Snapshots are kept and never overwritten. | P0 | R8, R9, R11, `spec:269-275`, `spec:953` | ALG-11…ALG-18 | Golden |
| BE-07 | Grade at read time against the current snapshot: stage tier, session tier, aggregate tier, with Building / Not enough data and never WEAK for small samples. | P0 | R9, R10, R12, R17, R24, `spec:280-294` | ALG-19…ALG-23 | Golden |
| BE-08 | Weakest stage for sessions and for aggregates. | P0 (R17); the Sessions filter is P1 (R18, R20) | R17, R18, R20, `spec:263` | ALG-24 | Golden |
| BE-09 | Recoverable revenue per session and per selection, against the group the filters define. The annualised value is a run-rate (× 365 ÷ days in range), null below 28 days (decision 0007). | P0 | R13, R16, `spec:261` | ALG-25…ALG-27 | Golden |
| BE-10 | **Action Card numbers** per session and stage: rate, P50, P75, gap to P50 in pp, UV lost (est. refunds at ⑤), tier, severity label, and expected recovery at P50 and P75. The formula is open (DQ-4). Numbers come only from Score (AGENTS.md rule 9). | P0 | R22, `spec:519-523`; AC-1 | ALG-09, ALG-20, ALG-25; DQ-4 | Golden |
| BE-11 | Host pooled metrics, leaderboard membership, rank and greying. | P0 | R24, R27, R28, `spec:566-579` | ALG-29, ALG-30 | Golden |
| BE-12 | Daily Reach × AOV tags for influencers: eligibility, borderline, 2-recalculation hysteresis, change marker, CVR tier, and an append-only **tag history**. | P0 (R25); map P1 (R26) | R25, R26, R27, `spec:661-729` | ALG-31…ALG-37 | Golden |
| BE-13 | Time ranges, time gates, previous period, MoM, YoY and change values. | P0 | R14, R12, R13, `spec:369-374`, `spec:195-196` | ALG-38, ALG-39 | Golden |
| BE-14 | Provisional retention: mark stage ⑤ provisional until refunds mature, and exclude immature sessions from the ⑤ benchmark. Blocked on DQ-3 and DQ-27; the window per platform is unknown (G3). | P1 | R36, `spec:1182` | ALG-04 (⑤), ALG-15 | Golden (after DQ-3) |
| BE-15 | A past grade can be reproduced from stored session versions and the snapshot for its `as_of` (stored-or-computed option C, decision 0005). | P0 | R11, `spec:275` | ALG-13; "Stored or computed" | Golden |

## Serve

Every endpoint takes the filter set (Brand, Platform, Type, Hosts, Time range) that applies to it (`spec:208-216`), and returns the group it graded against. The UI API is defined only in `contract/openapi.yaml` (still a placeholder: [contract/README.md](../contract/README.md)).

| ID | Requirement | Priority | Trace | ALG | Verify |
|---|---|---|---|---|---|
| BE-16 | **Scope line**: the group or groups with n, window and status ("Benchmark building (n=k of 20)"). Type = All returns All types plus both type groups. Freshness: data-as-of time and benchmark-as-of date. | P0 | R4, `spec:199-204`, `spec:942` | ALG-11, ALG-12, ALG-17 | Contract |
| BE-17 | **Filter options**: the user's brands (BE-29), platforms with connection status (no fallback to another platform), and hosts for the platform and type with sessions in range. | P0 | R2, R3, R5, `spec:191-197`, `spec:930` | ALG-29 | Contract, DB |
| BE-18 | **Overview**: KPI cards with change vs previous and P50 footnotes; tier distribution; sales cards; recoverable revenue; funnel current vs previous; GMV by last 7 gates with MoM / YoY; channel comparison when Type = All and both types have sessions; sessions section (Latest / Top GMV / Most upside). | P0 (R12–R14); P1 (R15, R16) | R12–R16, `spec:376-433` | ALG-10, ALG-19, ALG-22, ALG-25, ALG-26, ALG-38, ALG-39 | Contract, Golden |
| BE-19 | **Live Funnel**: funnel volume (UV passed, % of exposed, UV lost); summary strip with P50s; stage performance rows (rate, P25 / P50 / P75, gap to P50, tier, UV lost, weakest); per-type sub-rows when Type = All. | P0; weakest-stage links P1 (R18) | R17, R18, `spec:435-459` | ALG-04, ALG-09, ALG-10, ALG-22, ALG-24, ALG-28 | Contract, Golden |
| BE-20 | **Sessions list**: server-side search (date strings, host name, topic), sort on every sortable column, pagination (10 / 25 / 50 / 100), quick filters (tier, weakest stage). Live sessions are on top with no tier; quarantined sessions are labelled with their reason. | P0; quick filters P1 | R19, R20, `spec:461-497` | ALG-02, ALG-20, ALG-21, ALG-24, ALG-25 | Contract |
| BE-21 | **Session drawer**: meta, scope row, KPI strip, prev / next, deep link by `session_id`; Summary (funnel and stage performance); Action Cards with BE-10 numbers and text that **cites play IDs**. LLM-written text may explain the numbers but never computes them (AC-1). The play reference set is not designed yet. | P0 | R21, R22, `spec:499-531`; AC-1 | ALG-20…ALG-25 | Contract, UAT |
| BE-22 | **Benchmark drawer data** for any group and metric: value, tier and percentile rank when opened from a value; the population values for the histogram; group, window, n included / excluded / hosts; stage minimum; all metrics' P25 / P50 / P75; Building state. | P0 | R11, `spec:296-361` | ALG-14…ALG-18 | Contract, Golden |
| BE-23 | **Hosts**: leaderboard (ALG-29 columns, tiered funnel cells, rank, greying, "No lives in this range"), influencer map points (P1), host drawer (KPIs vs P50, tag with reason values, funnel, GMV / CVR per gate, sessions), host comparison for 2–4 `host_id`s on one platform. | P0; map P1 | R24–R28, `spec:533-659` | ALG-29…ALG-36, ALG-38 | Contract, Golden |
| BE-24 | **Comparison facts**: return the numbers behind the "largest difference" sentences for channel and host comparison. The rule is ALG-41 (decision 0009, PROPOSED); the text is rendered from per-language templates (R39), not by an LLM. | P1 (R15) / P0 (R28) | R15, R28, R39, `spec:430`, `spec:653` | ALG-10, ALG-29, ALG-41 | Contract, Golden |
| BE-25 | **States** (§12): every response distinguishes no brand access, no access to this brand, platform not connected, no sessions in scope, Building, Not enough data, live, quarantined, and error, so FE never infers a state from missing fields. | P0 | R35, `spec:924-945` | ALG-02, ALG-17, ALG-23 | Contract |
| BE-26 | **Settings**: users and access (list, invite, edit, deactivate, bulk brand assignment, guardrails: no self-demotion or self-deactivation, at least one active Admin); data connections and benchmark rules (read-only). | P0 (R29); P1 (R31) | R29, R31, `spec:731-771` | — | Contract, DB |
| BE-27 | **Export**: CSV of the Sessions and Hosts tables with the same filters and values as the screen; currency CNY. | P1 | R37, R38, `spec:1013` | — | Contract |

## Access

| ID | Requirement | Priority | Trace | ALG | Verify |
|---|---|---|---|---|---|
| BE-28 | Phase 1 sign-in: an admin-managed **allowlist**. Users and user–brand access are stored in Supabase (AUTH-1). | P0 | R29, R30, `spec:57`, `spec:775` | — | DB, UAT |
| BE-29 | **Brand scoping everywhere, enforced in the database** (e.g. row-level security on every table that holds brand data), for every read path: API, deep links, shared links, export. An unassigned brand returns "no access" and no data. Operators see their brands; Admins see all brands (`spec:51-52`). | P0 | R2, R30, `spec:49-57`, `spec:929` | — | DB, Contract |
| BE-30 | Phase 2: Okta OIDC sign-in and SCIM sync. Source "Okta", status from Okta, deactivation propagates. Brand access stays in the app (DQ-6, spec Q10). | P1 | R32, `spec:773-780` | — | UAT |
| BE-31 | **Audit log** of role and brand-access changes (who, what, when). | P1 | R31, `spec:740` | — | DB |

## Coverage: spec requirements R1–R45

Every R-ID in spec section 15 (`spec:976-1021`). There is no **R23** in the spec (`spec:999-1000`).
- **BE**: the backend owns it.
- **FE-only**: no BE work beyond what the contract already serves.
- **both**: FE renders what BE computes or enforces.

| R | Area | Owner | BE requirements |
|---|---|---|---|
| R1 | Shell | FE-only | — |
| R2 | Brand switcher lists only the user's brands | both | BE-17, BE-29 |
| R3 | Filters | both | BE-17 |
| R4 | Scope line, freshness | both | BE-04, BE-16 |
| R5 | Disabled controls; unconnected platforms | both | BE-17, BE-25 |
| R6 | Filter and drawer state in the URL | FE-only | (BE-20, BE-21 and BE-23 accept IDs for deep links) |
| R7 | One funnel vocabulary, glossary | both | BE-05 (field names per [glossary.md](glossary.md)) |
| R8 | Rolling benchmarks, Building | BE | BE-01, BE-06 |
| R9 | Quartile tiers, live, no small-sample tiers | BE | BE-06, BE-07 |
| R10 | Session tier = CVR quartile | BE | BE-07 |
| R11 | Benchmark drawer | both | BE-06, BE-15, BE-22 |
| R12 | Overview live performance cards | both | BE-05, BE-07, BE-13, BE-18 |
| R13 | Overview sales cards, recoverable | both | BE-05, BE-09, BE-13, BE-18 |
| R14 | Overview trends | both | BE-13, BE-18 |
| R15 | Channel comparison | both | BE-18, BE-24 |
| R16 | Overview sessions section | both | BE-09, BE-18 |
| R17 | Live Funnel | both | BE-05, BE-07, BE-08, BE-19 |
| R18 | Weakest-stage rule and links | both | BE-08, BE-19 |
| R19 | Sessions table | both | BE-20 |
| R20 | Quick filters, live / excluded labels | both | BE-02, BE-08, BE-20 |
| R21 | Session drawer | both | BE-21 |
| R22 | Action Cards | both | BE-10, BE-21 |
| R23 | *(not in the spec)* | — | — |
| R24 | Host leaderboard | both | BE-07, BE-11, BE-23 (DQ-8: R24 vs §7.2) |
| R25 | Reach × AOV tags | both | BE-12, BE-23 |
| R26 | Influencer map | both | BE-12, BE-23 |
| R27 | Host drawer | both | BE-11, BE-12, BE-23 |
| R28 | Host comparison | both | BE-11, BE-23, BE-24 |
| R29 | Settings: users and access | both | BE-26, BE-28 |
| R30 | Brand-level access everywhere | both | BE-29 |
| R31 | Data connections, benchmark rules, audit log | both | BE-26, BE-31 |
| R32 | Okta SSO + SCIM | both | BE-30 |
| R33 | Design system | FE-only | — |
| R34 | Responsive | FE-only | — |
| R35 | States | both | BE-02, BE-04, BE-25 |
| R36 | Provisional retention | both | BE-14 |
| R37 | CSV export, copy summary | both | BE-27 (Copy summary is FE-only) |
| R38 | CNY; USD toggle (P2) | both | BE-27 (CNY values everywhere; USD is P2, no BE work yet) |
| R39 | zh-CN / en for every string and generated sentence | both | BE-21, BE-24 (structured facts plus template keys; Action Card text per language) |
| R40 | Fixed bilingual terminology | both | BE-21 (Action Card text uses Appendix B terms) |
| R41 | Locale formatting | FE-only | — (BE returns unformatted numbers) |
| R42 | "Host" as the only UI term | FE-only | — |
| R43 | One Comparison panel component | FE-only | — (data is in BE-18, BE-23, BE-24) |
| R44 | Tooltips | FE-only | — (values are in BE-19, BE-22, BE-23) |
| R45 | Drawers, motion | FE-only | — |
