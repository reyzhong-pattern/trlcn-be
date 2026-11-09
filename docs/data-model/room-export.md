# Room export — data model

**Source file read: none.** No room-export file was attached to or readable in the bootstrap session (2026-11-09; `/mnt/user-data/uploads` and `/mnt/attach` were empty). **Every column name below is UNVERIFIED** until someone reads the header row of a real room-export file and records the file name here. Do this by reading the header only; never commit the file (it belongs under git-ignored `data/`).

- **Grain:** one row per live session (live room). UNVERIFIED.
- **Producer:** Compass, via Fetch (out of scope). Hand-over: raw file + file log ([../scope.md](../scope.md)).
- **Encoding, sheet name, header row position, number formats (e.g. 万, %, thousands separators):** UNVERIFIED.

## Funnel and order columns (builder-reported mapping)

| Field (this repo) | Compass column (zh) | Meaning | Used for | Status |
|---|---|---|---|---|
| `exposed_uv` | 曝光人数 | Live exposure UV | Stage ① input | UNVERIFIED |
| `entered_uv` | 观看人数 | De-duplicated users who entered the room (definition in [decision 0003](../decisions/0003-entered-uv-definition.md), ACCEPTED). UI label 进房人数 | Stage ① output, ② input, CVR denominator | Mapping ACCEPTED (0003); column presence in a file UNVERIFIED |
| `product_exposed_uv` | 商品曝光人数 | UV who saw a product | Stage ② output, ③ input | UNVERIFIED |
| `product_clicked_uv` | 商品点击人数 | UV who clicked a product | Stage ③ output, ④ input | UNVERIFIED |
| `paid_buyers_uv` | 成交人数 | Paying buyers (UV) | Stage ④ output, ⑤ input, CVR numerator | UNVERIFIED |
| `paid_orders` | 成交订单数 | Paid orders | AOV, quarantine rule 6 | UNVERIFIED |
| `number_of_refunding_users` | 退款人数 | Users who refunded | Stage ⑤ (see open item) | UNVERIFIED; attribution (refund time vs order time) open in [decision queue](../decision-queue.md) |
| `gmv` | 用户支付金额 | Amount paid by users (¥) | GMV, AOV, recoverable revenue | UNVERIFIED (unit, before/after refunds) |

## Session metadata columns

The spec needs session ID, host ID, type, platform, start and end time, and live topic (`upstream/design-pack/03-product-spec-v0.4.md:957`). Their Compass column names are **all UNVERIFIED** (not reported by the builder):

| Field | Compass column | Status |
|---|---|---|
| `session_id` | ? | UNVERIFIED |
| `host_id`, `host_name` | ? | UNVERIFIED |
| `type` | ? — values 自营 → Self-operated, 合作 → Influencer (mapping per [decision 0004](../decisions/0004-hifi-wins-and-resolved-rules.md)) | Column UNVERIFIED |
| `platform` | ? (may come from the file log rather than a column) | UNVERIFIED |
| `brand` | ? (may come from the file log) | UNVERIFIED |
| `start_time`, `end_time` / duration | ? (timezone: spec assumes UTC+8, `03-product-spec-v0.4.md:1033`) | UNVERIFIED |
| `live_topic` | ? | UNVERIFIED |
| avg watch time | ? | UNVERIFIED |

## Compass ratio columns (landing cross-checks only)

Not stored as truth; recomputed from counts and compared at landing (LAND-1).

| Compass column | Expected to equal (UNVERIFIED) |
|---|---|
| 曝光-观看率(人数) | `entered_uv ÷ exposed_uv` (stage ①) |
| 观看成交率(人数) | `paid_buyers_uv ÷ entered_uv` (CVR) |
| 商品点击成交率(人数) | `paid_buyers_uv ÷ product_clicked_uv` (stage ④) |

Rounding and the tolerance for a mismatch: TBD.

## Derived values (not columns)

- **Kept buyers** for stage ⑤ (spec: Kept buyers ÷ Paid buyers, `03-product-spec-v0.4.md:235`): the room export (as reported) has no kept-buyers column. A candidate is `paid_buyers_uv − number_of_refunding_users` — **UNVERIFIED and not decided**; depends on the 退款人数 attribution question in the queue.
- **Refund fraction** = `number_of_refunding_users ÷ paid_buyers_uv` (quarantine rule 8). The spec's refund *rate* is refunded orders ÷ paid orders (`03-product-spec-v0.4.md:259`); the room export (as reported) has no refunded-orders column. UNVERIFIED.

## Open

- Read a real header row and replace every UNVERIFIED with the file name and column position.
- Product export (live room × product): later, not modelled ([decision 0002](../decisions/0002-v1-landing-room-export-only.md)).
