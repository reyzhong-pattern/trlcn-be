# TrendVision Live — Performance Analytics: Product Spec

**Version:** v0.4 (for development) · **Date:** 2026-11-04 · **Owner:** Mio Jia
**Scope:** Session Analytics, Live Host Analysis and Settings (Admin), rebuilt as one brand-scoped product on the APAC Design System. Risk Radar and Live Playbook Builder are Day 2 (separate sidebar modules).
**Inputs:** the audit of the current staging app ([audit doc](https://claude.ai/artifact/Eii9kJVhU1pT6UocJ7M5gL)), product decisions of 2026-10-27 to 2026-10-29 (including the round 1 prototype review), and the APAC Design System skill (v1.3, synced 2026-10-28).
**Demo data:** `demo-data/` (synthetic, 4 platforms, 3 brands; see Appendix A).

---

## 1. Summary

Brand operators need one place to answer three questions about their livestreams:

1. **How are my lives performing?** (Session Analytics: Overview, Live Funnel)
2. **What should I fix in a specific session?** (Session detail with Action Cards)
3. **Which hosts are worth investing in?** (Host Analysis with auto-tags)

Design principles:

- **One benchmark group per comparison:** Brand × Platform × Type, rolling 90 days, set by the current filters (Type = All → All types).
- **Every grade explains itself.** Any tier, P50, gap bar or median line opens the Benchmark drawer, which shows the group, the window, the sample and the result.
- **Explanations live in Tooltips, not on the page.** Grading rules, thresholds and "why" texts sit in the Tooltip of the element they explain; the page keeps the value and the action. Every chart element and every truncated cell has a tooltip (10.5).
- **Funnels always show step rates in %** (4.3).
- **Filters apply visibly,** or are disabled with a reason.
- **Action Cards are per session only.** They open from a session row.
- **Sessions are found in a searchable table,** not a dropdown.
- **One funnel vocabulary** everywhere (4.3).
- **Built on the APAC Design System:** components and layout rules are used as specified, and the few extensions needed are listed in 10.6.

### Goals

- A new operator can read the Overview without a glossary.
- Any grade can be traced to its benchmark in one click.
- Every session and every host is reachable in two clicks or fewer from the module landing page.

### Non-goals (v1)

- Risk Radar, Live Playbook Builder (Day 2 modules).
- Cost, fee and ROI calculations (they need cost data; see 14).
- Multi-brand group views and cross-brand benchmarks.
- An "All platforms" view: Platform is single-select everywhere, including the Overview sales figures and GMV trend.

---

## 2. Users, roles and key scenarios

### 2.1 Roles and access

| Role | Who | Can do |
|---|---|---|
| **Operator** (base role, every user) | Brand operators | Use Session Analytics and Host Analysis for the brands assigned to them |
| **Admin** (Operator + admin rights) | Product owners, team leads | Everything an Operator can, for all brands, plus **Settings**: manage users, roles and brand access; view data connections |

- Access is granted **per brand**. A user only sees the brands assigned to them in the brand switcher.
- A user with no brand assigned sees an empty state: "You don't have access to any brand yet. Ask an admin." The Admin contact is shown.
- A link to a brand the user cannot access opens a "No access to KELO-COTE" page with a "Request access" action (P1), never the data.
- Sign-in: Okta SSO (phase 2). Until then, an admin-managed allowlist (section 9).

### 2.2 Key scenarios

| # | Scenario | Where it is served |
|---|---|---|
| S1 | "How did our Douyin lives do this month?" Live performance and sales KPIs at a glance | Overview → KPI rows |
| S2 | "Are we getting better?" Funnel by stage vs the previous period; GMV over the last 7 periods; MoM and YoY | Overview → Trends |
| S3 | "Do self-operated rooms or influencers work better for us?" | Overview → Channel type comparison (only when Type = All) |
| S4 | "Where do viewers drop off across these hosts?" | Live Funnel (side nav › Session Analytics; aggregated over all active filters) |
| S5 | "Last night's live with host X underperformed. What do we change?" | Sessions (side nav › Session Analytics) → session row → Session drawer → Action Cards |
| S6 | "Which hosts deliver, and which deserve more budget?" | Host Analysis → leaderboard, quadrant tags, Host drawer |
| S7 | "Why is this WEAK? Compared with what?" | Any tier or benchmark reference → Benchmark drawer |
| S8 | "Give the new hire access to Thorne only." | Settings → Users & access (Admin) |

---

## 3. Information architecture

### 3.1 Context hierarchy

```
Brand (workspace, chosen in the sidebar header)
 └─ Module (sidebar): Session Analytics | Host Analysis | Settings (Admin) | (Day 2: Risk Radar, Playbook Builder)
     └─ View (sidebar sub-items, Session Analytics only): Overview (the module item itself, default landing) | Live Funnel | Sessions
         (Host Analysis and each Settings section: single page)
         └─ Pinned page header: view title + description, time range (right), filter bar (Platform > Type > Hosts), scope line
             └─ Detail drawers: Session detail | Host detail (wide) → Benchmark drawer (standard, stacks on top)
```

- **Brand is not a filter.** It is the workspace, chosen from a switcher in the sidebar header (under the logo) and remembered per user. Changing the brand resets the filters to their defaults. The switcher lists only the brands the user can access.
- **The filter state** (Platform, Type, Hosts, Time range, Granularity) persists across views and across both analytics modules within the same brand.
- **Details open in drawers.** Drawers are modal (10.5). The list stays behind, so closing a drawer returns the user to the same scroll position, sort and filters.

### 3.2 Site map

```
/[brand]/sessions/overview             Session Analytics · Overview (sidebar item Session Analytics; default landing)
/[brand]/sessions/funnel               Session Analytics · Live Funnel (sidebar sub-item)
/[brand]/sessions/list                 Session Analytics · Sessions (sidebar sub-item)
    ?session=[id]                      Wide drawer: Session detail (Summary | Action Cards)
/[brand]/hosts                         Host Analysis
    ?host=[id]                         Wide drawer: Host detail (Summary | Funnel | Sessions)
    ?host=[id]&session=[id]            Drawer stack: Host → Session
    ?compare=[id],[id](,[id],[id])     Wide drawer: Host comparison (2–4 hosts)
any page  &bench=[group]:[metric]      Benchmark drawer (stacks on top of any page or drawer)
/settings/users                        Settings · Users & access (Admin)
/settings/connections                  Settings · Data connections (Admin, read-only v1)
/settings/benchmarks                   Settings · Benchmark rules (Admin, read-only v1)
/settings/audit-log                    Settings · Audit log (P1)
/[brand]/risk-radar, /[brand]/playbook Day 2
```

All filter and drawer state is in the URL (`platform`, `type`, `hosts`, `from`, `to`, `gran`, `q`, `session`, `host`, `compare`, `bench`), so a shared link opens exactly the same view. A link is only opened for recipients who can access that brand.

### 3.3 Navigation between views

```
Sidebar ──Session Analytics / Live Funnel / Sessions──▶ that view (same filters, top of the page), from any scroll position
Overview ──"View sessions"──▶ Sessions (same filters)
Overview ──top-session row──▶ Session drawer
Overview ──stage in funnel chart──▶ Live Funnel (stage highlighted)
Sessions ──row──▶ Session drawer ──tab──▶ Action Cards
Host Analysis ──row / map dot──▶ Host drawer ──session row──▶ Session drawer (stacked, back link)
Host drawer ──"Open in Session Analytics"──▶ Overview filtered to that host
Host Analysis › Leaderboard ──"Compare hosts"──▶ selection mode ──"Compare (n)"──▶ Host comparison drawer
Host drawer ──"Compare with…"──▶ selection mode with this host pre-selected
Any tier · P50 · gap bar · median line · scope chip ──▶ Benchmark drawer
```

### 3.4 Page shell (APAC Page Shell)

```
┌────────────┬──────────────────────────────────────────────────────────────────────────┐
│ [Pattern]  │ Session Analytics / Live Funnel                    [中文 | EN]  🔍   (MJ) │ top bar 48px (pinned)
│ Brand      ├──────────────────────────────────────────────────────────────────────────┤
│ [Thorne ▾] │ Live Funnel                                              [Last 30 days ▾]│ ┐
│            │ Where viewers drop off, stage by stage, across every session in scope     │ │ pinned page
│ ANALYTICS  │ Platform [Douyin ▾]  Type [All|Self-operated|Influencer]  Hosts [All ▾]   │ │ header block
│ ▣ Session  │ Benchmark: Thorne × Douyin × Influencer · 90d · n=91 ⓘ  Data as of 08:00 │ ┘
│   Analytics│──────────────────────────────────────────────────────────────────────────│
│  │ Live    │ … content (max-width 1440px, H-pad 40/32/24/16px) …                      │
│  │ Funnel ◀│                                                                          │
│  │ Sessions│                                                                          │
│ ◫ Host     │                                                                          │
│   Analysis │                                                                          │
│ ADMIN      │                                                                          │
│ ⚙ Settings │                                                                          │
│ (Ask AI)   │                                                                          │
└────────────┴──────────────────────────────────────────────────────────────────────────┘
  280px sidebar, full height and pinned (64px icon-only at md–lg; off-canvas below md)

After scrolling, the header block condenses to one pinned 52px row under the top bar:
│ Live Funnel   [D Douyin ▾]  [All|Self-operated|Influencer]  [All hosts (14) ▾]   [Last 30 days ▾] │
```

- **Sidebar** (APAC `Sidebar`, `collapsible="icon"`): the full Pattern logo (`Logo_full.svg`, product name under it; `Logomark_blue.svg` when collapsed), then the **brand switcher** (Select in the `SidebarHeader`; collapsed state shows a brand initial avatar with a Tooltip). Groups: **Analytics** (Session Analytics, Host Analysis), **Admin** (Settings; only rendered for Admins). Day 2 items are added to Analytics when they ship.
  - **Session Analytics views in the sidebar:** the Session Analytics item is the Overview page and the default landing. Its views **Live Funnel** and **Sessions** are sub-items indented under it (36px rows, a thin guide line, always visible). The open view has the active fill; while a sub-item is open, the parent reads bold with no fill. In the 64px icon rail the sub-items move into a flyout menu (Overview · Live Funnel · Sessions) that opens on hover or focus, and the parent icon shows the active fill when any of its views is open.
  - The sidebar is **pinned**: it stays in place while the page scrolls, so views can be switched from any scroll position. Switching a view keeps the filters and opens the new view at the top.
- **Top bar** (48px): pinned; breadcrumb on the left, following the APAC rule "sidebar section → page → sub-page": `Session Analytics` (Overview landing), `Session Analytics / Live Funnel`, `Session Analytics / Sessions`, `Host Analysis`, `Settings / Users & access`. On the right: the **language toggle** (中文 | EN, see 3.5), global search (⌘K, optional) and the user avatar menu (profile, theme, sign out).
- **Page header (one per view):** a `heading-md` title and a one-line description in `body-sm` `text-tertiary` on the left, and, following the APAC Dashboard template, the **time range DatePicker on the right**. Titles: Session Analytics (Overview), Live Funnel, Sessions, Host Analysis; descriptions e.g. "How your lives perform against their benchmark" / "Where viewers drop off, stage by stage, across every session in scope" / "Every session in scope. Open one to see what to fix before the next live" / "Which hosts are worth investing in: reach, basket and funnel". The time range is part of the same filter state as the filter bar. The granularity control is not in the page header: it sits inside each trend chart card it controls, and is not shown on views without trend charts.
- **Pinned header block:** the page header, filter bar and scope line form one block pinned under the top bar. At the top of the page it shows in full. Once the page scrolls (more than 28px) it condenses to one 52px row: the title (16px), the filter controls without their labels (32px high) and the time range; the description and scope line are hidden and come back when the page returns to the top (less than 8px). The block keeps its height in the page flow, so the content never jumps, and the filter popovers open from the condensed row. Settings has no analytics filters and keeps a plain page header.
- **Filter bar:** follows the APAC List-page filter bar (a horizontal row, `outline-default` bottom border, 16px vertical padding), inside the pinned header block with the scope line under it.
- **No view tabs:** Session Analytics views are sidebar sub-items, not tabs. APAC `Tabs` (`line` variant) are used only inside drawers (Session drawer, Host drawer).
- **Ask AI** (existing feature, kept): floating entry above the pinned header and below every overlay (10.4), dismissed automatically when a drawer or modal opens (APAC z-index rule). Its behaviour is out of scope for this spec.

### 3.5 Language: Chinese and English (foundation)

The whole product is bilingual from v1: **简体中文 (zh-CN)** and **English (en)**. This is a foundation requirement, not a later translation pass. No screen ships in one language only.

| Topic | Rule |
|---|---|
| Toggle | A segmented control **中文 \| EN** in the top bar, left of search. It switches instantly, with no reload, and keeps the current page, filters and open drawers |
| Default | The user's saved preference; on first sign-in, the browser locale (zh-* → 中文, otherwise EN). Okta profile locale in phase 2 |
| Persistence | Saved per user (profile setting). A shared link opens in the *recipient's* language; the URL carries no language |
| What translates | All UI text: navigation, labels, metric names, tooltips, tier and tag names, Benchmark drawer explanations, Action Card copy, generated insight sentences, empty and error states, toasts, invitation emails, exported column headers |
| What doesn't | Data from platforms: host names, live topics, product names. They are shown as they are in both languages, with no machine translation |
| Terminology | One fixed term per concept in each language (Appendix B). Metric names never vary between screens |
| Numbers | zh: 万 / 亿 for large values (124.4万, 1.24亿); en: K / M (1.24M). Same decimals in both. Percentages and ¥ unchanged |
| Dates and times | zh: 10月26日 21:00, 2026年10月; en: 26 Oct 21:00, Oct 2026. Week starts Monday in both. China Standard Time |
| Generated text | Insight sentences and Action Cards come from per-language templates with variables, never by translating English output. Ask AI answers in the UI language |
| Layout | Design for the longer English strings. Chinese uses Noto Sans SC with the ~4px taller CJK line height (APAC rule). Labels wrap rather than truncate; table headers may wrap to two lines |
| Components | Use the localisation props the design system provides: `Pagination labels`, `DataMetric comparisonLabel` / `tooltipAriaLabel`, `Dialog` / `Drawer accessibleTitle`, DatePicker locale |
| Engineering | All strings in i18n resource files (ICU message format, with plural and number formatting). No hard-coded UI strings; missing keys fail the build |
| Quality | Chinese terms are reviewed by operators before release (Q15). Every prototype round includes at least one 中文 artboard |

---

## 4. Global filter model

### 4.1 Filter group

| Order | Control | Location | Selection | Component | Default | Notes |
|---|---|---|---|---|---|---|
| 0 | **Brand** | Sidebar header | Single | `Select` | Last used | The workspace, not a filter. Lists only brands the user can access. Changing it resets the controls below. |
| 1 | **Platform** | Filter bar | Single, required | `Select` (items with platform icon) | First connected platform | Douyin, RED, Tmall, JD. Platforms not connected for this brand are listed disabled, with the description "Not connected". |
| 2 | **Type** | Filter bar | All or one | Segmented control (`Tabs`, default filled-pill variant, `sm`) | All | All, Self-operated, Influencer. With Brand and Platform, it defines the benchmark group. |
| 3 | **Hosts** | Filter bar | Multi-select with search | Multi-select combobox (extension, 10.6), grouped under "Self-operated" and "Influencer" | All hosts | The trigger shows a count ("All hosts (14)", "3 selected"). Each option shows type and sessions in range. Options and count follow the chosen Platform and Type (e.g. "All hosts (12)" with Type = Influencer). When a Type change drops selections, a toast names them. |
| 4 | **Time range** | Page header, right | Preset or custom | `Select` presets + `DatePicker` (`isRange`) for Custom | Last 30 days | Presets: Last 7 days, Last 30 days, Last 90 days (matches the benchmark window), This month, Last month, This quarter, Custom. |
| 5 | **Granularity** | Inside each trend chart card (Overview: GMV trend) | Single | Segmented control (`Tabs`, `sm`) | Auto: Day if ≤ 31 days, Week if ≤ 6 months, else Month | Sets the time gate used by trend charts (6.1). |
| 6 | **Search** | In the table toolbar (Sessions, Host Analysis) | Free text | `Input type="search"` | Empty | Sessions: date, host name, live topic. Hosts: host name. |

**Scope line** under the filter bar, always visible:

- Type = one → `Benchmark: Thorne × Douyin × Influencer · rolling 90d · n=91 sessions ⓘ`
- Type = All → `Benchmarks: All types (n=137) · Self-operated (n=46) · Influencer (n=91) ⓘ`

Each benchmark name in the scope line is a link that opens the Benchmark drawer for that group (5.4). The line ends with `Data as of 28 Oct 08:00`.

### 4.2 Filter applicability by view

✓ = applies · — = not applicable

| View | Platform | Type | Hosts | Time range | Granularity | Search |
|---|---|---|---|---|---|---|
| Overview | ✓ | ✓ | ✓ | ✓ | ✓ (trend charts) | — |
| Live Funnel | ✓ | ✓ | ✓ | ✓ | — | — |
| Sessions | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| Host Analysis | ✓ | ✓ (sets the grading group) | ✓ (limits rows) | ✓ | — | ✓ |
| Session drawer | Fixed to the session | Sets the grading group (5.3) | Fixed | Fixed | — | — |
| Host drawer | Inherits | Sets the grading group (5.3) | Fixed to host | ✓ (changeable in drawer) | ✓ (trend card) | — |
| Settings | — (filter bar hidden) | — | — | — | — | Users table only |

- A control that does not apply is shown disabled (APAC disabled style: 50% opacity). Disabled elements have `pointer-events: none`, so the reason Tooltip sits on a wrapper element. Granularity is never shown disabled: it appears only inside trend chart cards.
- A drawer always states its own scope in its header, because it can differ from the filter bar.

### 4.3 One funnel vocabulary

Use these names, numbers and order everywhere: charts, tables, Action Cards, tooltips, the Benchmark drawer, exports.

**Funnel display rule:** any funnel shown as rates uses these five step rates, each in % of the stage before it, in this order. Do not re-base stages on a common denominator (e.g. "per 1,000 entrants" or "% of exposed") in comparisons or tables; the only exception is the funnel volume chart, which shows UV counts and "% of exposed" as a volume view, not as rates to compare. This applies to every funnel presentation: comparison panels, Live Funnel, Session drawer, Host drawer, exports and any later funnel view, so the value shown is always the value its tier grades. Overall conversion is shown as CVR.

| Stage | From → To | Rate name | Formula |
|---|---|---|---|
| ① | Exposed → Entered room | **Entry rate** (shown as "Exposed rate" on the Overview KPI, see Q2) | Entered UV ÷ Exposed UV |
| ② | Entered room → Saw a product | **Product exposure rate** | Product-exposed UV ÷ Entered UV |
| ③ | Saw a product → Clicked a product | **Product click rate** | Product-click UV ÷ Product-exposed UV |
| ④ | Clicked → Paid | **Click-to-pay rate** | Paid buyers ÷ Product-click UV |
| ⑤ | Paid → Kept (no refund) | **Retention rate** | Kept buyers ÷ Paid buyers |

**Host** = any account that runs lives: a **self-operated** brand room or an **influencer** (KOL). The UI says "host" everywhere (filters, tables, drawers, comparison); "account" and "KOL" appear only in data and integration docs.

All counts are unique visitors (UV) per session. The word "exposure" alone is never used: it is "live exposure" (input to stage ①) or "product exposure" (stage ②). Each platform maps its native events to these five stages (13 and Q8).

---

## 5. Metrics, benchmarks and tiers

### 5.1 Metric dictionary

| Metric | Formula | Unit | Notes |
|---|---|---|---|
| Sessions analyzed | Count of completed, valid sessions in scope | count | Quarantined and live sessions are excluded and counted in a footnote. |
| Exposed UV | Σ live exposure UV | UV | Top of funnel. |
| Exposed rate (= Entry rate) | Σ Entered ÷ Σ Exposed | % | Stage ①. |
| Product exposure rate | Σ Product-exposed ÷ Σ Entered | % | Stage ②. |
| CVR (overall) | Σ Paid buyers ÷ Σ Entered UV | % | Pooled across sessions, not averaged. Matches the current app (16 ÷ 739 = 2.17%). |
| Session tier distribution | Count of sessions per tier | count | 5.3. |
| Total GMV | Σ GMV of paid orders through lives | ¥ | Before refunds. |
| Avg GMV / session | Total GMV ÷ Sessions analyzed | ¥ | |
| Paid orders | Σ paid orders through lives | count | |
| Avg AOV | Total GMV ÷ Paid orders | ¥ | Pooled. |
| Refund rate | Refunded orders ÷ Paid orders | % | Session drawer and Live Funnel. |
| Avg watch time | Σ watch seconds ÷ Σ Entered UV | s | Display only, not graded. |
| Recoverable revenue | Σ per session: Entered × max(0, P75 CVR − CVR) × GMV per buyer | ¥ | The upside if every session reached the top-quartile CVR of the group the filters define (All types when Type = All). For sessions with no buyers, GMV per buyer falls back to the group's median. Annualised value (hover) uses the annual GMV from the platform MCP. Demo (Thorne × Douyin, last 30 days, Type = All): +¥2.88M against ¥578.9K GMV; session S00234: +¥558.0K. |
| UV lost (stage) | UV into stage − UV out of stage | UV | |
| Weakest stage | The stage with the lowest tier; ties go to the stage with more UV lost | ①–⑤ | |

**Currency:** CNY everywhere in v1. A USD toggle with FX rate and date stated is P2.

### 5.2 Benchmarks (rolling)

- **Group:** Brand × Platform × Type, e.g. Thorne × Douyin × Influencer. With Type = All, the group is Brand × Platform × All types (all valid sessions of both types).
- **Follows the filters:** every value is graded against the group the current filters define, recalculated whenever the filters change. This covers KPI P50 footnotes, the tier distribution, session tiers, stage tiers, weakest stage and recoverable revenue, in the Session drawer and the Benchmark drawer too.
- **Population:** valid, completed sessions of that group in a rolling window. Default: trailing 90 days (Q4). Recalculated daily as data arrives through the MCP and APIs.
- **Statistics:** P25, P50 and P75 of session-level values for each stage rate, CVR, AOV and exposure per session.
- **Minimum sample:** 20 sessions per group (Q4). Below that the group is **Building**: "Benchmark building (n=14 of 20)". No tiers or tags are assigned; raw values are still shown. The demo data includes three Building groups (Appendix A).
- **Stage minimums:** a stage's percentiles only use sessions with enough input (≥ 30 UV into stages ①–④; ≥ 3 paid buyers for stage ⑤).
- **As of:** every benchmark is stored with its window dates, so any grade can be traced to the window it used.
- **No pooled All types group:** where the All types group cannot be built (no session-level values), Type = All grades each session, host and Live Funnel sub-row against its own type group. Combined KPIs, the combined Live Funnel row and recoverable-revenue maths use the own-type groups; combined values are not tiered, and P50 footnotes are replaced by "Combined value · each session is graded against its own type".

### 5.3 Tiers (quartiles of the rolling benchmark)

| Tier | Position in benchmark group | Table and badge component | Chart colour |
|---|---|---|---|
| **STAR** | Top 25% (≥ P75) | `Tag variant="positive"` | Chart 6 Green |
| **GOOD** | 25–50% (P50 to P75) | `Tag variant="informative"` | Chart 1 Blue |
| **MID** | 50–75% (P25 to P50) | `Tag variant="warning"` | Chart 3 Amber |
| **WEAK** | Bottom 25% (< P25) | `Tag variant="negative"` | Chart 4 Pink |
| Not enough data / Building | Below minimums | `Tag variant="neutral"` | Chart 9 Slate |

Rules:

1. **Stage tier:** a session's stage rate against the group's P25/P50/P75 for that stage.
2. **Session tier (confirm in Q5):** the quartile of the session's **CVR** (paid buyers ÷ entered) within its group. The alternative considered is a harmonic composite of the five stage percentiles. The demo data shows why the composite confuses users: the two rules agree on only 40% of sessions. 90 sessions rank STAR on the composite without a single STAR stage, and 22 rank STAR on the composite while their CVR is WEAK. CVR is the outcome, it is one number the Benchmark drawer can explain, and stage tiers already carry the diagnosis. The demo data provides both columns (`session_tier_cvr`, `session_tier`) so the prototype can test both.
3. **Aggregate tier** (KPI cards, Live Funnel, host rows): the pooled rate of the selection against the session-level P25/P50/P75 of the group the filters define. With Type = All this is the Brand × Platform × All types group; per-type rows are graded against their own type.
4. **Small samples:** no tier below the stage minimums. Show "Not enough data", never a WEAK badge.
5. **Benchmarks follow the filters:** every value is graded against the group the current filters define, recalculated live. A session is graded against the filtered group's current rolling window, not the window that ended the day before it, so a session can show a different tier under Type = All than under its own Type; every view names the group it used. If empirical-Bayes smoothing is kept (Q6), it is applied inside the calculation everywhere, and the Benchmark drawer shows the raw rate, the smoothed rate and a one-line explanation.

### 5.4 Benchmark drawer (grading rubric, everywhere)

Wherever the product shows a grade or a benchmark, the reference is clickable and opens the **Benchmark drawer**. It shows which sessions the value was compared with, how the benchmark was calculated, and where the value sits.

**Triggers** (all open the same drawer, pre-focused on the clicked metric):

| Where | Clickable element |
|---|---|
| Scope line (all analytics pages) | Benchmark group name |
| Overview | Tier distribution bar; P50 footnotes on KPI cards; channel comparison column headers |
| Live Funnel, Session drawer Summary, Host drawer Funnel | Stage performance gap bar (P25·P50·P75 in its tooltip); tier Tag |
| Sessions table | Session tier Tag; stage tier cells |
| Action Cards | P50 / P75 values; stage tier Tag; "Expected recovery" figure |
| Host Analysis | Funnel cell tier colours; quadrant Tag; median lines on the map |
| Host drawer | KPIs vs P50; tag |

Interaction rules:

- Click opens it (no hover open). Hovering the element first shows a Tooltip, "Compared with Thorne × Douyin × Influencer · click for details".
- 480px drawer (APAC Drawer Detail Panel width), modal with its own overlay (10.5), `heading-sm` title. It stacks on top of a wide drawer, adding its own overlay. Closing it returns to the drawer or page underneath. Deep link: `&bench=thorne-douyin-influencer:product_click_rate`.
- It is read-only and has no link to Settings: benchmark rules are Admin-only and live in Settings › Benchmark rules.

**Content:**

```
┌ Benchmark · Product click rate                                            ✕ ┐
│ Thorne × Douyin × Influencer                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ YOUR VALUE                                                                  │
│ 10.19%  →  GOOD (P50–P75)   ·   55th percentile of 91 sessions              │
│ ├────────░░░░░░░░░░░░░●░░░░░░░░────────────┤                                │
│ 0%     P25 7.92%   P50 10.06%  P75 11.98%   max                             │
│ [histogram of the 91 session values, value marked]                          │
├─ Calculation group ─────────────────────────────────────────────────────────┤
│ Brand: Thorne · Platform: Douyin · Type: Influencer                         │
│ Window: rolling 90 days, 30 Jul – 27 Oct 2026 (recalculated daily)          │
│ Sessions: 91 included · 0 excluded (quarantined, live) · 11 hosts        │
│ Stage minimum: ≥ 30 UV into stage                                           │
├─ How it is calculated ──────────────────────────────────────────────────────┤
│ Product click rate = Product-click UV ÷ Product-exposed UV, per session.    │
│ P25 / P50 / P75 = 25th, 50th, 75th percentile of the 91 session values.     │
│ STAR ≥ P75 · GOOD P50–P75 · MID P25–P50 · WEAK < P25                        │
├─ All results for this group ────────────────────────────────────────────────┤
│ Metric               P25      P50      P75                                  │
│ ① Entry rate          8.28%   13.00%   20.57%                               │
│ ② Product exposure   21.15%   26.34%   31.18%                               │
│ ③ Product click       7.92%   10.06%   11.98%   ◀ focused                   │
│ ④ Click-to-pay        3.42%    5.99%    8.88%                               │
│ ⑤ Retention          75.96%   83.36%   89.11%                               │
│ CVR                   0.05%    0.15%    0.24%                               │
│ AOV                  ¥229     ¥275     ¥351                                 │
│ Exposure / session   10.3K    23.9K    45.0K                                │
├─ Trend (P1) ────────────────────────────────────────────────────────────────┤
│ P50 of this metric over the last 6 recalculations (line)                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

(Values are from the demo dataset, `benchmarks.csv`.)

- **Your value** section: only when opened from a specific value (a session, a host, an aggregate). Opened from the scope line, the drawer starts at "Calculation group".
- **Building group:** the drawer shows "Benchmark building: 14 of 20 sessions needed. Tiers appear once the group reaches 20 sessions in the window," plus the values collected so far, untiered.
- **Type = All:** opened from a combined value, the drawer shows the Brand × Platform × All types group.
- **No status Tag** for a ready group; only a Building group shows a status banner.
- **Opened from a session:** "Your value", the histogram and the results table use the filtered group's current rolling window, so no window note is needed. With Type = All that is the All types group.

---

## 6. Module A: Session Analytics

Three views, opened from the sidebar: **Overview** (the Session Analytics item itself and the default landing: what happened), **Live Funnel** (a sub-item: where viewers drop off, aggregated) and **Sessions** (a sub-item: find one session and fix it). Each view has its own page header (3.4). Action Cards live inside the Session drawer.

Numbers, names and topics in wireframes are illustrative or from the demo data.

### 6.1 Time gates (used by trends)

- **Time gate** = one bucket at the chosen granularity (a day, a week or a month).
- **Current period** = the selected time range. **Previous period** = the range of equal length immediately before it.
- **MoM** = the same range shifted back one calendar month. **YoY** = the same range shifted back one year. (The demo data starts 1 Sep 2025, so YoY works for ranges from Sep 2026.)
- Every KPI card shows its change versus the previous period.

### 6.2 View: Overview (APAC Dashboard template)

```
┌ Live performance ───────────────────────────────────────────────── heading-sm + divider ┐
│ [Sessions analyzed] [CVR]           [Exposed rate]       [Product exposure rate]        │ 4× DataMetric
│  136  +12 vs prev   0.33% +0.04pp    10.7% −0.4pp        31.4% +1.2pp                   │ (compare)
│ [Session tiers ████ STAR 34 │███ GOOD 33 │███ MID 35 │████ WEAK 34   ·  of 136 sessions] │ full-width card
├ Sales ──────────────────────────────────────────────────────────────────────────────────┤
│ [Total GMV]        [Avg GMV/session]  [Paid orders]     [Avg AOV]                        │ 4× DataMetric
│  ¥1.54M  +8%        ¥11.3K  −3%        2,004  +11%       ¥268  −2%                       │
│ [Recoverable revenue  +¥412K this period if every session reached P75 CVR · ⓘ method]   │ featured card
├ Trends ─────────────────────────────────────────────────────────────────────────────────┤
│ [Funnel by stage: current vs previous]          │ [GMV by time gate: last 7] [D|W|M]      │ 2× chart cards
│                                                  │  MoM +6% · YoY +21%                     │
├ Channel type comparison (only when Type = All) ─────────────────────────────────────────┤
├ Sessions [Latest | Top GMV | Most upside] ·························· View all sessions ┤
│ 5 rows (DataTable) → row or "View details" opens Session drawer                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Row 1: Live performance** (4× `DataMetric variant="compare"`, 24px padding, 4-column grid, 16px gap)

| Card | Value | `change` / `comparisonLabel` | `sentiment` | Click target |
|---|---|---|---|---|
| Sessions analyzed | count | "+12" / "vs previous 30 days" | neutral | Sessions view |
| CVR | Paid buyers ÷ Entered | pp change | positive if up | Live Funnel |
| Exposed rate | Stage ① | pp change | positive if up | Live Funnel, stage ① highlighted |
| Product exposure rate | Stage ② | pp change | positive if up | Live Funnel, stage ② highlighted |

The `tooltip` prop on each card holds the definition (read-only). Each rate card adds a footnote line with the P50 of the current group (All types when Type = All), e.g. "P50 13.0%", which opens the Benchmark drawer.

**Session tier distribution** (full-width card under row 1): a horizontal stacked bar (Recharts horizontal bar) of STAR/GOOD/MID/WEAK counts, in the chart colours from 5.3. Clicking a segment opens Sessions filtered to that tier. The card's "How tiers work" link opens the Benchmark drawer focused on CVR. With Type = All, one bar is shown, graded against the All types group (one bar per graded group). Segment labels use `text-on-primary`. The card has no subtitle line.

**Row 2: Sales** (4× `DataMetric variant="compare"`)

| Card | Value | Change | Sentiment |
|---|---|---|---|
| Total GMV | ¥ | % vs previous | positive if up |
| Avg GMV / session | ¥ | % vs previous | positive if up |
| Paid orders (through lives) | count | % vs previous | positive if up |
| Avg AOV | ¥ | % vs previous | positive if up |

**Recoverable revenue** (featured card under row 2): the value for the period, a one-line explanation, an ⓘ Popover with the method and the annualised value, and "See sessions with most upside" (opens Sessions sorted by recoverable revenue).

**Row 3: Trends** (2× chart cards, 16px padding, `label-lg` titles)

1. **Funnel by stage, current vs previous period.** Grouped bars per stage rate (①–⑤): current = Chart 1, previous = Chart 9 Slate; pp change labelled. Recharts crosshair tooltip shows both values and the change. Clicking a stage opens Live Funnel with it highlighted.
2. **GMV by time gate.** Bars for the last 7 gates at the chosen granularity (Chart 1), with a dashed line for the same gates a year earlier (Chart 9). The card header holds the Day | Week | Month control and shows MoM % and YoY % (YoY as a plain percentage, even on a tiny base). Hover shows GMV, sessions and paid orders. Clicking a bar sets the time range to that gate.

**Row 4: Channel type comparison** (only when Type = All and both types have sessions). Built with the shared **Comparison panel** (7.4) with two series, Self-operated (Chart 1) and Influencer (Chart 2).

- Two columns, Self-operated (Chart 1) and Influencer (Chart 2), each with session count and a link to its Benchmark drawer.
- Rows: the same five funnel rows as host comparison: the step rates ① to ⑤ in % (Thorne × Douyin, last 30 days, Self-operated vs Influencer: ① 6.89% vs 19.43%, ② 86.47% vs 27.45%, ③ 25.23% vs 11.25%, ④ 10.23% vs 7.16%, ⑤ 77.93% vs 82.63%, from `live_funnel`). Outcome tiles: CVR, AOV and Avg GMV per session, the two values side by side in columns, leader in bold.
- The channel comparison shows no tiers.
- One computed sentence names the largest difference (never hard-coded text).
- When Type ≠ All, the section is not rendered.

**Row 5: Sessions** (P1): a full section (`heading-sm` + divider) with the toggle **Latest | Top GMV | Most upside** and "View all sessions" in its header. 5 rows (APAC `DataTable`): date, host, type (Type = All), GMV, CVR, tier, and a trailing "View details" icon button. Clicking the row or the button opens the Session drawer.

### 6.3 View: Live Funnel (aggregated)

The aggregate of all sessions matching the filters. It describes and diagnoses; it gives no action instructions (those are per session).

```
┌ Scope: Douyin · Influencer · 3 hosts · 1–30 Oct · 41 sessions · Benchmark n=91 ⓘ ────────┐
├ Funnel volume (chart card) ─────────────────────────────────────────────────────────────┤
│ Stage                 UV passed                                 % of exposed  UV lost       │
│ Live exposure         ██████████████████████████████  2.03M     100%                      │
│ ① Entry rate          ████                            256K      12.6%        −1.77M       │
│ ② Product exposure    ██                              60K       2.9%         −196K ◀ weakest│
│ ③ Product click       ▌                               9,465     0.5%         −50K         │
│ ④ Click-to-pay        ▏                               960       0.05%        −8.5K        │
│ ⑤ Retention           ▏                               775                    −185         │
├ Summary strip: CVR · AOV · GMV · Refund rate · Avg watch ──────────────────────────────┤
├ Stage performance (Table) ──────────────────────────────────────────────────────────────┤
│ Stage | Rate | Below P50 ┊ P50 ┊ Above P50 (gap bar ⓘ) | Tier | UV lost | Next step       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

- **Funnel volume:** a Recharts horizontal bar chart (APAC has no funnel chart), Chart 1 for bars. Rows use the stage names of the stage table (① Entry rate … ⑤ Retention rate) after a "Live exposure" start row, with "UV passed", "% of exposed" and "UV lost" columns, and the weakest-stage marker.
- **Funnel section:** Funnel volume only.
- **Summary section:** the Summary strip (CVR, AOV, GMV, refund rate, avg watch time, each with its P50 where one exists), then **Stage performance**.
- **Stage performance** (one table, also used in Session drawer › Summary and Host drawer › Funnel). Columns: **Stage** · **Rate** · **Below P50 ┊ P50 ┊ Above P50**, a diverging bar of the rate's gap to its P50 relative to P50 (dashed P50 line, bar colour = tier, label = gap in %; one scale per table, capped at ±100% so an outlier does not flatten the other rows) · **Tier** Tag · **UV lost** · **Next step** (one short play keyed to the tier). Hovering a bar shows the chart tooltip with rate, P25, P50, P75, gap to P50 (% and pp) and tier; the bar and the Tag open the Benchmark drawer. The weakest stage (lowest tier, most UV lost) is highlighted with a Weakest tag. The Sessions view's Weakest stage filter finds the sessions weakest at a stage.
- **Type = All:** each stage row is followed by Self-operated and Influencer sub-rows, each with its own bar, tier, UV lost and next step against its own type group.

### 6.4 View: Sessions (APAC List page + DataTable)

The only way to pick a single session.

```
┌ 🔍 Search date, host, live topic        Tier [All ▾]  Weakest stage [All ▾]  Columns ▾┐
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Date·start   Host         Type   Live topic        Dur   Exposed  CVR   GMV    AOV   Tier  Weakest  Recov. │
│ 26 Oct 21:00 Thorne悦恩运动极限… Self   备孕营养课        2h41  29,969   2.10% ¥13.5K ¥293  GOOD  ⑤      +¥5.2K │
│ 25 Oct 19:30 首彬悦读            Infl.  睡眠营养夜话      1h34  26,639   0.13% ¥2.0K  ¥290  MID   ②      +¥1.6K │
│ …                                                                                        │
└──────────────────────────────────────── Pagination: 1–25 of 136 · page size 25 ‹ › ──────┘
```

| Column | Content | Sortable |
|---|---|---|
| Date · start time | Local date and start time (separates same-day sessions) | ✓ (default, newest first) |
| Host | Name (Noto Sans SC for CJK), type icon | ✓ |
| Type | Self-operated / Influencer | ✓ |
| Live topic | Session title from the platform | — (searchable) |
| Duration | h:mm | ✓ |
| Exposed UV | count | ✓ |
| Stage rates ①–⑤ | % with tier Tag (hidden by default; "Columns" menu as a Popover) | ✓ |
| CVR | % | ✓ |
| GMV | ¥ | ✓ |
| Paid orders | count | ✓ |
| AOV | ¥ | ✓ |
| Session tier | `Tag` (opens Benchmark drawer) | ✓ |
| Weakest stage | ①–⑤ | ✓ |
| Recoverable revenue | ¥ | ✓ |

- APAC `DataTable` with controlled `sort` (sorted server-side), `onRowClick`, `loading` skeleton rows, `emptyState` built from the `Empty` component, and DataTable `pagination` (sizes 10/25/50/100).
- Rows follow the shared table rule (10.5): the whole row opens the Session drawer, and each row ends with a "View details" icon button. Truncated host names and live topics show their full text in a Tooltip.
- Row height 48px; header `label-md`; sticky header (sticks under the pinned page header); numbers right-aligned; Host column pinned on horizontal scroll.
- **Search** matches date strings ("10-26", "Oct 26"), host names (Chinese, and pinyin if the platform provides it) and topic words.
- **Live sessions** appear at the top with a "Live now" `Tag variant="informative"`. They have no tier until the session ends and syncs.
- **Empty state:** "No sessions match: Douyin · Influencer · 3 hosts · 1–30 Oct", with "Clear search" and "Widen time range" buttons.

### 6.5 Session drawer (wide)

Opens from a session row. Deep link: `?session=[id]`. It uses the **wide drawer** extension (10.6), modal over the whole viewport (10.5). It opens on **Action Cards** by default, because the reason to open a session is to decide what to change. A KPI strip in the drawer header keeps the key numbers visible on every tab.

```
┌ Thorne悦恩运动极限海外店                                                                   ✕ ┐
│ 26 Oct 2026 21:00 · 2h41 · Self-operated · Douyin                               (meta line)   │
│ Benchmark: Thorne × Douyin × Self-operated · 90d · n=46 ⓘ    Session tier: GOOD ⓘ (scope row) │
│ ‹ Prev  Next ›                                                               (actions row)   │
│ GMV ¥13.5K · Orders 46 · AOV ¥293 · CVR 2.10% · Refund 30% · Recoverable +¥5.2K  (KPI strip)  │
├ Action Cards (default) │ Summary │ (Day 2: Risk Radar · Playbook) ─────────────── Tabs line ─┤
│ Action Cards: one card per stage, in funnel order ① → ⑤                                       │
│ Summary: funnel volume + Stage performance (same component as 6.3; next step = first action    │
│          of that stage's Action Card; the CVR row has none)                                  │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **Header:** the title and meta line on the left with only Close on the right; the scope row (benchmark group the filters define, session tier) under it; then the actions row (Prev / Next); then the KPI strip and the tabs.
- **Summary** holds Funnel volume and Stage performance only.

**Action Cards** (per session only)

- One card per stage, in funnel order ① → ⑤. Each card keeps its severity label: **Critical** (WEAK), **Action needed** (MID), **Watch** (GOOD), **Strong** (STAR).
- Card header: stage name, session rate, P50, P75 (both open the Benchmark drawer), gap to P50 in pp, UV lost (est. refunds for stage ⑤), tier Tag.
- Card body, three columns (stacked below md): **What happened** · **Before next session** (concrete actions) · **Expected recovery** (¥ and UV if the stage reached P50, then P75).
- Top banner: the session's recoverable revenue (CVR → P75).
- Stages with "Not enough data" show one neutral card explaining why, with no instructions.
- **"Copy actions for host briefing"** (P1, secondary button) copies every graded card's "Before next session" actions as plain text, ready to paste into a chat or briefing doc; its tooltip says what is copied.
  - Copied text: a heading line "Host briefing · {host} · {session ID} · {date time}", then "Before the next session:", then one numbered line per graded card, "{n}. {stage}: {actions}". Cards with "Not enough data" are left out. In 中文 the same lines use the 中文 labels.
  - Clicking it also opens a standard `Dialog` titled **"Copied for host briefing"**: a status line ("Copied to your clipboard. Paste it into the host brief, a chat or a doc."), the copied text exactly as it will paste (monospace, read-only, scrolls past 360px), a meta line ("5 actions · 825 characters · plain text" for S00234) and a single primary **Done** button. ✕, Esc and the scrim also close it. No toast is shown.
  - If the browser blocks the clipboard, the status line says so ("The browser blocked the clipboard here. Select the text below and copy it.") and the text stays selectable.

---

## 7. Module B: Host Analysis

Purpose: help operators judge the performance, and later the ROI, of each host (a self-operated room or an influencer), and compare hosts side by side. It uses the same filters as Session Analytics. Breadcrumb: `Host Analysis`.

### 7.1 Layout

```
┌ Host Analysis                                                         [Last 30 days ▾] ┐
│ Platform [Douyin ▾]  Type [All|Self-operated|Influencer]  Hosts [All ▾]               │
├ Influencer map: Reach × AOV (chart card, collapsible) ──────────────────────────────────┤
│  AOV ▲          Premium Niche  ┊  Flagship                                               │
│      │      ●            ●     ┊      ⬤                                                  │
│      │ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄ ┼ ┄┄┄┄┄┄┄┄┄┄  P50 AOV ¥275 ⓘ                              │
│      │   ●  ●                  ┊  ●        ●                                             │
│      │     Under Review        ┊  Traffic Engine          P50 exposure 23.9K/session ⓘ  │
│      └──────────────────────────────────────────────▶ Avg exposure per session (log)    │
│   bubble size = GMV · colour = tag · ring = borderline · hollow = not enough data       │
├ Leaderboard ─────────────────────────────────────────────────── [⇄ Compare hosts] ┤
│ 🔍 Search host   Tag [All ▾]   Columns ▾                                           │
│ # │ Host (type · tag) │ Sessions │ GMV (GMV/session) │ AOV │ CVR │ Exposure/session │ ① ② ③ ④ ⑤ │ Last live │ › │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

- The map shows **influencers only** (8.1). It uses a Recharts scatter chart (extension, 10.6) with tag colours from 10.3.
- **Host-level grades follow the Type filter** (All / Self-operated / Influencer, the same switcher as Session Analytics): leaderboard funnel and CVR tiers, Host drawer KPIs vs P50 and the host's session tiers use the group the filters define (Type = All: All types). The scope line names that group. Quadrant tags and the influencer map stay on the influencer group (8), so they do not move with the filter.
- With Type = Self-operated, the map is replaced by a note: "Self-operated rooms aren't tagged. Compare them over time in each host's drawer."

### 7.2 Leaderboard columns

The leaderboard fits the content width without horizontal scroll (≥ 1280px).

| Column | Definition | Default |
|---|---|---|
| # | Rank by Total GMV; every host is ranked, including greyed hosts with too little data | shown |
| Host | Name (avatar; pinned left), then type and quadrant tag under it. The tag (8) is a `Badge variant="outline"` with a tag-colour dot; its Tooltip gives AOV and exposure vs P50; clicking it opens the Benchmark drawer on AOV and exposure | shown |
| Sessions | Sessions in range | shown |
| GMV | Σ GMV in the time range, with Avg GMV / session (Total GMV ÷ Sessions) under it | shown, default sort ↓ |
| AOV | Σ GMV ÷ Σ paid orders (pooled) | shown |
| CVR | Σ paid buyers ÷ Σ entered (pooled). Plain number like AOV: no tier colour, no tier word, and not affected by the Rates / Counts switch | shown |
| Exposure / session | Σ live exposure UV ÷ Sessions | shown |
| Funnel: ① Entry · ② Product exposure · ③ Product click · ④ Click-to-pay · ⑤ Retention | Step rates in %, pooled across all the host's sessions. Each cell is tier-coloured and shows the rate and the tier word; its Tooltip gives rate, tier, P25 · P50 · P75 and UV; click opens the Benchmark drawer | shown |
| Last live | Date of the most recent session | shown |
| Total exposure, Paid orders, Best session GMV | Columns menu | hidden |
| Cost, ROI (Day 2) | Fees, commission, ad spend; GMV ÷ cost | hidden until data exists |

- APAC `DataTable`, controlled sort in both directions on every numeric column (`asc`/`desc` toggles), default Total GMV ↓. A Funnel header band spans ①–⑤. Rows follow the shared table rule (10.5) and end with a "View details" icon button.
- **Every host is listed with a rank** by Total GMV. Hosts with no lives in the range are listed last with "No lives in this range". Hosts below the minimum sample are greyed, with "Not enough data" and "n/a" funnel cells.
- Row click or map-dot click opens the Host drawer. Clicking a quadrant label filters the table to that tag.
- **Compare hosts** (primary button in the Leaderboard section header, right) starts host comparison (7.4). It sits with the leaderboard because it acts on the leaderboard rows; while selecting it reads "Selecting hosts…" and clicking it again cancels.

### 7.3 Host drawer (wide)

```
┌ 康姐的小管家                                                                                    ✕ ┐
│ Influencer · Douyin · Last 90 days · 9 sessions                                     (meta line)   │
│ Benchmark: the group the filters define (Type = All: Thorne × Douyin × All types · n=137 · 90d) ⓘ │
│ Tag: Flagship (borderline) ⓘ                                                         (scope row)   │
│ [Compare with…]  [Open in Session Analytics]                                       (actions row)   │
├ Summary │ Funnel │ Sessions ──────────────────────────────────────────────────────── Tabs line ───┤
│ Summary:  GMV · GMV/session · AOV · Exposure/session · CVR, each vs group P50 (opens Benchmark)  │
│           Tag with suggested plays for Flagship (its Tooltip: AOV ¥297 vs P50 ¥275 (+8%,         │
│           borderline) · Exposure 30.5K vs P50 23.9K per session (+27%))                         │
│           Trend: GMV and CVR per time gate (line chart, Chart 1 / Chart 2)                       │
│ Funnel:   aggregated funnel volume + Stage performance (same component as 6.3)                  │
│ Sessions: this host's sessions (same DataTable as 6.4) → row opens Session drawer (stacked)     │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

- **Header:** the title and meta line on the left with only Close on the right; the scope row (benchmark group, tag) under it; then the actions row (Compare with…, Open in Session Analytics); then KPIs and tabs.
- KPIs vs P50 and the host's session tiers use the group the filters define (Type = All: All types). In the Sessions tab the live topic gets the flexible column.
- The time range follows the filter bar and can be changed inside the drawer.
- "Open in Session Analytics" sets the filters to this host and opens the Overview.
- A Session drawer opened from here replaces the drawer content, with a "← Back to 康姐的小管家" link (one wide drawer at a time; the Benchmark drawer is the only stacked layer).

### 7.4 Host comparison (2–4 hosts)

Operators compare hosts to decide who gets the next slot, budget or product. The Overview compares two channel types; this compares named hosts with the same pattern.

**Starting a comparison**

1. **Compare hosts** (primary button in the Leaderboard section header) switches the leaderboard into **selection mode**:
   - a checkbox column appears (`DataTable selectable`), and map dots become selectable too;
   - a sticky selection bar appears above the table: "2 of 4 selected · [host chips with ✕] · **Compare (2)** · Cancel".
2. **Limits:** minimum 2, maximum **4** hosts (Q17). At 4, the remaining checkboxes are disabled, with the Tooltip "You can compare up to 4 hosts." Compare stays disabled below 2.
3. Also reachable from the Host drawer ("Compare with…", which opens selection mode with that host pre-selected) and by deep link `?compare=ACC003,ACC012`.
4. Hosts of both types can be compared. Hosts with "Not enough data" can be selected, but are flagged in the comparison.
5. The Platform and time range come from the filter bar. All compared hosts are on the same platform, because Platform is single-select.

**Comparison view** (wide drawer, the same width rules as the Host drawer)

```
┌ Compare hosts                                                                           ✕ ┐
│ Thorne × Douyin · Last 90 days · graded against All types (n=137)    (meta line, scope row) │
│ [+ Add host]  (shown only with fewer than 4 hosts)                          (actions row)   │
│ ■ LisaWang（15号…） Influencer · 13 sessions ✕          ■ 康姐的小管家 Influencer · 9 sessions ✕ │
│ ■ 环球健选 Influencer · 7 sessions ✕                    ■ Thorne悦恩运动极限海外店 Self-op. · 25 ✕│
├ Funnel, side by side ─────────────────────────────────────────────────────────────────────┤
│ Stage                  Hosts compared with each other (one bar per host)   Tier vs All types     │
│ ① Entry rate           ██████████ 29.38%                                    STAR                  │
│ ② Product exposure     ███ 27.74%                                           GOOD                  │
│ ③ Product click        ████ 9.68%                                           MID                   │
│ ④ Click-to-pay         ████████ 8.83%                                       GOOD                  │
│ ⑤ Retention            █████████ 81.88%                                     MID                   │
│   (one bar per host in each row; LisaWang shown)                                                   │
├ Outcomes ─────────────────────────────────────────────────────────────────────────────────┤
│ [CVR] [Avg AOV] [GMV / session] [Total GMV] [Exposure / session] [Sessions]  (4 values each) │
├ GMV per week (line chart, one line per host) ─────────────────────────────────────────────┤
├ Biggest differences (computed sentences) ─────────────────────────────────────────────────┤
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

(Values from `host_comparison_example` in the prototype data; the bars in this sketch are not to scale.)

- **Host chips** (header): colour swatch, name, then type and session count only (no host tag). ✕ removes a host from the comparison and the panel updates. With only two hosts left, ✕ ends the comparison: the drawer closes and the leaderboard returns to normal (no selection mode), so a comparison never shows a single host. Its accessible label says so ("Remove {host} (ends the comparison)").
- **+ Add host** (actions row) returns to selection mode with the current picks kept. It shows only while fewer than 4 hosts are compared; at 4 it is hidden, not disabled, and it reappears as soon as a host is removed.
- **Funnel, side by side:** one row per step:
  - The five step rates in %, ① Entry rate to ⑤ Retention rate (4.3 funnel display rule), e.g. LisaWang（15号悦恩活动）: 29.38%, 27.74%, 9.68%, 8.83%, 81.88%.
  - Each row has one bar per host in its series colour, with the value. At the right end of each bar, in a column headed "Tier vs {group}" (e.g. "Tier vs All types"), the tier is shown as coloured text (the Tag text colour, no Tag box), graded against the group the Type filter sets; every host shares that group, so no per-host type label is shown. The tier text opens the Benchmark drawer, its Tooltip gives the rate and benchmark. A one-line note above the rows says bars compare the hosts while tiers grade against the group.
- **Outcome tiles:** CVR, Avg AOV, Avg GMV / session, Total GMV, Avg exposure / session, Sessions. In host comparison each tile lists every host on its own row (name left, value right), with the leader in bold. No leader chips. The 2-series channel comparison keeps the two values side by side in columns, which uses the space better.
- **GMV trend:** a line per host over the time gates (P1).
- **Biggest differences:** 1–3 sentences computed from the numbers, from per-language templates, e.g. "Thorne悦恩运动极限海外店 converts entrants 8× better than the influencers compared (CVR 1.99% vs 0.17–0.30%); LisaWang brings the largest basket (AOV ¥2,115)."
- **Grading group:** all compared hosts are graded against the group the filters define (the column header names it, e.g. "Tier vs All types"). Only where hosts must be graded against their own type groups (no pooled All types group, 5.2) does each tier show its type, e.g. "GOOD / Influencer".
- **Actions:** "Open host" on each chip (opens that Host drawer, with a back link to the comparison); "Copy summary" (P1).

**Shared component.** The same **Comparison panel** renders the Overview channel comparison (2 series, type colours) and the host comparison (2–4 series, host colours). Its layout is channel-comparison **Option A** from the prototype (paired funnel rows, outcome tiles, insight sentence; no leader chips). The pattern must work for up to 4 series: a strictly two-sided head-to-head layout does not scale and is not used.

---

## 8. Auto-tagging model: Reach × AOV quadrants (influencers)

### 8.1 Why these two axes, and why influencers only

Livestream GMV decomposes into multiplicative factors:

```
GMV = Exposure × Entry rate × Product exposure × Product click × Click-to-pay × AOV
      └ reach ┘   └────────── conversion (how the session was run) ───────────┘   └ basket ┘
```

**Exposure** (how many people the host reaches) and **AOV** (how much each buyer spends) mostly reflect *who the host is*: audience size, spending power and product positioning. They are fairly stable across sessions. The middle factors reflect *how a session was run*, and Session Analytics already diagnoses them. A Reach × AOV map therefore describes each host's commercial profile and points to a lever: buy reach, raise the basket, or scale up. Funnel quality appears as a secondary signal (CVR tier), not as an axis.

**Influencers only.** Building the demo data showed that each brand has only 1–2 self-operated hosts per platform (13 hosts across 10 groups). Splitting at a median of one or two hosts would just compare a host with itself. The tag supports the decision it was designed for, which influencers to keep, scale or drop. Self-operated rooms are compared with their own history instead (Host drawer trend).

### 8.2 Inputs and thresholds

| Input | Definition | Threshold |
|---|---|---|
| X: Reach | Avg live exposure UV per session in the window (log scale on the map) | Benchmark group **P50 of exposure per session** |
| Y: AOV | Σ GMV ÷ Σ paid orders in the window (pooled) | Benchmark group **P50 of AOV** |
| Group | Same Brand × Platform × Influencer | As in 5.2 |
| Window | Official tag: the rolling benchmark window (90 days), for stability. The map can also be redrawn for the selected time range (Q7). | |

Using the benchmark group's P50s, rather than medians across hosts, keeps tags consistent with the rubric in the Benchmark drawer. It also works when a group has few hosts.

### 8.3 Tags

| Tag | Reach | AOV | Profile | Suggested plays | Chart colour |
|---|---|---|---|---|---|
| **Flagship** | ≥ P50 | ≥ P50 | Big audience that spends | Protect and scale: priority slots and stock, exclusive bundles, more lives | Chart 5 Violet |
| **Traffic Engine** | ≥ P50 | < P50 | Big audience, small basket | Raise the basket: bundles, "buy 2" pricing, pin a higher-price hero SKU | Chart 2 Teal |
| **Premium Niche** | < P50 | ≥ P50 | Small audience that spends | Buy reach: paid traffic (Qianchuan / DOU+ on Douyin, Taobao Live boost), pre-heat videos, better slots | Chart 3 Amber |
| **Under Review** | < P50 | < P50 | Small audience, small basket | Check the funnel first. If it is not the cause, renegotiate terms or reduce allocation | Chart 9 Slate |

Secondary signals shown with the tag, not used to assign it:

- **CVR tier** of the host (STAR/GOOD/MID/WEAK) as a small Tag beside the tag, e.g. "Traffic Engine · CVR STAR".
- **Change marker** when the tag changed in the last 30 days ("↑ from Premium Niche").

### 8.4 Eligibility, stability and edge cases

1. **Eligibility:** at least 3 sessions and at least 10 paid orders in the window; otherwise "Not enough data" (hollow grey dot).
2. **Benchmark building:** if the group has fewer than 20 sessions, no tags: "Benchmark building".
3. **Borderline:** within ±10% of either P50 → ring on the dot and "(borderline)" after the tag.
4. **Stability:** official tags recalculate daily. A tag changes only after the new quadrant holds for 2 consecutive recalculations.
5. **Outliers:** P50 thresholds are robust to extremes (in the demo data LisaWang's AOV is ¥2,115 against a P50 of ¥275). The map clips axes at P99 and pins clipped points to the edge with an arrow.
6. **Transparency:** the tag's Tooltip always shows both values, both thresholds and the group.

**Demo-data result** (as of 27 Oct 2026, 74 influencer hosts): Flagship 20 · Traffic Engine 12 · Premium Niche 10 · Under Review 13 · Not enough data 12 · Benchmark building 7 (in the three Building groups). The 13 self-operated hosts are untagged.

### 8.5 Pseudocode

```text
for each group in (brand, platform, "Influencer"):
    B = benchmark(group, window = 90d)                 # from 5.2
    for a in hosts(group):
        if B.status == "building":                     a.tag = "Benchmark building"; continue
        if a.sessions < 3 or a.paid_orders < 10:       a.tag = "Not enough data"; continue
        hi_reach = a.exposure_per_session >= B.exposure_per_session.p50
        hi_aov   = a.pooled_aov           >= B.aov.p50
        a.tag = {(T,T): "Flagship", (T,F): "Traffic Engine",
                 (F,T): "Premium Niche", (F,F): "Under Review"}[(hi_reach, hi_aov)]
        a.borderline = |a.exposure_per_session / p50 − 1| <= 0.10 or |a.pooled_aov / p50 − 1| <= 0.10
        apply_hysteresis(a, consecutive_days = 2)
self-operated hosts: tag = none ("Not tagged")
```

---

## 9. Settings (Admin)

Only Admins see **Settings** in the sidebar (Admin group). It uses the APAC **Detail / Settings page** template: a 240px section list on the left and the section content on the right. Breadcrumb: `Settings / Users & access`. The analytics filter bar is hidden here.

| Section | v1 | Content |
|---|---|---|
| **Users & access** | P0 | User list, roles, brand access |
| **Data connections** | P1, read-only | Platform connection status per brand (drives disabled Platform options), last sync, annual GMV source |
| **Benchmark rules** | P1, read-only | Window length, minimum sample, stage minimums, tier rule. Editable in a later version (Q4) |
| **Audit log** | P1 | Who changed roles or access, and when |

### 9.1 Users & access

```
┌ Settings ──────────┬ Users & access ───────────────────────────────── [Invite user] ┐
│ Users & access  ●  │ 🔍 Search name or email   Role [All ▾]  Brand [All ▾]  Status ▾ │
│ Data connections   │ ☐ Name        Email                 Role      Brands         Status     Source  Last active │
│ Benchmark rules    │ ☐ Chen Yu     chen.yu@example.com   Operator  Thorne         Active     Okta    27 Oct      │
│ Audit log          │ ☐ Zhao Hao    zhao.hao@example.com  Operator  Thorne +1      Active     Okta    21 Oct      │
│                    │ ☐ Liu Jia     liu.jia@example.com   Operator  — none         No access  Okta    15 Oct      │
│                    │ Bulk: [Assign brands] [Remove brands] [Deactivate]                     │
└────────────────────┴───────────────────────────────────────────────────────────────┘
```

- **Table** (APAC `DataTable`, `selectable`): name, email, role (`Badge`), brands (up to 2 names, then "+N" with the full list on hover), status (`Tag`: Active = positive, Invited = informative, No brand access = warning, Deactivated = neutral), source (Manual / Okta), last active. Sortable by name, role and last active.
- **Invite user** (primary button in the page header): a standard `Dialog` with 4 fields (within the ≤ 5-field rule): email, name, role (`Radio`: Operator, Admin), brands (`Checkbox` group). Inline validation on blur. On success: toast "Invitation sent to chen.yu@example.com".
- **Edit access** (row click): a 480px `Drawer` with role, brand checkboxes, status, and a read-only history of access changes. Save / Cancel in a sticky footer.
- **Deactivate / remove brand access:** a `Dialog` confirm, as the APAC rule for irreversible actions requires: "Deactivate Zhao Hao? They lose access to Thorne and Swanson immediately."
- **Bulk actions** on selected rows: assign brands, remove brands, deactivate (each confirmed).
- **Guardrails:** an Admin cannot remove their own Admin role or deactivate themselves; at least one active Admin must remain.

**Permission matrix**

| Capability | Operator | Admin |
|---|---|---|
| View Session Analytics and Host Analysis for assigned brands | ✓ | ✓ (all brands) |
| Open Benchmark drawers | ✓ | ✓ |
| Copy Action Card checklists, share links | ✓ | ✓ |
| See Settings | — | ✓ |
| Invite, edit and deactivate users; assign brands | — | ✓ |
| View data connections and benchmark rules | — | ✓ |

### 9.2 Okta SSO (phase 2)

- **Phase 1 (prototype and pilot):** an admin-managed allowlist. Users are created by email in Settings; sign-in uses the method in place today.
- **Phase 2:** sign-in through Okta SSO (OIDC). Users assigned to the TrendVision app in Okta are synced into the user list (SCIM), with source "Okta" and status taken from Okta. Deactivating a user in Okta deactivates them here.
- **Brand access stays in the app** by default: Okta decides *who can sign in*, Settings decides *which brands they see*. Mapping Okta groups to brands is an open question (Q10).
- A synced user with no brand gets the status "No brand access" and appears under that status filter, so admins can act.

---

## 10. Design system application (APAC Design System v1.3)

### 10.1 Page templates used

| Screen | APAC template | Notes |
|---|---|---|
| Overview | Dashboard | Metric-card rows of 4 (Live performance, Sales), then 2-column chart cards |
| Live Funnel | Dashboard (chart card + table) | |
| Sessions | List Page (DataTable) | Toolbar + DataTable + pagination |
| Host Analysis | List Page + one chart card | Map above the DataTable |
| Session / Host detail | Drawer Detail Panel, **wide variant** (extension), modal | 10.6, 10.5 |
| Benchmark drawer, Edit user | Drawer Detail Panel (480px), modal | Width as specified; modal overlay (10.5) |
| Settings | Detail / Settings Page | 240px section nav |
| Invite user, confirms | Dialog Standard / Alert | ≤ 5 fields |

### 10.2 Component mapping

| Product element | APAC component | Key props / rules |
|---|---|---|
| KPI cards | `DataMetric` | `variant="compare"`, `change`, `comparisonLabel="vs previous 30 days"`, `sentiment`, `tooltip` = definition, `status` loading/empty/error. Value in `metric-lg` |
| Recoverable revenue card | `DataMetric` | `compare` without change, or `progress` showing recoverable as % of GMV (Q11) |
| Tables | `DataTable` | Controlled `sort`, `onRowClick`, `loading`, `emptyState`, `pagination`, `selectable` (Settings, Compare) |
| Small tables (benchmark results) | `Table` primitives | |
| Tier, status | `Tag` | positive / informative / warning / negative / neutral (5.3); 1px border in the state colour, subtle fill, state-colour text, 6px radius |
| Quadrant tag, role | `Badge` | `outline`, with a tag-colour dot (a category, not a status) |
| Drawer tabs | `Tabs` | `line` variant (Session Analytics views are sidebar sub-items, not tabs) |
| Type and granularity toggles | `Tabs` | default (filled pill) variant, `sm`, used as a segmented control |
| Platform, presets, quick filters | `Select` | Grouped items where useful |
| Time range | `DatePicker` | `isRange`, `align="end"` |
| Search | `Input` | `type="search"` |
| Definitions on hover, truncated text | `Tooltip` | Read-only text only; 300ms delay; dark pill (#171717 / #FAFAFA) in both themes |
| Chart tooltips | Recharts tooltip card | `surface-raised`, `outline-default` border, float shadow (border only in dark mode); 10.5 |
| Column chooser, method notes, borderline detail | `Popover` | Click-triggered, `align="end"` |
| Benchmark drawer, Edit user | `Drawer` | `side="right"`, 480px |
| Session and Host drawers | `Drawer` + width extension | 10.6 |
| Invite user, confirms | `Dialog` | Standard / Alert; `DialogClose` on Cancel |
| Feedback | `Toaster` + `toast` | `position="top-right"`, 4s, errors persist |
| Loading | `Skeleton` | Per card and per table row; no full-page spinners |
| Empty states | `Empty` | `outline-dashed` inside cards; `default` for full pages |
| Navigation | `Sidebar` (with `SidebarMenuSub` sub-items under Session Analytics), `Breadcrumbs` | 3.4 |
| Language toggle | `Tabs` default variant, `sm` (segmented control) | 中文 \| EN in the top bar (3.5) |
| Compare selection | `DataTable` `selectable`, `isRowSelectable` (false once 4 are picked) + sticky selection bar | 7.4 |
| Comparison panel | Extension (10.6) | Overview channel comparison and host comparison |

### 10.3 Chart colour assignments

Charts use the APAC chart palette only, never state colours (APAC design decision). Assignments are fixed, so the same thing has the same colour everywhere:

| Series | Colour |
|---|---|
| Primary series (current period, GMV, funnel bars) | Chart 1 Blue |
| Comparison series (previous period, last year) | Chart 9 Slate (dashed for lines) |
| Self-operated / Influencer | Chart 1 Blue / Chart 2 Teal |
| Tiers STAR / GOOD / MID / WEAK / n.a. | Chart 6 Green / Chart 1 Blue / Chart 3 Amber / Chart 4 Pink / Chart 9 Slate |
| Tags Flagship / Traffic Engine / Premium Niche / Under Review | Chart 5 Violet / Chart 2 Teal / Chart 3 Amber / Chart 9 Slate |
| Compared hosts 1–4 (Host comparison only) | Chart 1 Blue, Chart 2 Teal, Chart 3 Amber, Chart 5 Violet, in selection order (Chart 4 Pink is skipped because it means WEAK elsewhere) |
| Benchmark band (P25–P75) and P50 tick | `surface-accent` fill, `outline-strong` tick |


### 10.4 Typography, spacing, elevation

- Page title `heading-md`; section headers (Live performance, Sales, Trends) `heading-sm` with a divider; card titles `label-lg`; KPI values `metric-lg` (`metric-md` in compact drawer cards); table headers `label-md`; captions and "as of" text `body-sm` in `text-tertiary`.
- Host names and live topics are often Chinese: render them in Noto Sans SC and allow for the ~4px taller CJK line height (48px rows still fit one line).
- Card padding: 24px for KPI cards, 16px for chart cards, 12px for dense table-adjacent panels. Card gap 16px; section gap 24px.
- Live performance KPI cards use the shadow `0 2px 4px rgba(0,0,0,0.05)`.
- Tier distribution segment labels use `text-on-primary`.
- Layers follow the APAC Z-INDEX SCALE (04 skill), bottom to top: in-page dropdowns and popovers 100; sticky content (host selection bar, table headers) 200; pinned page header 210, top bar 220, sidebar 230 (its icon-rail flyout inside it); Ask AI 250; drawer overlay / drawer 300 / 310 (wide drawers, Filters drawer, Edit access); stacked Benchmark drawer 320 / 330; dialogs and the off-canvas sidebar below md 400 / 410; toasts and tooltips 500. Every drawer and dialog overlay covers the sidebar and top bar, and dropdowns opened from the pinned header stay within it.
- Dark mode: all tokens have dark values; drawers and popovers use `outline-default` borders instead of shadows. Theme (Light / Dark) is a user setting in the avatar menu.

### 10.5 Interaction rules applied

- 150ms ease-out; overlays fade and scale (0.95 → 1.0).
- **Drawers slide in from the right edge:** `translateX(100%) → 0` over 280ms, `cubic-bezier(0.22, 1, 0.36, 1)`, while the overlay fades in over 200ms. Closing reverses it in 200ms (`cubic-bezier(0.4, 0, 1, 1)`) before the drawer unmounts. A stacked Benchmark drawer slides in over the wide drawer the same way. Switching sessions with Prev / Next or refocusing a metric does not replay the motion. With `prefers-reduced-motion`, drawers only fade (120ms).
- **One table behaviour everywhere:** table row hover is `bg-subtle` only (`DataTable onRowClick`); the whole row is the click target for drawers, and every row also ends with a "View details" icon button.
- **Drawers and dialogs are modal:** a dark overlay covers the whole viewport, sidebar included; a stacked Benchmark drawer adds its own overlay on top of the wide drawer. This deviates from the APAC Drawer Detail Panel template, where the sidebar stays interactive.
- Focus rings on `:focus-visible` only; drawers trap focus and return it to the row on close.
- Loading uses skeletons per card; the filter bar stays usable while data loads.
- **Pinned shell:** the sidebar, top bar and page header block stay in place while the page scrolls; the header block condenses into one row after 28px of scroll and expands again near the top (3.4). Sticky elements inside the page (the host selection bar, table headers) stick under the condensed header, not under the top bar.

**Tooltips**

- **Explanations live in Tooltips, not on the page:** grading rules, thresholds and "why" texts (e.g. why a host is tagged) sit in the Tooltip of the element they explain; the page keeps the value and the action (e.g. the Host drawer shows the tag with its suggested plays, and the tag's Tooltip gives AOV and exposure vs P50).
- **Chart tooltip** on every chart element: hovering (or keyboard-focusing) any bar, column, segment, point, track or heat cell shows the APAC chart tooltip, a card (`surface-raised`, `outline-default` border, float shadow; border only in dark mode) with a bold title, one row per value with its series swatch, and a short note on what it means. Column charts highlight the hovered column (crosshair band) and list every series at that position. Content per chart:

| Chart | Tooltip content |
|---|---|
| Session tier distribution | Sessions (k of n), share and the CVR range of the tier |
| Funnel by stage | Current, previous, change, P50 of the group and tier, stage definition |
| GMV trend | GMV, same week last year, YoY, sessions, paid orders |
| Channel / host comparison | Every series at that stage with its tier and group |
| Funnel volume | UV reached, % of exposed, step rate, UV lost, weakest-stage reason |
| Benchmark tracks and Stage performance gap bars (stage tables, Session drawer, Host drawer) | Rate, P25 · P50 · P75, vs P50, tier, vs previous |
| Stage performance rows | Rate, P50, gap, tier, trend and the suggested next step |
| Influencer map | Tag, AOV, exposure per session, GMV, sessions and what the quadrant means |
| Leaderboard funnel cells | Rate, tier, P25 · P50 · P75, UV |
| Benchmark drawer | Value with P25 / P50 / P75; per histogram bin, the sessions and share |
| Weekly GMV / CVR (Host drawer, host comparison) | Each line at that week |

- **Standard tooltip for truncated text:** table cells that can truncate (host, live topic, email, host names in lists) show the dark pill tooltip (#171717, 300ms delay, both themes) with the full text, only when the text is actually cut. This applies to every DataTable.
- Tooltips stay inside the viewport and hide on scroll. On touch screens the first tap shows the tooltip and the second tap runs the element's action; tapping elsewhere hides it.

### 10.6 Extensions needed in the design system

These are not in APAC v1.3. Build them from shadcn/ui with APAC tokens, as the skill directs, and propose them back to the design system:

| Extension | Why | Proposal |
|---|---|---|
| **Wide drawer** | Session and Host details hold a funnel, a table and cards; 480px is too narrow | `Drawer` width token "wide" = 75% of the content column (min 720px, max 1080px); the full content column at md–lg; full width below the top bar below md. Modal (10.5). Header: title and meta line left, Close right; scope row; actions row; then KPIs and tabs |
| **Multi-select combobox** | Hosts filter | Combobox with checkboxes, search, groups, "Select all in group", and a count in the trigger |
| **Segmented control** | Type and granularity | Formalise the `Tabs` default variant at `sm` as a segmented control |
| **Scatter chart** | Influencer map | Recharts `ScatterChart` with palette colours, log X axis and reference lines |
| **Benchmark track** | P25·P50·P75 band with a value dot | Small inline component (Benchmark drawer "Your value"); its label reads "P25 x · P50 y · P75 z" |
| **Gap bar** | Stage performance | Diverging bar of the gap to P50 relative to P50: dashed P50 line, bar colour = tier, label = gap in %, one scale per table capped at ±100% |
| **Funnel chart** | Funnel volume | Recharts horizontal bar with stage labels and drop annotations |
| **Comparison panel** | Channel type comparison (2 series) and host comparison (2–4 series) | Paired-bar funnel rows (optional "Tier vs {group}" column: coloured tier text; "/ type" only when hosts are graded against different groups) + outcome tiles (one row per series for hosts, side-by-side columns for 2 series) + insight sentences; series colours passed in; no leader chips |

---

## 11. Responsive behaviour

The primary target is desktop (≥ lg, 1280px), following the APAC breakpoints. Below lg the product stays fully usable for reading; editing in Settings is desktop-first. Tables never squeeze columns below a usable width: they scroll horizontally inside their card. KPI strips, summary strips and comparison layouts reflow to fewer columns.

| Area | ≥ xl (1440) | lg (1280–1439) | md (768–1279) | < md |
|---|---|---|---|---|
| Sidebar | 280px expanded, pinned; Live Funnel and Sessions as sub-items under Session Analytics | 280px (user can collapse to 64px) | 64px icon rail (auto), Tooltip labels; Session Analytics sub-items in a flyout on hover or focus | Off-canvas drawer with the sub-items as at xl; hamburger in the top bar |
| Content padding | 40px | 32px | 24px | 16px |
| Page header (pinned block) | Title and description left, time range right; condenses to one 52px row on scroll | same | same; the condensed time range drops its dates | Title, then time range full width; condensed: title and the "Filters (n)" button |
| Filter bar | One row | One row; Hosts trigger shortens to a count | Wraps to two rows | Collapsed into a "Filters (3)" button that opens a Filters drawer with Platform, Type and Hosts and Reset / Apply (changes apply only on Apply); the scope line stays visible |
| KPI cards | 4 columns | 4 columns | 2 columns | 1 column |
| Chart cards | 2 columns | 2 columns | 1 column | 1 column; legends below the chart |
| DataTables | All default columns | Funnel columns condensed to coloured tier text | Horizontal scroll inside the card, Host pinned, compact pagination | Horizontal scroll; Pagination summary and page size hidden (component default) |
| Influencer map | Full | Full | Full width, shorter | Replaced by a tag summary (4 counts); the map opens on tap |
| Wide drawers | 75% of content column | 75% (min 720px) | Full content column | Full width below the top bar; tabs scroll horizontally |
| Benchmark drawer | 480px | 480px | 480px | Full width below the top bar |
| Host comparison | 4 columns of bars per row | same | Bars stack per host under each step | One step per card; host chips scroll horizontally; max 4 hosts kept |
| Language toggle | 中文 \| EN in top bar | same | same | Moves into the avatar menu |
| Theme | Light / Dark in the avatar menu (APAC dark tokens) | same | same | same |
| Action Card columns | 3 columns | 3 columns | 3 columns | Stacked |
| Settings | 240px nav + content | same | Section nav becomes a `Select` above the content | Same as md; Edit-user drawer full screen |

---

## 12. States and edge cases

| State | Where | Behaviour |
|---|---|---|
| No brand access | Whole app | Full-page `Empty`: "You don't have access to any brand yet," with the admin contact |
| Link to an unassigned brand | Whole app | "No access to KELO-COTE" page, no data shown; "Request access" (P1) |
| Platform not connected | Platform Select | Disabled option, "Not connected". Never falls back to another platform's data. Demo: KELO-COTE × JD, Swanson × RED |
| No sessions in scope | Any view | `Empty` naming the active filters, with "Widen time range" and "Clear hosts" |
| Benchmark building | Scope line, tiers, tags | "Benchmark building (n=14 of 20)". Values shown; tiers and tags hidden. Demo: KELO-COTE × RED × Self-operated, KELO-COTE × Tmall × Influencer, Swanson × JD × Influencer |
| Not enough data (stage / host) | Tables, cards, map | Neutral Tag "Not enough data", reason in a Tooltip. Never a WEAK badge |
| Mixed types | Overview tiers, Live Funnel | Combined values graded against the All types group; per-type rows graded against their own type |
| No pooled All types group | Type = All | Each session, host and sub-row graded against its own type; combined values untiered; P50 footnotes read "Combined value · each session is graded against its own type" |
| Host with no sessions in range | Host leaderboard | Listed last with "No lives in this range" |
| Hosts dropped by a filter change | Hosts | Toast: "2 hosts removed: not Self-operated" |
| Live session | Sessions, drawers | "Live now" Tag; excluded from benchmarks, tiers and KPIs until it ends and syncs |
| Quarantined session | Sessions | Listed with a neutral "Excluded" Tag and the reason; excluded from all aggregates |
| Loading | All | Skeletons per card and row; filter bar usable |
| Error | Cards, tables | `DataMetric status="error"`; DataTable `error` + `errorState` with "Retry" |
| Data freshness | Scope line | "Data as of 28 Oct 08:00 · Benchmark as of 27 Oct" |
| Compare limit | Selection mode | At 4 hosts, other checkboxes disabled with the Tooltip "You can compare up to 4 hosts"; Compare disabled below 2 |
| Compared host with little data | Host comparison | Its values are shown with a neutral "Not enough data" Tag and no tier Tags |
| Missing translation | Any | Never shown to users: missing keys fail the build; in development, the English string with a visible marker |

---

## 13. Data and integration

- **Sources:** session-level funnel and order data per platform (Douyin, RED, Tmall, JD) through MCP/API connectors (sync frequency: Q13). Each platform maps its native events to the five stages in 4.3. The mapping is documented per platform (Q8), because "product exposure" and "click" differ between platforms.
- **Annual GMV:** provided by the platform MCP per brand × platform; used only to annualise recoverable revenue.
- **Benchmarks:** a daily job computes P25/P50/P75 per Brand × Platform × Type (Self-operated, Influencer and All types) for each stage rate, CVR, AOV and exposure per session over the rolling window. Results are stored with their window dates. When the filters change, every value is re-graded against the group they define.
- **Session scoring:** a session is graded against the filtered group's current rolling 90-day window, like every other value. Its tiers can change as the window moves; the stored tier columns in `sessions.csv` are a snapshot for the demo only.
- **Tags:** a daily job runs the section 8 model and stores tag history (change marker, hysteresis).
- **Users and access:** a user table (id, email, name, role, status, source) and a user–brand access table; Okta sync in phase 2.
- **Session metadata needed:** session ID, host ID, type, platform, start and end time, live topic. Start time and topic tell same-day sessions apart and feed search.
- **Not available yet:** cost data (fees, commission, ad spend), traffic-source split (organic, paid, short-video bridge), SKU-level sales, and an in-session minute timeline. See Appendix C.2.

---

## 14. Day 2 and later

- **Risk Radar** and **Live Playbook Builder** as their own modules in the Analytics sidebar group, sharing the brand context and filters. Both get a tab slot in the Session drawer. Playbook Builder › Follow-through answers "did the changes work?" (G8); v1 has no stage-by-stage comparison with a host's previous session.
- **ROI:** cost, fee and commission data per host and session; ROI columns in the host leaderboard; an ROI axis option on the influencer map.
- **Multi-brand groups:** admin-configured groups appear in the brand switcher; benchmarks stay per brand.
- **Alerts:** notify when a host's tag changes or a session lands in WEAK.
- **Editable benchmark rules** in Settings (window, minimums), with versioning so past tiers stay reproducible.

---

## 15. Requirements

P0 = required for the first prototype and release · P1 = release · P2 = later. "Audit" refers to issue IDs in the audit doc; "Gap" to Appendix C.2.

| ID | Area | Requirement | Priority | Ref |
|---|---|---|---|---|
| R1 | Shell | APAC Page Shell: full-height pinned sidebar (280 / 64 / off-canvas) with Live Funnel and Sessions as sub-items under Session Analytics (flyout on the icon rail), pinned 48px top bar with breadcrumb, one pinned page header per view that condenses on scroll, content max-width 1440px | P0 | 3.4 |
| R2 | Context | Brand switcher in the sidebar header lists only the user's brands; switching resets the filters | P0 | — |
| R3 | Filters | Platform (single) > Type (All / one) > Hosts (multi, searchable); time range in the page header; granularity inside trend cards | P0 | Audit I4, I10 |
| R4 | Filters | Scope line names the benchmark group(s), sample size, window and data freshness; each name opens the Benchmark drawer | P0 | Audit I2 |
| R5 | Filters | Controls that do not apply are disabled with a reason; unconnected platforms are disabled | P0 | Audit I4 |
| R6 | Filters | All filter and drawer state in the URL | P1 | — |
| R7 | Vocabulary | One funnel vocabulary (4.3) with Tooltip definitions and a glossary | P0 | Audit I6, I7 |
| R8 | Benchmarks | Rolling benchmarks per Brand × Platform × Type with minimum samples and a Building state | P0 | Audit I1–I3 |
| R9 | Tiers | Quartile tiers against the group the filters define, recalculated live; no tier for small samples | P0 | Audit I1, I11 |
| R10 | Tiers | Session tier = CVR quartile (pending Q5) | P0 | 5.3 |
| R11 | Benchmark drawer | Every tier, P50, track, median line and tag opens the Benchmark drawer with group, window, sample, method, all results and the value's position | P0 | 5.4 |
| R12 | Overview | Live performance cards: sessions analyzed, CVR, exposed rate, product exposure rate; tier distribution card | P0 | — |
| R13 | Overview | Sales cards: total GMV, avg GMV/session, paid orders, avg AOV; recoverable revenue card | P0 | Audit I9 |
| R14 | Overview | Trends: funnel vs previous period; GMV over the last 7 time gates with MoM and YoY | P0 | — |
| R15 | Overview | Channel type comparison only when Type = All and both types have data | P1 | Audit I14 |
| R16 | Overview | Sessions section with Latest / Top GMV / Most upside toggle and "View all sessions" | P1 | C.1 |
| R17 | Live Funnel | Aggregated funnel volume and one Stage performance table (gap to P50, tier, UV lost, next step) under all filters; per-type rows when Type = All | P0 | — |
| R18 | Live Funnel | Weakest-stage rule stated; link to the sessions weakest at each stage | P1 | Audit I8 |
| R19 | Sessions | Searchable, sortable, paginated DataTable (date, host, live topic) | P0 | Audit I10 |
| R20 | Sessions | Quick filters (tier, weakest stage); optional stage columns; live and excluded sessions labelled | P1 | — |
| R21 | Session drawer | Wide drawer, default tab Action Cards, KPI strip in header, Summary tab; prev/next; deep link | P0 | Audit I5 |
| R22 | Action Cards | Per single session only; in funnel order with severity labels; three-part card; "Copy actions for host briefing" (P1) | P0 | Audit I5 |
| R24 | Hosts | Leaderboard with Sales, Reach and Funnel column groups; pooled metrics; two-way sort; search; hosts without sessions hidden | P0 | Audit I13 |
| R25 | Hosts | Reach × AOV tag for influencers (section 8); Tooltip reason; tag filter | P0 | — |
| R26 | Hosts | Influencer map (scatter) above the table | P1 | — |
| R27 | Hosts | Host drawer: summary vs P50, tag with suggested plays (reason in its Tooltip), aggregated funnel, trend, sessions | P0 | Audit I13 |
| R28 | Hosts | Host comparison: Compare hosts action, selection mode (2–4), comparison drawer, deep link | P0 | 7.4 |
| R29 | Settings | Users & access: user table, invite (Dialog), edit (Drawer), deactivate (confirm), bulk brand assignment, guardrails | P0 | 9.1 |
| R30 | Settings | Brand-level access enforced everywhere (switcher, URLs, shared links, API) | P0 | 2.1 |
| R31 | Settings | Data connections and Benchmark rules (read-only); audit log | P1 | 9 |
| R32 | Auth | Okta SSO + SCIM user sync (phase 2) | P1 | 9.2 |
| R33 | Design system | Components, colours, typography and overlays per section 10; extensions in 10.6 built on shadcn/ui with APAC tokens | P0 | 10 |
| R34 | Responsive | Behaviour per section 11 | P0 (≥ md), P1 (< md) | 11 |
| R35 | States | Empty, building, not-enough-data, live, excluded, loading, error, freshness, no-access states (section 12) | P0 | 12 |
| R36 | Data | Provisional retention until refunds mature | P1 | Gap G3 |
| R37 | Export | CSV export of Sessions and Host tables; Overview "Copy summary" | P1 | Gap G11 |
| R38 | Currency | CNY throughout; optional USD toggle | P2 | Audit I9 |
| R39 | Language | zh-CN and en for every screen, string and generated sentence; toggle in the top bar; per-user preference | P0 | 3.5 |
| R40 | Language | Fixed bilingual terminology (Appendix B) used everywhere; operator review before release | P0 | 3.5 |
| R41 | Language | Locale formatting: 万/亿 vs K/M, date formats, plural rules; DS localisation props | P0 | 3.5 |
| R42 | Terminology | "Host" is the only UI term for accounts and KOLs | P0 | 4.3 |
| R43 | Components | One Comparison panel for channel types (2) and hosts (2–4) | P0 | 7.4 |
| R44 | Tooltips | Chart tooltip on every chart element; full-text tooltip on every truncated cell; explanations in Tooltips, not on the page | P0 | 10.5 |
| R45 | Drawers | Modal drawers with overlay, slide motion (280ms in, 200ms out; fade with reduced motion) and the wide-drawer header layout | P0 | 10.5, 10.6 |

---

## 16. Assumptions and open questions

**Assumptions:**

- **A1.** "Time gate" = one bucket at the selected granularity; "previous period" = the period of equal length right before the selected range.
- **A2.** "Exposed rate" on the Overview = Entry rate (stage ①).
- **A3.** Benchmark window = trailing 90 days, minimum 20 sessions per group.
- **A4.** "Exposure times" in the host table = live exposure UV, shown as a total and per session.
- **A5.** Times are shown in China Standard Time (UTC+8).

**Open questions:**

- [ ] **Q2.** Confirm "Exposed rate" = Entry rate (stage ①).
- [ ] **Q4.** Rolling window length and minimum sample size; should self-operated groups use a longer window (G9)?
- [ ] **Q5.** Session tier by CVR quartile (recommended) or by the five-stage composite?
- [ ] **Q6.** Keep empirical-Bayes smoothing for low-traffic sessions?
- [ ] **Q7.** Should the influencer map follow the selected time range, or only the 90-day official tag?
- [ ] **Q8.** Event mapping to the five stages for RED, Tmall and JD: owner, and are all five stages available on each platform?
- [ ] **Q9.** Are the tag names (Flagship, Traffic Engine, Premium Niche, Under Review) clear to operators? Should Chinese names sit alongside?
- [ ] **Q10.** Okta phase 2: keep brand access in the app, or map Okta groups to brands?
- [ ] **Q11.** Recoverable revenue card: an absolute value, or a progress card showing it as % of GMV?
- [ ] **Q13.** Data sync frequency and acceptable delay after a live ends.
- [ ] **Q14.** Which of the open gaps (G1, G3–G9, G11–G13) belong in v1, Day 2, or later?
- [ ] **Q15.** Review the proposed Chinese terms in Appendix B with operators (especially 主播 for "host", 留存率 for retention, and the tier and tag names).
- [ ] **Q17.** Confirm a maximum of 4 hosts per comparison (it keeps the bars readable and fits the 4 distinct chart colours).

---

## Appendix A. Demo dataset

Synthetic data for prototyping the mixed, multi-platform analytics. Folder: `demo-data/`. Douyin values are loosely calibrated to the staging app (e.g. self-operated product exposure ~89%, influencer ~22%). The other platforms follow plausible but **invented** patterns: higher entry and product exposure on Tmall and JD (shopping intent, store-based lives), smaller reach and higher AOV on RED. Account names on Douyin come from the staging app; all others, and all users, are fictional. Seasonal lifts are included for 11.11, 618, 38 and Double 12, and a dip in February.

### A.1 Files

| File | Rows | Content |
|---|---|---|
| `sessions.csv` | 4,136 | One row per session, 1 Sep 2025 – 28 Oct 2026: funnel counts, orders, GMV, refunds, watch time, status (ok / quarantined / live), stage rates, stage tiers, `session_tier_cvr` (recommended rule), `session_tier` (composite), weakest stage, recoverable revenue, benchmark n |
| `accounts.csv` | 87 | Account ID, brand, platform, type, name, active dates |
| `benchmarks.csv` | 20 | Snapshot as of 27 Oct 2026 (90-day window) per Brand × Platform × Type: n sessions, n excluded, n accounts, status (ready / building), P25/P50/P75 for 5 stage rates, CVR, AOV, exposure per session |
| `host_tags.csv` | 87 | Per account, 90-day window: sessions, GMV, orders, AOV, exposure, pooled stage rates, CVR, tag, borderline, CVR tier |
| `platform_connections.csv` | 12 | Brand × platform: connected or not, last sync, annual GMV (simulating the MCP value) |
| `users.csv` | 7 | Fictional users with roles, brand access, status and source, for the Settings prototype |
| `generate_demo_data.py` | — | Reproducible generator (fixed seed): `python3 generate_demo_data.py <output_dir>` |

### A.2 Coverage (sessions)

| Brand | Douyin | RED | Tmall | JD |
|---|---|---|---|---|
| Thorne | 547 | 328 | 627 | 250 |
| KELO-COTE | 764 | 219 | 215 | not connected |
| Swanson | 515 | not connected | 449 | 222 |

### A.3 Built-in demo scenarios

| Scenario to prototype | Where it appears in the data |
|---|---|
| Platform not connected | KELO-COTE × JD, Swanson × RED |
| Benchmark building | KELO-COTE × RED × Self-operated (14 sessions), KELO-COTE × Tmall × Influencer (13), Swanson × JD × Influencer (16) |
| Small self-operated groups (G9) | Every self-operated group has 1–2 accounts |
| Extreme outlier | LisaWang（15号悦恩活动）, Thorne × Douyin: AOV ¥2,115 vs a P50 of ¥275 (tagged Flagship) |
| Borderline tag | 康姐的小管家, Thorne × Douyin: AOV +8% over P50 |
| Not enough data | 12 influencers with fewer than 3 sessions or 10 orders in the window |
| Host with no sessions in range | 李娜老师讲修行(臻健来), Thorne × Douyin |
| Live session | S99999, KELO-COTE芭克母婴海外, 28 Oct 2026 14:00 |
| Quarantined sessions | 41 sessions with status `quarantined` |
| Sessions with zero buyers | Recoverable revenue uses the group's median GMV per buyer |
| Composite vs CVR tier disagreement (Q5) | Compare the `session_tier` and `session_tier_cvr` columns |
| Users without brand access, invited, deactivated | `users.csv` U006, U005, U007 |
| YoY trend | Sep–Oct 2025 vs Sep–Oct 2026, including the 11.11 pre-sale lift from 20 Oct |

## Appendix B. Bilingual terminology (proposed, for operator review)

One term per concept. Platform-native wording is used where operators already know it (Douyin Compass / 抖音罗盘 style). Items marked † need confirmation (Q15).

| Concept | English (UI) | 中文 (UI) |
|---|---|---|
| Product name | TrendVision Live · Performance Analytics | TrendVision Live · 直播效果分析 |
| Session Analytics | Session Analytics | 场次分析 |
| Overview / Live Funnel / Sessions | Overview / Live Funnel / Sessions | 概览 / 直播漏斗 / 场次列表 |
| Host Analysis | Host Analysis | 主播分析 |
| Page descriptions (one per view, 3.4) | Session Analytics: How your lives perform against their benchmark · Live Funnel: Where viewers drop off, stage by stage, across every session in scope · Sessions: Every session in scope. Open one to see what to fix before the next live · Host Analysis: Which hosts are worth investing in: reach, basket and funnel | 直播整体表现与基准对比 · 按环节查看范围内所有场次的流失情况 · 范围内的所有场次，打开任一场次查看下场前要改进的地方 · 从触达、客单价和漏斗判断哪些主播值得投入 |
| Settings · Users & access | Settings · Users & access | 设置 · 用户与权限 |
| Host | Host | 主播 † |
| Self-operated / Influencer | Self-operated / Influencer | 自营 / 达人 |
| Brand / Platform / Type | Brand / Platform / Type | 品牌 / 平台 / 类型 |
| Douyin / RED / Tmall / JD | Douyin / RED / Tmall / JD | 抖音 / 小红书 / 天猫 / 京东 |
| Session | Session | 场次 |
| Live topic | Live topic | 直播主题 |
| Exposed (UV) | Exposed | 曝光人数 |
| Entered | Entered | 进房人数 |
| ① Entry rate ("Exposed rate" on the Overview) | Entry rate | 曝光进房率 |
| ② Product exposure rate | Product exposure rate | 商品曝光率 |
| ③ Product click rate | Product click rate | 商品点击率 |
| ④ Click-to-pay rate | Click-to-pay rate | 点击成交率 |
| ⑤ Retention rate | Retention rate | 留存率（未退款）† |
| CVR | CVR | 进房成交转化率 |
| GMV / Avg GMV per session | GMV / Avg GMV / session | 成交金额 / 场均成交金额 |
| Paid orders / Avg AOV | Paid orders / Avg AOV | 成交订单数 / 客单价 |
| Refund rate | Refund rate | 退款率 |
| Avg watch time | Avg watch time | 平均观看时长 |
| Recoverable revenue | Recoverable revenue | 可提升成交额 |
| UV lost / Weakest stage | UV lost / Weakest stage | 流失人数 / 最弱环节 |
| Benchmark / benchmark group | Benchmark / benchmark group | 基准 / 基准组 |
| Rolling 90 days | Rolling 90 days | 近90天滚动 |
| Benchmark building | Benchmark building | 基准积累中 |
| Not enough data | Not enough data | 数据不足 |
| Tiers STAR / GOOD / MID / WEAK | STAR / GOOD / MID / WEAK | 优秀 / 良好 / 中等 / 待提升 † |
| Session tier | Session tier | 场次等级 |
| Action Cards | Action Cards | 行动建议卡 |
| Critical / Action needed / Watch / Strong | Critical / Action needed / Watch / Strong | 紧急 / 需改进 / 关注 / 保持 |
| What happened / Before next session / Expected recovery | What happened / Before next session / Expected recovery | 发生了什么 / 下场前要做 / 预计提升 |
| Tags Flagship / Traffic Engine / Premium Niche / Under Review | Flagship / Traffic Engine / Premium Niche / Under Review | 旗舰型 / 流量型 / 高客单潜力型 / 待评估 † |
| Borderline | Borderline | 临界 |
| Compare hosts / Compare (n) | Compare hosts / Compare (n) | 主播对比 / 对比（n） |
| Channel type comparison | Channel type comparison | 渠道类型对比 |
| Biggest difference | Biggest difference | 最大差异 |
| Previous period / MoM / YoY | vs previous period / MoM / YoY | 较上期 / 环比 / 同比 |
| Last 7 / 30 / 90 days | Last 7 / 30 / 90 days | 近7天 / 近30天 / 近90天 |
| Data as of | Data as of | 数据更新于 |
| Operator / Admin | Operator / Admin | 运营 / 管理员 |
| Invite user / Deactivate | Invite user / Deactivate | 邀请用户 / 停用 |
| No brand access | No brand access | 无品牌权限 |
| Live now | Live now | 直播中 |

---

## Appendix C. Answer-path review and known gaps

### C.1 Answer-path check

Each key question is traced from the default landing page (Overview, last 30 days, Type = All).

| Question | Path | Clicks | Verdict |
|---|---|---|---|
| S1 How did our lives do this month? | Overview KPI rows | 0–1 (time range) | ✓ Answered on landing |
| S2 Are we getting better? | Overview deltas + Trends | 0 | ◐ Answers "vs before", not "vs plan": there are no targets (G4) |
| S3 Self-operated or influencers? | Overview channel comparison | 0 | ✓ |
| S4 Where do viewers drop off? | Live Funnel | 1 | ✓ |
| S5 What do I fix from last night's live? | Sessions → row (newest first) → Action Cards | 2 | ✓ The Session drawer opens on **Action Cards by default**, with a KPI strip in the drawer header |
| S6 Which hosts deserve more budget? | Host Analysis → tag + columns → Host drawer | 1–2 | ◐ Performance yes; ROI no (G1) |
| S7 Why is this WEAK? | Any grade → Benchmark drawer | 1 | ✓ |
| S9 How do these hosts compare? | Host Analysis → Compare hosts → tick 2–4 → Compare | 2 + selections | ✓ (7.4) |
| S8 Give a new hire access to one brand | Settings → Invite user | 2 | ✓ |
| How does Douyin compare with Tmall for us? | Switch Platform and read the Overview | 2 | ◐ Out of scope: Platform stays single-select (G2) |
| Which products drove GMV? | — | — | ✗ No SKU data (G5) |
| When in the live did viewers leave? | — | — | ✗ No in-session timeline (G6) |
| Did paid traffic pay off? | — | — | ✗ No traffic-source split (G7) |
| Did the changes we made last time work? | — (v1) · Playbook Builder › Follow-through (Day 2, proposed) | — | ✗ in v1: no stage-by-stage comparison with the previous session; follow-through is in Playbook Builder (Day 2, G8) |

**Overall:** the redesign answers the "what happened, where, and how do I compare" questions within two clicks, and every grade explains itself. The remaining gaps are about **why** (products, traffic, timeline) and **so what** (targets, ROI).

### C.2 Known gaps

| ID | Gap | Why it matters for brand operators | Suggested direction | Decision needed |
|---|---|---|---|---|
| G1 | **No cost or ROI data** | Host decisions are about return, not GMV alone | Add fee / commission / ad spend per session or per contract; ROI column and map axis | Data source and owner |
| G2 | **Cross-platform view** (resolved: out of scope) | — | Platform stays single-select everywhere, including Overview sales and GMV. No "All platforms" option in v1 | — |
| G3 | **Refunds mature after the live** | Retention and refund rate keep changing for 7–15 days, so recent sessions look better than they are | Mark stage ⑤ "Provisional until D+15"; exclude immature sessions from the retention benchmark | Refund window per platform |
| G4 | **No targets** | "Are we on track?" is a daily question | Monthly GMV / CVR targets per brand × platform (Settings), shown as a target line on the GMV trend and as progress `DataMetric` cards | Who sets targets, and at which level |
| G5 | **No product (SKU) view** | AOV and click-to-pay plays (bundles, hero SKU) need SKU sales | A Products tab in the Session drawer: SKU, clicks, orders, GMV | SKU data availability per platform |
| G6 | **No in-session timeline** | Action Cards say *which* stage leaked, not *when* | Minute-level viewers / entries / orders with product-pin markers in the Session drawer; links to the existing Replay & Hooks | Is minute data available per platform? |
| G7 | **No traffic-source split** | "Buy reach" plays need paid vs organic vs short-video traffic | Add traffic-source shares to sessions; split stage ① by source | Data availability |
| G8 | **No action follow-through** | Operators cannot see whether an Action Card was applied, or whether it worked | Mark cards "Planned / Done" and compare the next session's stage (links to Playbook Builder, Day 2) | In scope for Day 2? |
| G9 | **Self-operated benchmark groups are tiny** | Most brands have 1–2 self-operated hosts per platform, so their benchmark is mostly their own history | Keep the group, but say so in the Benchmark drawer: "This group contains 1 host; tiers compare this room with its own recent sessions." Consider a longer window for self-operated groups | Accept wording; window length |
| G10 | **UI language** (resolved) | — | Bilingual zh-CN / en foundation (3.5, Appendix B) | — |
| G11 | **Sharing and export** | Weekly reports to managers are routine; share links only work for users with brand access | Raise CSV / image export to P1; add "Copy summary" on the Overview | Priority |
| G12 | **Admin scope** | All Admins currently manage all brands | Optional "Brand admin" who manages users for their brands only | Needed in v1? |
| G13 | **Ask AI** | It exists in the current app but is not specified; it should use the same filters, benchmarks and vocabulary | Spec it separately: scope-aware prompts ("Explain this session's WEAK stage") | Owner and scope |
