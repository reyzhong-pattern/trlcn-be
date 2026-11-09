# Decision queue

Open items, each with an owner. These are cleared **during building**, not before. When one is settled, Rey records it as a decision in [decisions/](decisions/) (agents may draft it as PROPOSED) and it is removed here.

| # | Open item | Why it matters | Owner | Status |
|---|---|---|---|---|
| DQ-1 | **Tiers stored by a daily job, or computed at read time?** Spec 5.2 says benchmarks "follow the filters", "recalculated whenever the filters change" (`upstream/design-pack/03-product-spec-v0.4.md:270`) and 5.3 rule 5 says "recalculated live" (`:294`); spec 13 says a daily job computes benchmarks per group (`:953`); decision 0004 says the window is recalculated daily. | Shapes the Score layer (tables vs functions) and every Serve endpoint. | Rey | Open |
| DQ-2 | **Adopt the quarantine rules** ([data-model/quarantine-rules.md](data-model/quarantine-rules.md), Q-1…Q-8, PROPOSED), including the zero-paid-buyers case for Q-8. | LAND-1 cannot be accepted without them. | Rey | Open |
| DQ-3 | **Is the room export's 退款人数 attributed by refund time or by order time?** | Decides how stage ⑤ (kept buyers) and refund fraction are derived and whether they change after landing (spec R36 provisional retention, `:1012`). | Rey | Open |
| DQ-4 | **Expected-recovery-at-P50/P75 formula on Action Cards** (spec `:523`). Take it from the mockup's behaviour (version 1794210096-60c6), per decision 0004. | Needed for AC-1 and golden tests. | Claude Code drafts; Rey approves | Open |
| DQ-5 | **Approved source for new data** (beyond the room exports handed over by Fetch). | No new data source is used until approved. | Rey + data owner | Open |
| DQ-6 | **Okta details** (tenant, OIDC app, SCIM endpoint, group → brand mapping per spec Q10, `:1044`). | AUTH-1 phase 2. | FE + BE engineer | Open |
| DQ-7 | **Accept or reject decision 0002** (v1 lands the room export only). | LAND-1 scope. | Rey | Open (PROPOSED) |
