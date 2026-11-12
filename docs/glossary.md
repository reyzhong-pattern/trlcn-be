# Glossary

Terms used across this repo. UI labels (zh/en) are fixed by the spec's terminology (`upstream/design-pack/05-terminology-zh-en.md`, `upstream/design-pack/03-product-spec-v0.4.md:1095` onward).

| Term | Meaning |
|---|---|
| **Room export** | The Compass export with **one row per live session** (live room). The v1 landing input (decision [0002](decisions/0002-v1-landing-room-export-only.md), PROPOSED). Fields: [data-model/room-export.md](data-model/room-export.md). Never called "R1". |
| **Product export** | The Compass export with one row per **live room × product**. Later than v1; not modelled yet. |
| **Requirement ID** | `R1`–`R45` are requirement IDs from spec section 15 (`upstream/design-pack/03-product-spec-v0.4.md:972-1021`), e.g. R1 = Shell, R10 = session tier. R23 does not exist in the spec. Repo-added IDs: `LAND-1`, `AC-1`, `AUTH-1` ([requirements.md](requirements.md)). "R1" never refers to a data file. |
| **Session record** | One landed, validated row per live session in this repo's store, derived from one room-export row: session metadata (session ID, host, type, platform, start/end, topic) and the funnel counts, orders and GMV. Status: valid, quarantined, or live. Only valid, completed sessions enter benchmarks. |
| **Quarantine** | A session record that fails a landing rule ([data-model/quarantine-rules.md](data-model/quarantine-rules.md)). Kept with its reason, excluded from every aggregate and benchmark, shown as "Excluded" (spec `03-product-spec-v0.4.md:939`). |
| **Benchmark group** | The population a value is graded against: **Brand × Platform × Type**, where Type is Self-operated, Influencer, or **All types** (pooled, both types) (spec 5.2, `03-product-spec-v0.4.md:269`; decision [0004](decisions/0004-hifi-wins-and-resolved-rules.md)). Rolling window, minimum 20 sessions, else "Building". |
| **Type** | Host type. Room-export value 自营 → **Self-operated**; 合作 → **Influencer** (decision 0004). UI label for Influencer is 达人 (`05-terminology-zh-en.md:17`). |
| **Tier** | Quartile grade against a benchmark group: **STAR** ≥ P75, **GOOD** ≥ P50, **MID** ≥ P25, **WEAK** < P25; or "Not enough data" / "Building" below minimums (spec 5.3; decision 0004). *Stage tier* grades one stage rate; *session tier* grades the session's CVR (decision [0001](decisions/0001-algorithm-follows-spec-v0.4.md)). A tier is never combined with recoverable revenue. |
| **Recoverable revenue** | ¥ upside per spec 5.1 (`03-product-spec-v0.4.md:261`): Σ Entered × max(0, P75 CVR − CVR) × GMV per buyer. A separate answer from the tier. |
| **Data-as-of date** | `as_of`: **yesterday** (data is T-1, decision 0011). Every time range and the rolling benchmark window **end on** this date; the window is recalculated daily (decisions 0004, 0011). Shown in the scope line as "Data as of … · Benchmark as of …" (spec `03-product-spec-v0.4.md:942`). |
| **Stage numbers ①–⑤** | The five funnel step rates, in order (spec 4.3, `03-product-spec-v0.4.md:229-235`): ① Entry rate = Entered ÷ Exposed; ② Product exposure rate = Product-exposed ÷ Entered; ③ Product click rate = Product-click ÷ Product-exposed; ④ Click-to-pay rate = Paid buyers ÷ Product-click; ⑤ Retention rate = Kept buyers ÷ Paid buyers. |
| **CVR** | Paid buyers ÷ Entered UV. Pooled (Σ ÷ Σ) for aggregates. |
| **Entered UV (进房人数)** | Room-export column 观看人数 (decision [0003](decisions/0003-entered-uv-definition.md)). |
| **Host** | Any account that runs lives (self-operated room or influencer). "Account" and "KOL" appear only in data docs (spec `03-product-spec-v0.4.md:237`). |
| **Fetch** | Getting files from Compass. Out of scope; not in this repo. Hands over raw files plus a file log ([scope.md](scope.md)). |
| **Land / Score / Serve / Access** | This repo's four layers ([scope.md](scope.md)). |
| **Play** | A reference action in the Action Card reference set (AC-1). Each has a play ID that Action Card text cites. The set is not designed yet. |
