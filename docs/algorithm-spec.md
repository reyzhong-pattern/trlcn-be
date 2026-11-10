# Algorithm spec (Score layer)

- **Status: DRAFT for Rey's approval** (step 05). Nothing here is ACCEPTED until Rey says so (AGENTS.md rule 2). Rules that rest on an open item say **PROPOSED (DQ-n)**; Step 06 implements the proposed option unless Rey picks another.
- **Purpose:** precise enough that two people implementing it independently get identical numbers. Step 06 builds a reference implementation and golden tests from this document alone.
- **Sources, in order:** spec v0.4 → accepted decisions → contract (AGENTS.md "Source-of-truth order").
- **Not a source:** `upstream/design-pack/generate_demo_data.py` and every number it produced, including the demo figures quoted in the spec (e.g. ¥2.88M and S00234 ¥558.0K at `spec:261`). They come from a day-before-session window the spec rejects (`spec:294`). See [Where the generator differs](#where-the-generator-differs).
- Health tier and recoverable revenue are separate outputs (AGENTS.md rule 8). No LLM computes anything here (rule 9).

## Citation shorthand

| Shorthand | File |
|---|---|
| `spec:N` | `upstream/design-pack/03-product-spec-v0.4.md` line N |
| `gen:N` | `upstream/design-pack/generate_demo_data.py` line N |
| `0001` … `0004` | `docs/decisions/0001-algorithm-follows-spec-v0.4.md`, `0002-v1-landing-room-export-only.md`, `0003-entered-uv-definition.md`, `0004-hifi-wins-and-resolved-rules.md` |
| `DQ-n` | an item in [decision-queue.md](decision-queue.md) |

Decision IDs: the step-05 brief named "D-01", "D-14" and "D-10". The repo has no such files. D-01 = **0001**, D-14 = **0003**. "Fetch is out of scope" (D-10) is not a decision record; it is `AGENTS.md` rule 7 and [scope.md](scope.md).

## Conventions used by every rule

- **C1. Exact arithmetic.** Ratios are computed exactly (rational or arbitrary-precision decimal), never in binary floating point, and then rounded once (ALG-03). Comparisons (`≥`, `<`, `≤ 0.10`) are made on the rounded decimal values. Reason: float64 gives `330/300 − 1 = 0.10000000000000009`, which would wrongly fail an inclusive `≤ 0.10` test (ALG-33 example).
- **C2. Time zone.** All dates are calendar days in UTC+8 (China Standard Time), the spec's display zone (`spec:1033`).
- **C3. Null.** "null" means "no value". A null is never treated as 0, never enters a percentile, and never produces a tier.
- **C4. The data-as-of date** `as_of` is the latest UTC+8 calendar day for which landed data is complete (glossary). How Land sets it: DQ-33.
- **C5. Scope vs group.** The *scope* is everything the filters select (Brand, Platform, Type, Hosts, Time range; `spec:191-195`). The *benchmark group* is only Brand × Platform × Type (`spec:193`). The Hosts filter and the time range never change the group or its percentiles.

---

## 1. Inputs

### ALG-01 Session record

**Definition.** The algorithm starts from one landed session record per live session (glossary "Session record"). Mapping each platform's native events to the five stages (spec Q8, `spec:1042`) is out of scope: it is already done by the time a record exists.

| Field | Type | Meaning | Source |
|---|---|---|---|
| `session_id` | text | Unique per brand × platform | room export, column UNVERIFIED ([room-export.md](data-model/room-export.md)) |
| `brand`, `platform` | text | Workspace and platform | room export or file log, UNVERIFIED |
| `host_id`, `host_name` | text | The account that ran the live | UNVERIFIED |
| `type` | enum | `Self-operated` \| `Influencer` (自营 / 合作, 0004 item 8) | UNVERIFIED column |
| `start_time`, `end_time` | timestamp with zone | Start and end of the live | UNVERIFIED |
| `live_topic` | text | Session title | UNVERIFIED |
| `exposed_uv` | int ≥ 0 | 曝光人数 | builder-reported, UNVERIFIED |
| `entered_uv` | int ≥ 0 | 观看人数 (0003) | 0003; column presence UNVERIFIED |
| `product_exposed_uv` | int ≥ 0 | 商品曝光人数 | UNVERIFIED |
| `product_clicked_uv` | int ≥ 0 | 商品点击人数 | UNVERIFIED |
| `paid_buyers` | int ≥ 0 | 成交人数 | UNVERIFIED |
| `paid_orders` | int ≥ 0 | 成交订单数 | UNVERIFIED |
| `refunding_users` | int ≥ 0 | 退款人数 (attribution: DQ-3) | UNVERIFIED |
| `gmv` | decimal(2) ≥ 0, CNY | 用户支付金额, before refunds (`spec:255`) | UNVERIFIED |
| `avg_watch_sec` | decimal ≥ 0 | Average watch seconds per entered user | column UNVERIFIED (DQ-32) |
| `status` | enum | `ok` \| `live` \| `quarantined` (ALG-02) | set by Land |
| `quarantine_reasons` | text[] | Rule IDs Q-1…Q-8 ([quarantine-rules.md](data-model/quarantine-rules.md)) | set by Land |

**Derived field.** `kept_buyers = paid_buyers − refunding_users`. **PROPOSED (DQ-27, depends on DQ-3)**: the room export has no kept-buyers column ([room-export.md](data-model/room-export.md)). Stage ⑤ needs one (`spec:235`).

**Session day.** `session_day` = the UTC+8 calendar date of `start_time`. **PROPOSED (DQ-15).** Every day-based rule (window, time range, time gates) uses `session_day`.

**Not enough data.** Not applicable: this rule defines inputs.

**Edge cases.**
- A missing count is null (C3). Every rate that uses it is null.
- A record whose counts break a quarantine rule is still a record, with `status = quarantined`.

**Example.** Session **S-A**, used throughout this document:

| exposed | entered | product_exposed | product_clicked | paid_buyers | paid_orders | refunding_users | gmv | avg_watch_sec |
|---|---|---|---|---|---|---|---|---|
| 2,000 | 300 | 240 | 60 | 12 | 14 | 2 | 4,200.00 | 65 |

`kept_buyers` = 12 − 2 = **10**. If `start_time` = 2026-10-26T21:00+08:00, then `session_day` = 2026-10-26.

## 2. Validity

### ALG-02 Session status and exclusions

**Definition.** Every record has exactly one status.

| Status | Meaning | In benchmarks / percentiles | In tiers, weakest stage, recoverable | In KPIs and aggregates | Listed in Sessions | Counted as "excluded" |
|---|---|---|---|---|---|---|
| `ok` | Completed and passed every quarantine rule ("valid") | yes | yes | yes | yes | no |
| `live` | Not ended or not yet synced | no | no | no | yes, "Live now", no tier (`spec:496`, `spec:938`) | yes |
| `quarantined` | Broke ≥ 1 quarantine rule | no | no | no | yes, "Excluded" + reason (`spec:939`) | yes |

- "Sessions analyzed" counts `ok` sessions in scope only (`spec:249`).
- The Benchmark drawer reports `n included` = `ok` sessions in the group window, and `n excluded` = `live` + `quarantined` sessions in the group window (`spec:332`).
- How Land decides a session is `live`: **open (DQ-28)**.
- Quarantine rules themselves are PROPOSED (DQ-2).

**Not enough data.** Not applicable.

**Edge cases.** A session can go from `live` to `ok` when it is re-landed. Status is the status in the latest landed version (DQ-29).

**Example.** A group window holds 19 `ok`, 1 `live` and 2 `quarantined` sessions. Then n included = **19**, n excluded = **3**, and the group is Building (ALG-17).

## 3. Rates

### ALG-03 Rounding

**Definition.** PROPOSED (DQ-11); 0004 item 4 fixes only "rates rounded to 4 decimals before grading".

| Value | Decimals | Applied when |
|---|---|---|
| Stage rates, CVR, refund rate, percent change | 4 (a fraction, so 0.1234 = 12.34%) | Once, on the exact ratio |
| Percentiles of 4-dp values (P25/P50/P75 of rates and CVR) | 4 | Once, on the exact interpolated value (ALG-14) |
| Currency: AOV, GMV per buyer, avg GMV per session, recoverable revenue, median GMV per buyer, percentiles of AOV | 2 | Once, on the exact value |
| Exposure per session (host), percentiles of exposure | 2 | Once, on the exact value |
| Avg watch time | 2 | Once |
| Percentile rank | 0 | Once |

- **Rounding mode: half away from zero.** All values here are ≥ 0, so this is "half up". It is the behaviour of Postgres `round(numeric, n)` and of Python `Decimal.quantize(..., ROUND_HALF_UP)`. It is **not** Python's built-in `round()` (half to even, on binary floats).
- Every downstream rule takes the rounded value as its input. Nothing is rounded twice.

**Inputs.** An exact ratio.

**Not enough data.** Not applicable.

**Edge cases.** A ratio with denominator 0 is null, not rounded.

**Example.**
- 1 ÷ 800 = 0.00125 exactly → **0.0013**. Half to even would give 0.0012.
- 2 ÷ 3 → **0.6667**. 1 ÷ 6 → **0.1667**.

### ALG-04 Stage rates ①–⑤ (session level)

**Definition.** These are the five step rates, each in % of the stage before (`spec:229-235`).

| Stage | Rate | Numerator | Denominator = "UV into stage" |
|---|---|---|---|
| ① | Entry rate | `entered_uv` | `exposed_uv` |
| ② | Product exposure rate | `product_exposed_uv` | `entered_uv` |
| ③ | Product click rate | `product_clicked_uv` | `product_exposed_uv` |
| ④ | Click-to-pay rate | `paid_buyers` | `product_clicked_uv` |
| ⑤ | Retention rate | `kept_buyers` (ALG-01) | `paid_buyers` |

`rate = round4(numerator ÷ denominator)` (ALG-03).

**Not enough data.** A rate is computed whenever its denominator is > 0. Whether it is *graded* is decided by the stage minimums (ALG-18): ≥ 30 UV into stages ①–④, ≥ 3 paid buyers for ⑤ (`spec:274`).

**Edge cases.**
- Denominator 0 → null.
- A rate above 1 cannot occur in an `ok` record (quarantine Q-2…Q-5, Q-7).
- Any input null → null.

**Example (S-A).** ① 300/2000 = **0.1500**. ② 240/300 = **0.8000**. ③ 60/240 = **0.2500**. ④ 12/60 = **0.2000**. ⑤ 10/12 = 0.83333… → **0.8333**.

### ALG-05 CVR

**Definition.** `cvr = round4(paid_buyers ÷ entered_uv)` (`spec:253`, `spec:291`).

**Not enough data.** For grading (session tier) the session needs `entered_uv ≥ 30` (0004 item 3). The CVR percentile population: ALG-15.

**Edge cases.** `entered_uv = 0` → null. `paid_buyers = 0` with `entered_uv > 0` → 0.0000. That is a real value and is graded.

**Example (S-A).** 12 ÷ 300 = **0.0400**.

### ALG-06 AOV and GMV per buyer

**Definition.**
- `aov = round2(gmv ÷ paid_orders)` (`spec:258`).
- `gmv_per_buyer = round2(gmv ÷ paid_buyers)`. This is used only by recoverable revenue (ALG-25).

**Not enough data.** AOV enters the AOV population only when `paid_orders ≥ 1` (ALG-15).

**Edge cases.** A zero denominator gives null. A null `gmv_per_buyer` is replaced by the group fallback only inside ALG-25.

**Example (S-A).** AOV = 4,200.00 ÷ 14 = **300.00**. GMV per buyer = 4,200.00 ÷ 12 = **350.00**.

### ALG-07 Refund rate

**Definition.** The spec defines refund rate as refunded orders ÷ paid orders (`spec:259`), but the room export has no refunded-orders column (UNVERIFIED, [room-export.md](data-model/room-export.md)).

**PROPOSED for v1 (DQ-27):** `refund_rate = round4(refunding_users ÷ paid_buyers)`. It is labelled as a share of buyers. The spec's order-based definition is kept for when refunded orders exist.

**Not enough data.** Refund rate is display only and not graded (no tier in `spec:259`), so it has no minimum.

**Edge cases.** `paid_buyers = 0` → null.

**Example (S-A).** 2 ÷ 12 = **0.1667**.

### ALG-08 Avg watch time

**Definition.** Pooled: `avg_watch = round2(Σ watch_seconds ÷ Σ entered_uv)`, where `watch_seconds = avg_watch_sec × entered_uv` per session (`spec:260`). It is display only and never graded.

The room-export column is UNVERIFIED, and so is the assumption that it is per entered user (DQ-32).

**Not enough data.** None.

**Edge cases.** Σ entered = 0 → null.

**Example.** S-A: 65 × 300 = 19,500 s. S-B (ALG-10): 40 × 100 = 4,000 s. Pooled: 23,500 ÷ 400 = **58.75 s**.

### ALG-09 UV lost per stage

**Definition.** `uv_lost(stage) = UV into stage − UV out of stage` (`spec:262`). For stage ⑤ that is `paid_buyers − kept_buyers = refunding_users`, which is the "est. refunds" of `spec:522`.

**Not enough data.** None. UV lost is a count and is always shown.

**Edge cases.** UV lost is never negative in an `ok` record. With a null input it is null.

**Example (S-A).** ① 1,700, ② 60, ③ 180, ④ 48, ⑤ 2.

### ALG-10 Pooled aggregates vs session-level values

**Definition.**
- **Session-level values** (one per session) feed percentiles (ALG-15) and session grades (ALG-20, ALG-21).
- **Pooled aggregates** are Σ numerator ÷ Σ denominator over the `ok` sessions in scope, never an average of session rates (`spec:251-253`, `spec:258`).

| Aggregate | Formula |
|---|---|
| Sessions analyzed | count of `ok` sessions in scope |
| Exposed UV | Σ `exposed_uv` |
| Stage rates ①–⑤ | ALG-04 formulas on the sums |
| CVR | Σ `paid_buyers` ÷ Σ `entered_uv` |
| Total GMV | Σ `gmv` |
| Avg GMV / session | round2(Total GMV ÷ Sessions analyzed) (`spec:256`) |
| Paid orders | Σ `paid_orders` |
| Avg AOV | round2(Σ `gmv` ÷ Σ `paid_orders`) |
| Refund rate | ALG-07 on the sums |
| UV lost per stage | ALG-09 on the sums |
| Avg watch time | ALG-08 |

**Not enough data.** Aggregates are always shown. Whether they are tiered: ALG-22.

**Edge cases.** No `ok` sessions in scope → every aggregate is null except Sessions analyzed = 0. This is the "No sessions in scope" state (`spec:931`).

**Example.** S-A plus **S-B** (exposed 1,000, entered 100, product_exposed 50, clicked 20, buyers 2, orders 2, refunding 0, gmv 500.00, avg watch 40):
- Pooled CVR = 14 ÷ 400 = **0.0350**. The mean of the session CVRs, (0.0400 + 0.0200) ÷ 2 = 0.0300, is **not** used.
- Pooled stages: ① 3,000→400 **0.1333**; ② **0.7250**; ③ 80/290 = **0.2759**; ④ 14/80 = **0.1750**; ⑤ 12/14 = **0.8571**.
- Pooled AOV = 4,700.00 ÷ 16 = **293.75**.

## 4. Benchmark group and window

### ALG-11 Benchmark group

**Definition.** `group = (brand, platform, type_key)`, where `type_key ∈ {Self-operated, Influencer, All types}` (`spec:269`, 0004 item 7).
- **All types** is pooled: all `ok` sessions of both types, as one population.
- The Type filter picks the group: Type = one → that type; Type = All → All types (`spec:193`, `spec:292`).
- Hosts and Time range do not change the group (C5).

**Inputs.** The filters' Brand, Platform, Type.

**Not enough data.** See ALG-17.

**Edge cases.**
- Platform not connected for the brand: there is no group and no data. The platform is never substituted (`spec:930`).
- Type = All and per-type sub-rows: ALG-28.

**Example.** Filters Thorne · Douyin · Type = All · Hosts = {H1} · Last 30 days → group (Thorne, Douyin, All types). The group's percentiles are the same whatever Hosts or Time range say.

### ALG-12 Rolling window

**Definition.**
- The **current window** for data-as-of date `as_of` is the closed interval of UTC+8 days **[as_of − 89, as_of]**, both ends included: 90 days (`spec:271`; 0004 item 1).
- A session is in the window when `session_day` (ALG-01) is in it.
- The window is recalculated daily, when `as_of` moves. This matches the spec's example "30 Jul – 27 Oct 2026" (`spec:331`): 90 days inclusive.
- A session is part of its own benchmark population (0004 item 2).

**Inputs.** `as_of`, `session_day`.

**Not enough data.** See ALG-17.

**Edge cases.**
- A session that crosses midnight belongs to its start day (DQ-15).
- Sessions with `session_day > as_of` cannot exist, because `as_of` is the last complete day.
- Window length 90 and minimum 20 are spec assumption A3 (`spec:1031`); spec Q4 (`spec:1038`) is still open. Confirm: DQ-35.

**Example** (`as_of` = 2026-10-27, window 2026-07-30 … 2026-10-27, 90 days):

| start_time | UTC+8 day | In window |
|---|---|---|
| 2026-07-29T23:30+08:00 | 2026-07-29 | no |
| 2026-07-30T00:10+08:00 | 2026-07-30 | yes |
| 2026-07-29T16:30Z | 2026-07-30 | yes |
| 2026-10-27T23:59+08:00 | 2026-10-27 | yes |
| 2026-10-28T00:05+08:00 | 2026-10-28 | no |

### ALG-13 Which window grades a value

**Definition.** Every value is graded against the **current window** of the group the filters define, whatever the session's date or the selected time range (`spec:294`, `spec:954`).
- A session from last year is graded against today's window.
- A session's tier can therefore change from day to day as the window moves (`spec:954`).

**Inputs.** The group (ALG-11) and `as_of`.

**Not enough data.** As in ALG-17 and ALG-18.

**Edge cases.** Previous-period and YoY values (ALG-39) are shown as rates and changes only, never tiered, so no historical window is needed for them.

**Example.** With `as_of` = 2026-10-27, a session from 2026-03-02 viewed today is graded against 2026-07-30 … 2026-10-27, not against a window ending 2026-03-01.

## 5. Benchmark statistics

### ALG-14 Percentile method

**Definition.** P25, P50, P75 by **linear interpolation between closest ranks** (0004 item 6):

```
x[0] ≤ x[1] ≤ … ≤ x[n−1]   (the population's values, already rounded per ALG-03)
h  = (n − 1) × p            p ∈ {0.25, 0.50, 0.75}
Pp = x[⌊h⌋] + (h − ⌊h⌋) × (x[⌊h⌋+1] − x[⌊h⌋])     (when ⌊h⌋ = n−1, Pp = x[n−1])
then round Pp to the metric's decimals (ALG-03)
```

- This is Postgres `percentile_cont(p) WITHIN GROUP (ORDER BY x)`, NumPy `percentile(..., method="linear")` (its default) and Excel `PERCENTILE.INC`.
- It is **not** `percentile_disc`.
- **Arithmetic warning.** Postgres `percentile_cont` computes in double precision. Interpolated values can end exactly on a rounding half (fraction 0.5), and in float64 those can round the wrong way (example below). The implementation must interpolate in `numeric` (exact) before rounding: for example, compute the two neighbours with `row_number()` and apply the formula in `numeric`. Alternatively it must pass the tie fixture in golden tests.

**Inputs.** The metric's population (ALG-15).

**Not enough data.** Fewer qualifying values than the metric minimum (ALG-18) → that metric's percentiles are null.

**Edge cases.**
- n = 1 is never reached, because the minimum is 20.
- Equal values are fine: the formula needs no distinct values.

**Example.** Values {0.0100, 0.0200, 0.0300, 0.0400, 0.0500, 0.1000}, n = 6:

| p | h | percentile_cont (this rule) | percentile_disc (not used) |
|---|---|---|---|
| 0.25 | 1.25 | 0.02 + 0.25 × 0.01 = **0.0225** | 0.0200 |
| 0.50 | 2.50 | **0.0350** | 0.0300 |
| 0.75 | 3.75 | **0.0475** | 0.0500 |

**Tie fixture.** P50 of {0.0003, 0.0004} = 0.00035 exactly → **0.0004** (half up). Float64 interpolation followed by Python `round(…, 4)` gives 0.0003.

### ALG-15 Metric populations

**Definition.** For each group and current window, P25/P50/P75 are computed for each metric over these session-level values (`spec:272`). The populations are PROPOSED where marked.

| Metric | Session value | Population: `ok` sessions in the group window with … | Basis |
|---|---|---|---|
| ① Entry rate | ALG-04 | `exposed_uv ≥ 30` | `spec:274` |
| ② Product exposure rate | ALG-04 | `entered_uv ≥ 30` | `spec:274` |
| ③ Product click rate | ALG-04 | `product_exposed_uv ≥ 30` | `spec:274` |
| ④ Click-to-pay rate | ALG-04 | `product_clicked_uv ≥ 30` | `spec:274` |
| ⑤ Retention rate | ALG-04 | `paid_buyers ≥ 3` | `spec:274` |
| CVR | ALG-05 | `entered_uv ≥ 30` | PROPOSED (DQ-13): mirrors 0004 item 3 |
| AOV | ALG-06 | `paid_orders ≥ 1` | PROPOSED (DQ-13) |
| Exposure per session | `exposed_uv` | all `ok` sessions | PROPOSED (DQ-13) |
| Median GMV per buyer (P50 only) | ALG-06 `gmv_per_buyer` | `paid_buyers ≥ 1` | 0001 item 4; population PROPOSED (DQ-16) |

**Not enough data.** See ALG-18.

**Edge cases.** A session whose value is null is not in any population, even if it meets the minimum.

**Example.** Median GMV per buyer over {200.00, 250.00, 350.00, 400.00}: h = 1.5 → 250 + 0.5 × 100 = **300.00**.

### ALG-16 Percentile rank (Benchmark drawer "Nth percentile")

**Definition.** The position of a value within its metric's population, shown as "55th percentile of 91 sessions" (`spec:325`). The spec gives no formula.

PROPOSED (DQ-14), midrank:

```
rank = round0( 100 × (count(x < v) + 0.5 × count(x = v)) ÷ n )
```

**Inputs.** The value v (same rounding as the population) and the population.

**Not enough data.** The metric is not ready (ALG-18) → no rank.

**Edge cases.** A value outside the population (for example an aggregate) uses the same formula; `count(x = v)` may be 0.

**Example** (population from ALG-14, n = 6):
- v = 0.0350 → (3 + 0) ÷ 6 → **50**.
- v = 0.0300 → (2 + 0.5) ÷ 6 = 41.67 → **42**.
- v = 0.1000 → (5 + 0.5) ÷ 6 = 91.67 → **92**.
- v = 0.0100 → 0.5 ÷ 6 = 8.33 → **8**.

## 6. Minimums and Building

### ALG-17 Group minimum and Building

**Definition.** A group is **ready** when its current window has **≥ 20 `ok` sessions**. Otherwise it is **Building**, shown as "Benchmark building (n=k of 20)" (`spec:273`, `spec:932`).
- A Building group assigns no tiers (stage, session, aggregate), no weakest stage, no tags (`spec:273`) and no recoverable revenue (that needs P75, ALG-25).
- Raw values are still shown.

**Inputs.** The count of `ok` sessions in the group window, before any stage minimum.

**Not enough data.** This rule *is* the group-level minimum.

**Edge cases.** All types can be ready while one type group is Building. Only the sub-rows of that type are affected (ALG-28).

**Example.** 19 `ok` + 1 `live` + 2 `quarantined` → **Building (n=19 of 20)**. One more `ok` session → ready.

### ALG-18 Metric minimums

**Definition.** In a ready group, a metric is **ready** when its population (ALG-15) has **≥ 20 qualifying sessions**. Otherwise that metric is **Not enough data** for the whole group: no percentiles and no tiers on that metric.

PROPOSED (DQ-12): the spec sets the 20-session minimum per group (`spec:273`) and the input minimums per stage (`spec:274`), but is silent on a per-stage count.

A **session** is gradeable on a metric when it meets that metric's input minimum:

| Metric | Gradeable when |
|---|---|
| ①–④ | ≥ 30 UV into the stage |
| ⑤ | ≥ 3 paid buyers |
| Session tier (CVR) | `entered_uv ≥ 30` (0004 item 3) |

CVR's minimum is therefore 30 entered for both the population and the session.

**Inputs.** The populations from ALG-15.

**Not enough data.** As defined above.

**Edge cases.** A metric that is ready can still leave a given session "Not enough data" when that session's input is below the minimum.

**Example.** A ready group with 22 `ok` sessions, of which 18 have `product_clicked_uv ≥ 30`: stage ④ is **Not enough data for the group**, and no session gets a ④ tier. Stages with ≥ 20 qualifying sessions are graded normally.

## 7. Tiers

### ALG-19 Tier function

**Definition.** For a value v and a metric's P25 ≤ P50 ≤ P75 (all rounded per ALG-03):

```
v ≥ P75 → STAR    v ≥ P50 → GOOD    v ≥ P25 → MID    otherwise → WEAK
```

(`spec:282-285`, 0004 item 5.) A value on a boundary takes the **higher** tier.

**Inputs.** The rounded value and the rounded percentiles.

**Not enough data.** See ALG-23 for when this function is not called.

**Edge cases.** When P25 = P50 = P75, every value ≥ P75 is STAR and every value below is WEAK. This is correct under the rule.

**Example** (P25 0.0225, P50 0.0350, P75 0.0475):

| v | 0.0475 | 0.0474 | 0.0350 | 0.0225 | 0.0224 |
|---|---|---|---|---|---|
| tier | **STAR** | **GOOD** | **GOOD** | **MID** | **WEAK** |

### ALG-20 Stage tier (session)

**Definition.** `stage_tier = tier(session stage rate, the group's P25/P50/P75 for that stage)`, using the raw (unsmoothed) rate (`spec:290`, 0001 items 2–3).

**Not enough data.** The group is Building, or the stage metric is not ready, or the session is below that stage's input minimum (ALG-18).

**Edge cases.** The rate is null → Not enough data.

**Example.** S-A ③ = 0.2500 against P25 0.2000, P50 0.2400, P75 0.3000 → **GOOD**.

### ALG-21 Session tier

**Definition.** `session_tier = tier(cvr, the group's CVR P25/P50/P75)` (`spec:291`, 0001 item 1). There is no composite and no smoothing (0001 item 3).

**Not enough data.** The group is Building, or the CVR metric is not ready, or `entered_uv < 30` (0004 item 3).

**Edge cases.** CVR 0.0000 with entered ≥ 30 is graded, normally WEAK.

**Example** (CVR P25 0.0225, P50 0.0350, P75 0.0475):
- S-A: entered 300, CVR 0.0400 → **GOOD**.
- S-B: entered 100, CVR 0.0200 → **WEAK**.
- S-C: entered 25, CVR 0.0400 → **Not enough data**.

### ALG-22 Aggregate tier

**Definition.** `aggregate_tier = tier(pooled rate of the selection (ALG-10), the group's session-level P25/P50/P75)` (`spec:292`). It is used for KPI cards, Live Funnel rows, host funnel cells and the host CVR tier.

**Not enough data.** PROPOSED (DQ-19): the stage minimums are applied to the **pooled** inputs: Σ UV into the stage ≥ 30 (①–④, and CVR on Σ entered), Σ paid buyers ≥ 3 (⑤). The group must be ready and the metric ready.

**Edge cases.**
- The Overview host CVR column is a plain number with no tier (`spec:571`).
- The channel comparison shows no tiers (`spec:429`).

**Example.** S-A + S-B pooled CVR 0.0350 (Σ entered 400 ≥ 30) against P25 0.0225 / P50 0.0350 / P75 0.0475 → **GOOD** (on the P50 boundary, so it goes up).

### ALG-23 Precedence of non-tier states

**Definition.** For any graded value, the first matching state wins:
1. Platform not connected → no data (`spec:930`).
2. Group **Building** → "Benchmark building (n=k of 20)" (ALG-17).
3. Metric not ready, or input below its minimum → **Not enough data** (ALG-18, ALG-22).
4. Otherwise → the tier (ALG-19).

A small sample never shows WEAK (`spec:293`, `spec:933`).

**Inputs.** The states above.

**Not enough data.** As listed.

**Edge cases.** `live` and `quarantined` sessions get no tier at all; they show their status tag (ALG-02).

**Example.** A session with entered 25 in a ready group shows **Not enough data** for session tier, even though its CVR (0.0000) is below P25.

## 8. Weakest stage

### ALG-24 Weakest stage

**Definition.** Among stages ①–⑤ that **have a tier**, the weakest stage is the one with the lowest tier (WEAK < MID < GOOD < STAR). Ties go to the stage with more UV lost (ALG-09) (`spec:263`, 0001 item 6). PROPOSED (DQ-18): a second tie (same tier, same UV lost) goes to the **earlier** stage.
- Sessions use session stage tiers and UV lost.
- Aggregates (the Live Funnel weakest marker, `spec:445`) use aggregate tiers and pooled UV lost.

**Not enough data.** No stage has a tier → weakest stage is null.

**Edge cases.** Stages without a tier are skipped. They are not treated as WEAK.

**Example.**
- S-A tiers ① MID, ② WEAK, ③ WEAK, ④ GOOD, ⑤ STAR with UV lost 1,700 / 60 / 180 / 48 / 2 → ② and ③ tie on WEAK; ③ lost more (180 > 60) → **③**.
- Double tie: tiers GOOD, WEAK, WEAK, STAR, STAR with UV lost 100 / 50 / 50 / 10 / 1 → **②**.

## 9. Recoverable revenue

### ALG-25 Session recoverable revenue

**Definition** (`spec:261`, 0001 item 4):

```
recoverable = round2( entered_uv × max(0, P75_CVR − cvr) × gpb )
gpb = gmv_per_buyer (ALG-06)                      if paid_buyers ≥ 1
    = the group's median GMV per buyer (ALG-15)   if paid_buyers = 0
```

- P75_CVR and the median come from the **grading group's current window**: the group the filters define (ALG-11, ALG-13).
- The median's population includes the session itself (0004 item 2).
- `cvr` is the 4-dp CVR (ALG-05).
- PROPOSED (DQ-16).

**Inputs.** `entered_uv`, `cvr`, `gmv`, `paid_buyers`; the group's CVR P75 and median GMV per buyer.

**Not enough data → null (not 0).** The group is Building, or the CVR metric is not ready, or (zero-buyer case) the median GMV per buyer population has fewer than 20 sessions.

Eligibility, PROPOSED (DQ-16): every `ok` session with `entered_uv > 0`. The spec sets no minimum ("Σ per session", `spec:261`), so the session-tier minimum of entered ≥ 30 does **not** apply here. Recoverable revenue is a separate answer from the tier (AGENTS.md rule 8).

**Edge cases.**
- `entered_uv = 0` → recoverable 0.00. There is no upside without entrants.
- A CVR at or above P75 → 0.00.
- `live` and `quarantined` → null.

**Example** (group CVR P75 0.0475, median GMV per buyer 300.00):

| Session | entered | buyers | CVR | gpb | recoverable |
|---|---|---|---|---|---|
| S-A | 300 | 12 | 0.0400 | 350.00 | 300 × 0.0075 × 350 = **787.50** |
| S-B | 100 | 2 | 0.0200 | 250.00 | 100 × 0.0275 × 250 = **687.50** |
| S-D | 200 | 0 | 0.0000 | 300.00 (median) | 200 × 0.0475 × 300 = **2,850.00** |
| S-E | 400 | 20 | 0.0500 | 300.00 | **0.00** (above P75) |

### ALG-26 Aggregate recoverable revenue

**Definition.** `Σ session recoverable` over the `ok` sessions in scope. Every session is graded against the one group the filters define. With Type = All that is the All types group (`spec:261` "All types when Type = All"; 0004 item 7).

**Not enough data.** The group is Building or CVR is not ready → null.

Null sessions are left out of the sum, and their count is returned beside it ("n sessions not counted").

**Edge cases.** Under Type = All, a session's recoverable revenue can differ from its value under its own Type, because P75 differs. Every view names the group it used (`spec:294`).

**Example.** S-A + S-B + S-D + S-E = 787.50 + 687.50 + 2,850.00 + 0.00 = **4,325.00**.

### ALG-27 Annualised recoverable revenue

**Definition.** The spec says the hover value "uses the annual GMV from the platform MCP" (`spec:261`, `spec:952`), but gives no formula. **No such input exists in this repo**: no MCP source is approved (DQ-5).

Until DQ-17 is decided, the annualised value is **null**, and Serve says "not available".

**Candidate formulas** (UNVERIFIED, for DQ-17):
- A: `recoverable × annual_gmv ÷ period_gmv`
- B: `recoverable × 365 ÷ days_in_range`

**Inputs.** Annual GMV per brand × platform (missing).

**Not enough data.** Always null today.

**Edge cases.** For candidate A, `period_gmv = 0` → null.

**Example** (candidate formulas only, recoverable 4,325.00 over 30 days, period GMV 20,000.00, annual GMV 1,000,000.00):
- A → **216,250.00**
- B → **52,620.83**

The two disagree by 4×, which is why DQ-17 needs a decision.

## 10. Type = All

### ALG-28 Type = All, per-type rows, and the "no pooled group" fallback

**Definition.**
- With Type = All, every session, host, KPI and the combined Live Funnel row is graded against **Brand × Platform × All types** (pooled; `spec:269`, `spec:292`, 0004 item 7).
- The Live Funnel's Self-operated and Influencer **sub-rows** are graded against their own type groups (`spec:459`, `spec:934`).
- The channel comparison shows no tiers (`spec:429`).
- **The "no pooled All types group" fallback** (`spec:276`, `spec:935`, `spec:654`) applies only "where the All types group cannot be built (no session-level values)". Every room-export row is a session-level value, so this condition cannot arise in v1. PROPOSED (DQ-20): the fallback is not implemented.

**Not enough data.** As in ALG-17 and ALG-18, per group. A sub-row whose type group is Building shows Building while the combined row is graded.

**Edge cases.** A type with no sessions in scope gets no sub-row. The channel comparison needs both types to have sessions (`spec:425`).

**Example.** An influencer session with CVR 0.0300:
- Type = All, All types group P25/P50/P75 0.0100 / 0.0250 / 0.0350 → **GOOD**.
- Type = Influencer, Influencer group P25/P50/P75 0.0050 / 0.0100 / 0.0200 → **STAR**.

Both are correct; the view names the group.

## 11. Hosts

### ALG-29 Host pooled metrics

**Definition.**
- A host is `host_id` within brand × platform. Its metrics pool its `ok` sessions in the **time range** (`spec:568-574`) using ALG-10.

| Column | Formula |
|---|---|
| Sessions | count |
| GMV | Σ gmv |
| Avg GMV / session | round2(GMV ÷ Sessions) |
| AOV | round2(Σ gmv ÷ Σ paid_orders) |
| CVR | round4(Σ paid_buyers ÷ Σ entered) |
| Exposure / session | round2(Σ exposed ÷ Sessions) |
| ①–⑤ | ALG-04 on the sums |
| Last live | max `session_day` |
| Total exposure | Σ exposed |
| Paid orders | Σ paid_orders |
| Best session GMV | max gmv |

- Funnel cells are tiered with ALG-22 against the group the filters define (`spec:557`, `spec:573`).
- The CVR column has no tier (`spec:571`).

**Not enough data.** Per cell, ALG-22. Row greying: ALG-30.

**Edge cases.** A host with no `ok` sessions in range: counts are 0, rates null, "No lives in this range" (ALG-30).

**Example.** Host H1 = S-A + S-B:
- Sessions 2, GMV **4,700.00**, Avg GMV / session **2,350.00**, AOV **293.75**, CVR **0.0350**.
- Exposure / session **1,500.00**.
- ① **0.1333** ② **0.7250** ③ **0.2759** ④ **0.1750** ⑤ **0.8571**.
- Best session GMV **4,200.00**.

### ALG-30 Leaderboard membership, rank and greying

**Definition.**
- **Membership.** PROPOSED (DQ-8, DQ-9): every host of the brand × platform (and of the Type filter's type) that has **any landed session**. Hosts with no `ok` session in the range are listed **last**, with "No lives in this range". This follows `spec:579` and `spec:936`, and the demo scenario at `spec:1087`, over R24's "hosts without sessions hidden" (`spec:1000`). The Hosts filter limits the rows (`spec:215`).
- **Rank.** Total GMV descending. Ties → `host_id` ascending. PROPOSED (DQ-31). Hosts without lives come after all hosts with lives, ordered by `host_id`.
- **Greying.** PROPOSED (DQ-10): a row is greyed "Not enough data" when the host has fewer than 3 `ok` sessions or fewer than 10 paid orders in the range. This reuses the tag eligibility of `spec:703`. Its funnel cells then show "n/a".

**Not enough data.** As defined above.

**Edge cases.**
- Greyed hosts keep their rank (`spec:566`).
- A host whose type does not match the Type filter is not listed.

**Example.** H2 (GMV 4,700.00, 3 sessions), H1 (4,700.00, 2), H3 (900.00, 1), H4 (no lives) → **#1 H1, #2 H2, #3 H3, #4 H4** ("No lives in this range").
- H1 is ahead of H2 because their GMV ties and `host_id` H1 < H2.
- H3 is greyed: 1 session.

## 12. Reach × AOV tags (influencers)

### ALG-31 Tag inputs and thresholds

**Definition** (`spec:676-683`, `spec:712-726`):
- **Window:** always the group's **current 90-day window**, never the time range. Redrawing the map for the selected range is spec Q7 (`spec:1041`), out of v1 (DQ-34).
- **Group:** Brand × Platform × **Influencer**, whatever the Type filter (`spec:557`).
- **Host inputs:**
  - `exposure_per_session = round2(Σ exposed ÷ sessions)`
  - `pooled_aov = round2(Σ gmv ÷ Σ paid_orders)`
  - Both computed over the host's `ok` sessions in that window.
- **Thresholds:** the Influencer group's P50 of exposure per session and P50 of AOV (ALG-15).
- Self-operated hosts get no tag ("Not tagged", `spec:726`).

**Not enough data.** See ALG-32.

**Edge cases.** A host can have a tag and still show no lives in the selected range, because the tag window ≠ the range.

**Example.** Group P50 exposure per session **20,000.00**, P50 AOV **300.00**. Host X has 5 sessions, 40 orders, exposure / session 25,000.00 and AOV 280.00.

### ALG-32 Tag eligibility

**Definition.** The first match wins (`spec:703-704`, `spec:717-718`):
1. Self-operated → "Not tagged".
2. Influencer group Building → "Benchmark building".
3. Host has fewer than 3 `ok` sessions or fewer than 10 paid orders in the window → "Not enough data".
4. Otherwise → a quadrant (ALG-33).

The exposure and AOV metrics must also be ready (ALG-18). If either is not, the host is "Not enough data". PROPOSED (DQ-12).

**Not enough data.** As defined above.

**Edge cases.** Exactly 3 sessions and 10 orders is eligible.

**Example.**
- Z: 2 sessions, 15 orders → **Not enough data**.
- V: 3 sessions, 9 orders → **Not enough data**.
- X: 5 sessions, 40 orders → eligible.

### ALG-33 Quadrant and borderline

**Definition** (`spec:689-694`, `spec:720-724`):

```
hi_reach = exposure_per_session ≥ P50_exposure
hi_aov   = pooled_aov           ≥ P50_aov
(T,T) Flagship · (T,F) Traffic Engine · (F,T) Premium Niche · (F,F) Under Review
borderline = |exposure_per_session ÷ P50_exposure − 1| ≤ 0.10  or  |pooled_aov ÷ P50_aov − 1| ≤ 0.10
```

- The borderline ratios are computed exactly (C1) and are **not** rounded before comparing.
- Ties at P50 go high.
- ±10% is inclusive.

**Not enough data.** ALG-32.

**Edge cases.** A P50 of 0 would divide by zero. AOV P50 cannot be 0, because its population has ≥ 1 order. Exposure P50 of 0 → borderline false. This is UNVERIFIED as reachable.

**Example** (P50s 20,000.00 / 300.00):

| Host | exposure / session | AOV | Quadrant | Borderline |
|---|---|---|---|---|
| X | 25,000.00 (+25%) | 280.00 (−6.67%) | **Traffic Engine** | **yes** (AOV) |
| Y | 19,000.00 (−5%) | 400.00 (+33.33%) | **Premium Niche** | **yes** (reach) |
| W | 20,000.00 (0%) | 330.00 (+10.00%) | **Flagship** | **yes**: exactly +10% is inclusive |

For W, float64 gives `330/300 − 1 = 0.10000000000000009`, which would wrongly fail the test (C1).

### ALG-34 Hysteresis (2 consecutive recalculations)

**Definition.** Each daily recalculation `d` computes `computed[d]` (ALG-32/33). The **official** tag follows these rules (`spec:706`, `spec:725`). Details are PROPOSED (DQ-21).
- **First recalculation** for a host, or when the previous official value is a status ("Not tagged", "Benchmark building", "Not enough data"): `official[d] = computed[d]`.
- **Status values apply at once.** When `computed[d]` is a status, `official[d] = computed[d]`. The pseudocode assigns these before `apply_hysteresis` (`spec:717-718`).
- **Quadrant change.** When `computed[d]` is a quadrant ≠ `official[d−1]`, the official tag changes only if `computed[d] = computed[d−1]`. Otherwise `official[d] = official[d−1]`.
- "Consecutive" means consecutive recalculations that ran, not calendar days. A missed day does not reset the count.

**Inputs.** The stored history (ALG-37).

**Not enough data.** ALG-32.

**Edge cases.** Borderline is recomputed daily from the current inputs and does not wait for hysteresis.

**Example.**

| Day | computed | official |
|---|---|---|
| 1 | Flagship | **Flagship** (first) |
| 2 | Traffic Engine | Flagship |
| 3 | Flagship | Flagship |
| 4 | Traffic Engine | Flagship |
| 5 | Traffic Engine | **Traffic Engine** (held 2 recalculations) |
| 6 | Traffic Engine | Traffic Engine |

### ALG-35 Change marker

**Definition.** Shown when the official tag changed from one quadrant to another quadrant on a day `c` with `c ≥ as_of − 29`, i.e. within the 30 days ending on `as_of` (`spec:699`). It names the previous official quadrant ("from Premium Niche").
- The spec's example "↑" has no defined direction. PROPOSED (DQ-22): no arrow, only "from {tag}", until UX defines an order.
- Changes to or from a status do not create a marker.

**Inputs.** The tag history (ALG-37).

**Not enough data.** None.

**Edge cases.** Several changes within 30 days → the most recent one is shown.

**Example.** A change on 2026-09-28: with `as_of` 2026-10-27 the marker is **shown**; with `as_of` 2026-10-28 it is **not shown**.

### ALG-36 Host CVR tier (secondary signal)

**Definition.** `cvr_tier = tier(host pooled CVR over the tag window, the Influencer group's CVR P25/P50/P75)`. It is the small Tag beside the quadrant tag (`spec:698`).

PROPOSED (DQ-23): the tag's group and window are used, because tags "stay on the influencer group" (`spec:557`). The ALG-22 pooled minimum applies: Σ entered ≥ 30.

**Not enough data.** The group is Building, or CVR is not ready, or Σ entered < 30. Hosts that are "Not enough data" for the tag show no CVR tier.

**Edge cases.** Only influencers get a CVR tier.

**Example.** Pooled CVR 0.0350 against 0.0050 / 0.0100 / 0.0200 → **CVR STAR** ("Traffic Engine · CVR STAR").

### ALG-37 Tag history (what must be stored)

**Definition.** One row per influencer host per recalculation. It is needed for hysteresis (ALG-34), the change marker (ALG-35) and auditability (`spec:955`).

| Field | Example |
|---|---|
| `as_of` | 2026-10-27 |
| `window_from`, `window_to` | 2026-07-30, 2026-10-27 |
| `brand`, `platform`, `host_id` | Thorne, douyin, H-X |
| `group_status`, `group_n` | ready, 91 |
| `sessions`, `paid_orders` | 5, 40 |
| `exposure_per_session`, `pooled_aov`, `pooled_cvr` | 25000.00, 280.00, 0.0350 |
| `p50_exposure`, `p50_aov` | 20000.00, 300.00 |
| `computed` | Traffic Engine |
| `official` | Traffic Engine |
| `borderline` | true |
| `cvr_tier` | STAR |
| `changed_from` (null unless official changed this day) | Flagship |

**Not enough data.** Rows are stored for status values too.

**Edge cases.** The history is append-only; a recalculation is never edited. A re-run for the same `as_of` replaces that day's row (idempotent).

**Example.** The row above records the day-5 change in the ALG-34 table.

## 13. Time

### ALG-38 Time range and time gates

**Definition.**
- **Anchor.** Presets end on `as_of`, not on the calendar today (PROPOSED, DQ-24) (`spec:195`):

| Preset | Range |
|---|---|
| Last N days | [as_of − (N−1), as_of] |
| This month | [first day of as_of's month, as_of] |
| Last month | the full previous calendar month |
| This quarter | [first day of as_of's quarter, as_of] |
| Custom | inclusive start and end days |

- **Time gate** = one bucket at the granularity (`spec:371`). Day = a UTC+8 day. Week = an ISO week, **Monday–Sunday** (PROPOSED, DQ-25). Month = a calendar month. Sessions fall in the gate of their `session_day`.
- **Auto granularity** (`spec:196`): **Day** if the range is ≤ 31 days; **Week** if ≤ 6 months, i.e. `start ≥ (end shifted back 6 calendar months) + 1 day`; else **Month** (PROPOSED, DQ-25).
- **GMV by time gate** shows the last 7 gates, ending with the gate that contains the range end (`spec:423`). A gate cut by the range end is partial and is labelled partial (DQ-25).

**Inputs.** `as_of`, the preset or custom dates, and the granularity.

**Not enough data.** None. Empty gates show 0 GMV and 0 sessions.

**Edge cases.** A custom end after `as_of` is clamped to `as_of`.

**Example** (`as_of` 2026-10-27, a Tuesday):
- Last 30 days = **2026-09-28 … 2026-10-27**. This month = 2026-10-01 … 2026-10-27. Last month = 2026-09-01 … 2026-09-30.
- Last 7 day gates = 2026-10-21 … 2026-10-27.
- Last 7 week gates start on Mondays 2026-09-14, 09-21, 09-28, 10-05, 10-12, 10-19, **10-26** (partial, to 10-27).
- Auto granularity: 30 days → Day. 2026-07-30 … 10-27 (90 days) → Week. 2026-04-28 … 10-27 (183 days) → Week. 2026-04-27 … 10-27 (184 days) → Month.

### ALG-39 Previous period, MoM, YoY and change values

**Definition** (`spec:372-374`):
- **Previous period** = the same number of days, ending the day before the range starts.
- **MoM** = both range ends shifted back 1 calendar month. **YoY** = both shifted back 12 months.
- A day that does not exist is **clamped** to the month's last day, e.g. 31 Mar → 28/29 Feb (PROPOSED, DQ-26).
- **Change values:**
  - Counts and currency: `pct_change = round4((cur − prev) ÷ prev)`.
  - Rates: `pp_change = cur − prev`, on the 4-dp rates. 0.0050 = +0.50 pp.
- Previous-period values are aggregates (ALG-10) and are never tiered.

**Not enough data.** `prev = 0` or null → `pct_change` null (shown "n/a"). The spec asks for YoY "as a plain percentage, even on a tiny base" (`spec:423`), so a small non-zero base is still shown.

**Edge cases.** MoM and YoY ranges can overlap the current range for long ranges. This is accepted as specified.

**Example** (current = 2026-09-28 … 2026-10-27):
- Previous = 2026-08-29 … 2026-09-27. MoM = 2026-08-28 … 2026-09-27. YoY = 2025-09-28 … 2025-10-27.
- Clamp: 2026-03-31 → MoM 2026-02-28. 2028-02-29 → YoY 2027-02-28.
- GMV 12,000.00 vs 10,000.00 → **0.2000** (+20.0%). CVR 0.0350 vs 0.0300 → **+0.0050** (+0.50 pp).

---

## Stored or computed

**Status: PROPOSED.** It answers DQ-1. Only Rey accepts.

**The question.** Benchmarks and tiers "follow the filters, recalculated live" (`spec:270`, `spec:294`). The spec also says "a daily job computes P25/P50/P75 per Brand × Platform × Type … Results are stored with their window dates" (`spec:953`), and 0004 item 1 recalculates the window daily.

**What "follows the filters" actually needs.** Under C5 and ALG-11, the only filters that change grading are Brand × Platform × Type. That gives at most **3 groups per brand × platform**. Hosts and Time range only select which values are graded, never the percentiles. So "follows the filters" means *pick the right one of three stored snapshots*. It does not require recomputing percentiles per request.

| Option | How | "Follows the filters" | Reproducing a past grade | Cost and risk |
|---|---|---|---|---|
| A. Daily job stores everything | Nightly: benchmark snapshot per group, plus a tier for every session × group (3 per session) | Yes: all 3 groups are pre-graded | Yes, if every day's tiers are kept | Writes every session × 3 groups every day, because tiers change as the window moves (ALG-13). Aggregate tiers of arbitrary selections (Hosts × Time range) still can't be precomputed, so it becomes a hybrid anyway |
| B. All at read time | Percentiles computed from session records per request | Yes | Only by re-running with the old `as_of` and the data as it was then; re-landed data (DQ-29) breaks this | Percentiles over 90 days × group on every request; no stored "as of" for the drawer (`spec:275`) |
| **C. Hybrid (recommended)** | Daily job stores a **benchmark snapshot** per (as_of, group): window dates, n included / excluded / hosts, P25/P50/P75 per metric, metric status, median GMV per buyer. It also stores **tag history** (ALG-37). **Tiers, weakest stage and recoverable revenue are computed at read time** from session values plus the current snapshot | Yes: read time picks the snapshot for the filtered group | Yes: a grade = f(session values, snapshot for that as_of). Snapshots are kept, never overwritten | One small row per group per day. Read-time grading is a comparison against 3 numbers. Aggregate tiers work for any selection |

**Recommendation: C.**
- Tag history must be stored anyway, because hysteresis needs yesterday's state.
- Benchmark snapshots must be stored with window dates anyway (`spec:275`).
- Everything else is a cheap pure function of stored inputs, so step 06's reference implementation and the BE share one definition.

**Consequence.** "Recalculated live" (R9, `spec:986`) is satisfied by read-time grading against the current snapshot. It does not mean recomputing percentiles per request.

## Where the generator differs

`upstream/design-pack/generate_demo_data.py` is not a reference. Its outputs are never expected values (`tests/golden/README.md`).

| # | Rule | Spec / decisions say | Generator does | Where |
|---|---|---|---|---|
| 1 | Window end | Current window ending on `as_of` (`spec:294`, 0004 item 1) | Window ends the day **before each session** | `gen:209` (`gd < d`) |
| 2 | Own session in population | Included (0004 item 2) | Excluded | `gen:209` |
| 3 | All types group | Pooled All types group (`spec:269`, 0004 item 7) | Only Brand × Platform × Type, no All types | `gen:196`, `gen:251` |
| 4 | Session tier minimum | entered ≥ 30 (0004 item 3) | entered > 0 | `gen:237` |
| 5 | Session tier rule | CVR quartile (0001) | Also computes a harmonic composite into `session_tier` | `gen:227-233` |
| 6 | Rounding before grading | Rates rounded to 4 dp before grading (0004 item 4); half up (ALG-03, PROPOSED) | Grades unrounded floats; rounds only stored percentiles, with NumPy half-to-even | `gen:220`, `gen:238`, `gen:261` |
| 7 | Recoverable | Uses rounded CVR and P75 of the group the filters define; zero-buyer median from the current window, own session included (ALG-25) | Unrounded CVR and P75 from the day-before window; median from that window, excluding the session, own type only | `gen:237-245` |
| 8 | Stage needs 20 qualifying sessions | Spec silent; PROPOSED yes (ALG-18, DQ-12) | Yes, `len(sorted_cols[i]) < MIN_BENCH` | `gen:219` (agrees with the proposal) |
| 9 | CVR population | entered ≥ 30 (PROPOSED, ALG-15) | Every session with entered > 0 | `gen:259` |
| 10 | Kept buyers / refunds | `kept = paid_buyers − refunding_users` (PROPOSED, ALG-01) | Simulates `kept_buyers` and sets `refund_orders = paid − kept` (buyers used as orders) | `gen:141` |
| 11 | Host exposure per session | round2 (ALG-31) | Rounded to an integer before comparing | `gen:276` |
| 12 | Host CVR tier | Pooled Σ entered ≥ 30 (PROPOSED, ALG-36) | Needs ≥ 3 sessions | `gen:302` |
| 13 | Borderline | Exact arithmetic (C1) | Float division `≤ .10` | `gen:299-300` |
| 14 | Hysteresis, change marker, tag history | Required (`spec:699`, `spec:706`) | None: one snapshot only | whole file (no match for "hyster" or "history") |
| 15 | Annual GMV | From the platform MCP; not available (ALG-27) | Last-12-months GMV × random 3.5–5.0 | `gen:312`, `gen:315` |
| 16 | Benchmark snapshot window | [as_of − 89, as_of] (ALG-12) | `w_from = AS_OF − 89` | `gen:249` (agrees) |

## Open items

Every item below is also in [decision-queue.md](decision-queue.md) as **PROPOSED**. Each lists options, a recommendation (the "PROPOSED" behaviour this spec uses until decided) and an owner. Items already in the queue before step 05 are referenced, not repeated: DQ-1 (stored or computed, answered above), DQ-2 (quarantine rules), DQ-3 (退款人数 attribution), DQ-4 (Action Card expected recovery), DQ-5 (data source), DQ-6 (Okta), DQ-7 (decision 0002).

| DQ | Gap or contradiction | Options | Recommendation | Owner | Rules |
|---|---|---|---|---|---|
| DQ-8 | **R24 vs §7.2/§12.** R24 says "hosts without sessions hidden" (`spec:1000`); §7.2 says they are "listed last with 'No lives in this range'" (`spec:579`), and so do §12 (`spec:936`) and the demo scenario (`spec:1087`) | a) hide; b) list last | **b**: three later, more detailed passages agree, and a demo scenario exists | Rey | ALG-30 |
| DQ-9 | Which hosts exist for "no lives in range"? The room export only knows hosts that went live | a) any landed session ever; b) a session in the last N days; c) a host registry (no source) | **a**, for that brand × platform (× type) | Rey | ALG-30 |
| DQ-10 | The "minimum sample" that greys a leaderboard host is undefined (`spec:579`) | a) tag eligibility (≥ 3 sessions and ≥ 10 orders); b) per-cell pooled minimums only; c) ≥ 1 session | **a** for the row, plus per-cell ALG-22 minimums | Rey | ALG-29, ALG-30 |
| DQ-11 | Rounding: mode, which values, and whether percentiles are rounded; only "4 decimals before grading" is decided (0004 item 4) | a) half up, exact decimal, round once (ALG-03); b) half even; c) round only at display | **a** | Claude Code drafts, Rey approves | ALG-03, ALG-14 |
| DQ-12 | Does a stage (or CVR, AOV, exposure) need ≥ 20 qualifying sessions? The spec is silent (`spec:273-274`) | a) yes, per metric; b) no: any qualifying count once the group has 20 | **a**: percentiles of 3 values are not a benchmark | Rey | ALG-18, ALG-32 |
| DQ-13 | CVR, AOV and exposure populations and minimums are not stated | CVR: entered ≥ 30 or > 0; AOV: orders ≥ 1 or ≥ 3; exposure: all | **CVR entered ≥ 30; AOV orders ≥ 1; exposure all `ok`** | Rey | ALG-15 |
| DQ-14 | Percentile-rank formula for "Nth percentile" (`spec:325`) is undefined | a) midrank; b) `count(<v)/n`; c) `count(≤v)/n` | **a**: symmetric, and ties sit in the middle | Claude Code drafts, Rey approves | ALG-16 |
| DQ-15 | Which day a session belongs to | a) start time UTC+8; b) end time; c) split | **a**: start time is what the UI shows (`spec:477`) | Rey | ALG-01, ALG-12, ALG-38 |
| DQ-16 | Recoverable revenue: eligibility, CVR precision, median population | Eligibility: entered > 0 or ≥ 30; CVR: 4 dp or exact; median: grading group's current window incl. self, or own type | **entered > 0 (the spec sets no minimum); 4-dp CVR; median of the grading group's current window, self included, ≥ 20 buyers' sessions; null when Building** | Rey | ALG-25, ALG-26 |
| DQ-17 | Annualised recoverable: no formula in the spec (`spec:261`), and no input exists | a) × annual GMV ÷ period GMV; b) × 365 ÷ days; c) drop | **Null until DQ-5**, then a or b by Rey | Rey | ALG-27 |
| DQ-18 | Weakest stage: second tie (same tier and same UV lost); no stage graded | Earlier stage, later stage, or "none" | **Earlier stage; null when nothing graded** | Rey | ALG-24 |
| DQ-19 | Aggregate tiers have no stated minimum | a) stage minimums on pooled inputs; b) none | **a** | Rey | ALG-22, ALG-36 |
| DQ-20 | The "no pooled All types group" fallback (`spec:276`, `spec:935`, `spec:654`) can't trigger with room-export data; 0004's "supersedes" note on it was Claude Code's wording | a) drop it; b) implement it anyway | **a** | Rey | ALG-28 |
| DQ-21 | Hysteresis details: first calculation, status transitions, missed days | As in ALG-34, or require 2 days for status changes too | **As in ALG-34** (status values apply at once, per `spec:717-718`) | Rey | ALG-34 |
| DQ-22 | The change marker's "↑" has no defined direction (`spec:699`) | a) no arrow; b) an order of tags; c) arrow = AOV direction | **a** until UX decides | Rey (UX) | ALG-35 |
| DQ-23 | Host CVR tier: group, window, minimum | Influencer group + tag window, or filter group + time range | **Influencer group, tag window, Σ entered ≥ 30** | Rey | ALG-36 |
| DQ-24 | What the time-range presets are relative to | a) `as_of`; b) calendar today | **a**: today's partial data would otherwise look like a drop | Rey | ALG-38 |
| DQ-25 | Week definition, "≤ 6 months", partial gates | ISO Mon–Sun vs Sun–Sat; 6 calendar months vs 183 days | **ISO Mon–Sun; 6 calendar months; partial gates labelled** | Rey | ALG-38 |
| DQ-26 | MoM/YoY month-end handling; change when prev = 0 | Clamp vs roll forward; null vs ∞ | **Clamp; null** | Rey | ALG-39 |
| DQ-27 | Room-export fields for stage ⑤ and refund rate: kept buyers and refunded orders are not in the reported columns ([room-export.md](data-model/room-export.md)) | Derive (ALG-01, ALG-07, ALG-08) or add fields to the export | **Derive as proposed; verify against a real header** (also R36 / G3 provisional retention, `spec:1012`, `spec:1182`) | Rey + data owner | ALG-01, ALG-07 |
| DQ-28 | How Land knows a session is `live` | a) a status column; b) end time missing; c) export time < end time | **Decide from a real header** (UNVERIFIED) | Rey + data owner | ALG-02 |
| DQ-29 | Re-exports of the same session (e.g. refunds change) | a) latest file wins, history kept; b) first wins | **a** | Rey | ALG-02 |
| DQ-30 | "Largest difference" sentences (`spec:430`, `spec:653`): no metric or measure defined | Relative (×) vs absolute (pp) difference; which metrics | **Claude Code drafts a rule with the contract**; numbers from Score, text from templates (R39) | Claude Code drafts, Rey approves | BE-24 |
| DQ-31 | Leaderboard rank ties | `host_id` vs name vs sessions | **`host_id` ascending** (stable) | Rey | ALG-30 |
| DQ-32 | Avg watch time column and its unit | Per entered user vs per viewer-minute | **Verify against a real header** (UNVERIFIED) | Rey + data owner | ALG-08 |
| DQ-33 | How `as_of` is set | a) the latest complete export day from the file log; b) the sync date − 1 | **a** (UNVERIFIED: file-log fields are TBD, [scope.md](scope.md)) | Rey + data owner | C4, ALG-12 |
| DQ-34 | Spec Q7: the map follows the time range or only the 90-day tag (`spec:1041`) | Official tag only in v1, or both | **Official tag only in v1** | Rey | ALG-31 |
| DQ-35 | Spec Q4: 90 days and 20 sessions confirmed? A longer window for self-operated (G9)? (`spec:1038`) | Keep A3, or a longer self-operated window | **Keep 90 / 20 for all groups in v1** | Rey | ALG-12, ALG-17 |
