# Quarantine rules (landing)

- **Status: PROPOSED.** Adoption is an open item for Rey ([../decision-queue.md](../decision-queue.md)). Only Rey sets these to ACCEPTED.
- **Applies to:** each room-export row at landing (LAND-1), after column mapping ([room-export.md](room-export.md); column names UNVERIFIED).
- **Effect:** a row that breaks any rule is landed as a **quarantined** session record with every broken rule ID as its reason. It is excluded from all aggregates, benchmarks, tiers and recoverable revenue, and listed with an "Excluded" tag and the reason (spec `upstream/design-pack/03-product-spec-v0.4.md:939`). It is never deleted or silently corrected.

| ID | Rule (quarantine if …) | Why |
|---|---|---|
| Q-1 | any count is negative (`exposed_uv`, `entered_uv`, `product_exposed_uv`, `product_clicked_uv`, `paid_buyers_uv`, `paid_orders`, `number_of_refunding_users`) | Counts cannot be negative |
| Q-2 | `entered_uv > exposed_uv` | Stage ① rate > 100% |
| Q-3 | `product_exposed_uv > entered_uv` | Stage ② rate > 100% |
| Q-4 | `product_clicked_uv > product_exposed_uv` | Stage ③ rate > 100% |
| Q-5 | `paid_buyers_uv > product_clicked_uv` | Stage ④ rate > 100% |
| Q-6 | `paid_orders > 0` **and** `paid_buyers_uv > paid_orders` | Each buyer has at least one order |
| Q-7 | `number_of_refunding_users > paid_buyers_uv` | Cannot refund more buyers than paid |
| Q-8 | refund fraction (`number_of_refunding_users ÷ paid_buyers_uv`) outside [0, 1] | Stage ⑤ input must be a fraction |

## Notes (not rules)

- Q-8 overlaps Q-1 and Q-7; it is kept as listed. When `paid_buyers_uv = 0` the fraction is undefined: whether that is "outside [0, 1]" is **open** (UNVERIFIED; proposed: not a breach, since stage ⑤ is not graded below 3 paid buyers, `03-product-spec-v0.4.md:274`).
- Null / blank / non-numeric cells: handling TBD (not one of the 8 rules).
- Compass ratio-column mismatches are cross-check findings, not quarantine rules, unless Rey decides otherwise.
- Live sessions are excluded from benchmarks as a separate status (spec `03-product-spec-v0.4.md:938`), not by quarantine.
