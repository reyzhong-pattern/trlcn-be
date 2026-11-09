# Design brief: TrendVision Live — Performance Analytics (prototype)

Version: matches product spec v0.4 (5 Nov 2026). This is a condensed brief for Claude Design. The full product spec (`03-product-spec-v0.4.md`) is the source of truth when something here is unclear.

## 1. Product in one paragraph

A desktop web app for **brand operators** who run livestream commerce for one brand across Douyin, RED, Tmall and JD. It answers three questions: *How are my lives performing?* (Session Analytics), *What should I fix in a specific session?* (Action Cards per session), and *Which hosts are worth investing in?* (Host Analysis). Every grade is measured against a **rolling benchmark** of comparable sessions, and every grade can be clicked to see that benchmark (the Benchmark drawer). The audience is non-analysts: labels are plain, numbers carry units, and nothing is graded without its comparison group being shown.

## 2. Design system

Use the **APAC Design System** (Pattern): React + Tailwind + shadcn/ui + Recharts, Geist / Noto Sans SC, 4px grid, light and dark. Follow its page templates, components, overlay rules and chart palette exactly. Components not in the system (wide drawer, multi-select combobox, segmented control, scatter chart, benchmark track, funnel bars) are built from shadcn/ui with APAC tokens.

Key rules:

- **Shell:** full-height pinned sidebar 280px (64px icon-only at md–lg, off-canvas below md); pinned 48px top bar inside the content column with a breadcrumb on the left and avatar on the right; a pinned page header block per view; content max-width 1440px, horizontal padding 40/32/24/16px.
- **Type scale:** page title `heading-md`; section headers `heading-sm` + divider; card titles `label-lg`; KPI numbers `metric-lg`; table headers `label-md`; captions `body-sm` `text-tertiary`.
- **Cards:** KPI cards padding 24px; chart cards 16px; grid gap 16px; section gap 24px.
- **Overlays:** Tooltip = read-only definitions (dark pill); chart tooltip = the APAC chart tooltip card on chart elements (see 5.9); Popover = small click-triggered panels; Drawer = detail panels (480px standard); Dialog = short forms, confirms and the copied-text preview; Toast top-right.
- **Charts** use the chart palette only, never state colours.

## 3. Navigation and layout

```
Sidebar (full height, pinned)            Content column
┌───────────────┐  ┌──────────────────────────────────────────────────────────┐
│ Pattern logo  │  │ Top bar: Session Analytics / Live Funnel [中文|EN] 🔍 (MJ)│
│ Brand [Thorne▾]  ├──────────────────────────────────────────────────────────┤
│               │  │ ┌ Pinned page header ────────────────────────────────┐ │
│ ANALYTICS     │  │ │ Live Funnel                       [Last 30 days ▾] │ │
│ ▣ Session     │  │ │ Where viewers drop off, stage by stage, …          │ │
│   Analytics   │  │ │ Platform [Douyin▾] Type [All|Self-op|Infl.]         │ │
│   │ Live      │  │ │   Hosts [All hosts (14) ▾]                          │ │
│   │ Funnel  ◀ │  │ │ Benchmark: Thorne × Douyin × All types · 90d · n=137│ │
│   │ Sessions  │  │ └────────────────────────────────────────────────────┘ │
│ ◫ Host Analysis  │ … content …                                              │
│ ADMIN         │  │                                                          │
│ ⚙ Settings    │  │                                                          │
└───────────────┘  └──────────────────────────────────────────────────────────┘
Scrolled: the header block condenses to one 52px row under the top bar:
  Live Funnel  [Douyin ▾] [All|Self-op|Infl.] [All hosts (14) ▾]  [Last 30 days ▾]
```

- **Logo:** use `Pattern-brand asset/Logo_full.svg` at the top of the expanded sidebar and `Pattern-brand asset/Logomark_blue.svg` when it is collapsed to 64px.
- **Brand** is the workspace, chosen in the sidebar header. It is not a filter.
- **Session Analytics views live in the sidebar:** the Session Analytics item is the **Overview** page and the default landing; **Live Funnel** and **Sessions** are sub-items indented under it. The open view has the active fill; while a sub-item is open, the parent is bold with no fill. There is no view tab row. The sidebar stays pinned while the page scrolls, so views can be switched anywhere; switching keeps the filters and opens the view at the top. In the 64px icon rail the sub-items open in a flyout menu from the Session Analytics icon.
- **Breadcrumb:** "Session Analytics" on the Overview landing, "Session Analytics / Live Funnel", "Session Analytics / Sessions", "Host Analysis", "Settings / Users & access".
- **Page header, one per view:** title and a one-line description on the left, time range on the right. Session Analytics: "How your lives perform against their benchmark"; Live Funnel: "Where viewers drop off, stage by stage, across every session in scope"; Sessions: "Every session in scope. Open one to see what to fix before the next live"; Host Analysis: "Which hosts are worth investing in: reach, basket and funnel".
- **Pinned header block:** page header, filter bar and scope line are one block pinned under the top bar. After a short scroll it condenses into one 52px row (title, Platform, Type, Hosts without their labels, time range); the description and scope line hide until you are back at the top. The content never jumps, and the dropdowns open from the condensed row. Settings keeps a plain page header.
- **Language toggle** 中文 | EN (segmented control) in the top bar, left of search. See section 4b.
- **Filter bar** (in the pinned header block, shared by Session Analytics and Host Analysis): Platform (single select) > Type (All / Self-operated / Influencer, segmented) > Hosts (multi-select with search, grouped by type, shows a count).
- **Time range** (presets: Last 7 / 30 / 90 days, This month, Last month, This quarter, Custom) sits on the right of the page header. **Granularity** (Day / Week / Month) is not in the page header: it sits inside each trend chart card it controls.
- **Avatar menu** (top bar, right): profile, **theme** (Light / Dark) and sign out.
- **Scope line** under the filter bar names the benchmark group the filters define (Type = All: the All types group). The name is a link that opens the Benchmark drawer.
- **Details open in drawers** that slide in from the right edge (280ms). Drawers and dialogs are modal: a dark overlay covers the whole viewport, the pinned sidebar, top bar and page header included; overlays always sit above the pinned shell. Session and Host details use a **wide drawer** (75% of the content column, min 720px, max 1080px). The **Benchmark drawer** is 480px and stacks on top of any page or drawer.
- **Content padding:** 40 / 32 / 24 / 16px from xl down to mobile; content max-width 1440px.

## 4. Vocabulary (use exactly)

**Host** = any account that runs lives: a self-operated brand room or an influencer (KOL). Always say "host" in the UI, never "account" or "KOL".

| Stage | Name | Formula |
|---|---|---|
| ① | Entry rate (Overview card label: "Exposed rate") | Entered ÷ Exposed |
| ② | Product exposure rate | Saw a product ÷ Entered |
| ③ | Product click rate | Clicked ÷ Saw a product |
| ④ | Click-to-pay rate | Paid buyers ÷ Clicked |
| ⑤ | Retention rate | Kept (not refunded) ÷ Paid buyers |

- **CVR** = Paid buyers ÷ Entered. **AOV** = GMV ÷ Paid orders. **Currency** ¥ (CNY). Counts are unique visitors (UV).
- **Benchmark group** = Brand × Platform × Type, over a rolling 90-day window, with a minimum of 20 sessions (below that: "Benchmark building").
- **Tiers** (quartiles of the benchmark): STAR ≥ P75 · GOOD P50–P75 · MID P25–P50 · WEAK < P25. A **session's tier** = the quartile of its CVR. Small samples show "Not enough data", never WEAK.
- Tier display: `Tag` positive (STAR), informative (GOOD), warning (MID), negative (WEAK), neutral (Not enough data / Building). In charts: Chart 6 Green, Chart 1 Blue, Chart 3 Amber, Chart 4 Pink, Chart 9 Slate.
- **Grades follow the filters:** every value is graded against the group the filters define. With Type = All, combined values are graded against the Brand × Platform × All types group and per-type rows against their own type. Only when there is no pooled All types group are combined values left untiered.

## 4b. Language: Chinese and English (foundation)

- The whole product is bilingual, 简体中文 and English, with the toggle **中文 | EN** in the top bar. Switching keeps the page, filters and open drawers.
- Translate every UI string: navigation, labels, metric names, tooltips, tier and tag names, Action Card copy, insight sentences, empty states and toasts. Use the fixed terms in `05-terminology-zh-en.md`.
- Don't translate platform data: host names and live topics stay as they are.
- **Numbers:** in 中文, use 万 / 亿 (124.4万, 1.24亿); in EN, use K / M (1.24M).
- **Dates:** 10月26日 21:00 in 中文, 26 Oct 21:00 in EN.
- **Layout:** size for the longer English strings. Chinese uses Noto Sans SC with the slightly taller CJK line height. Labels wrap, never truncate.

## 5. Screens

### 5.1 Session Analytics · Overview (landing, the Session Analytics sidebar item; APAC Dashboard template)

1. **Live performance** (section header). A row of 4 `DataMetric` compare cards: Sessions analyzed, CVR, Exposed rate, Product exposure rate. Each shows its change vs the previous 30 days, a definition in its tooltip, and on the rate cards a "P50 x%" footnote for the current group that opens the Benchmark drawer.
   Below it, a full-width card: **Session tier distribution**, a stacked horizontal bar of STAR/GOOD/MID/WEAK counts (one bar, graded against the group the filters define; Type = All uses the All types group), plus a "How tiers work" link. A segment opens Sessions filtered to that tier.
2. **Sales.** A row of 4 cards: Total GMV, Avg GMV / session, Paid orders, Avg AOV. Below it, a featured **Recoverable revenue** card ("+¥166K this period if every session reached the top-quartile CVR of its group"), with an ⓘ Popover explaining the method and "See sessions with most upside".
3. **Trends.** Two chart cards side by side:
   - **Funnel by stage, current vs previous**: grouped bars per stage rate ①–⑤, current Chart 1, previous Chart 9; a stage opens Live Funnel with it highlighted.
   - **GMV by time gate**: the last 7 gates at the chosen granularity (Day | Week | Month control in the card header) as bars, a dashed line for the same gates last year, and MoM and YoY in the card header.
4. **Channel type comparison** (only when Type = All and both types have sessions): Self-operated vs Influencer, built with the shared **Comparison panel** (5.8). Rows: the five step rates ① to ⑤ in % (no "per 1,000 entrants" re-basing). Outcome tiles: CVR, AOV, Avg GMV / session, the two values side by side, leader in bold. No tiers. One computed sentence names the biggest difference.
5. **Sessions** (section): 5 rows with a toggle Latest | Top GMV | Most upside, and "View all sessions". Each row ends with a "View details" icon button; the row or the button opens the Session drawer.

### 5.2 Session Analytics · Live Funnel (sidebar sub-item)

The aggregate of all sessions in the filters. It describes and diagnoses; actions are per session.

- **Funnel section:** **Funnel volume** only: a "Live exposure" start row, then ① to ⑤ as horizontal bars with UV passed, % of exposed and UV lost; the weakest stage is marked.
- **Summary section:** the **Summary strip** (CVR, AOV, GMV, refund rate, avg watch time, each with its P50 where one exists), then **Stage performance**.
- **Stage performance** (one table, also used in Session drawer › Summary and Host drawer › Funnel). Columns: **Stage** · **Rate** · **Below P50 ┊ P50 ┊ Above P50** · **Tier** · **UV lost** · **Next step**.
  - The gap column is a diverging bar of the rate's gap to its P50, relative to P50: a dashed P50 line in the middle, bar colour = tier, label = gap in % ("±0%" when level). One scale per table, capped at ±100% so an outlier does not flatten the other rows. The three header labels sit close together, centred on a bold "P50".
  - Hovering a bar shows the chart tooltip (rate, P25, P50, P75, gap to P50 in % and pp, tier); the bar and the Tier Tag open the Benchmark drawer.
  - **Next step** is one short play keyed to the tier. The weakest stage is highlighted with a "Weakest" tag.
  - **Type = All:** each stage row is followed by Self-operated and Influencer sub-rows, each with its own bar, tier, UV lost and next step against its own type group.

### 5.3 Session Analytics · Sessions (sidebar sub-item; APAC List page + DataTable)

- **Toolbar:** search ("Search date, host, live topic"), Tier and Weakest-stage selects, a Columns popover.
- **Columns:** Date · start time, Host, Type, Live topic, Duration, Exposed UV, CVR, GMV, AOV, Session tier, Weakest stage (①–⑤), Recoverable revenue. Stage-rate columns are hidden by default.
- Sorted newest first; 48px rows; sticky header; pagination (25 per page). Every row ends with a "View details" icon button, and truncated host names and topics show their full text in a Tooltip.
- A live session sits on top with a "Live now" tag and no tier.
- A row opens the **Session drawer**.

### 5.4 Session drawer (wide)

- **Header:** title (host) and meta line (date and time · duration · type · platform) on the left, only Close on the right. Under it the scope row (benchmark group link, session tier Tag), then the actions row (‹ Prev · Next ›), then a KPI strip: GMV, Orders, AOV, CVR, Refund rate, Recoverable.
- **Tabs:** **Action Cards** (default) | Summary. (Day 2: Risk Radar · Playbook.)
- **Action Cards:** one card per stage, in funnel order ① → ⑤, each with its severity label: Critical (WEAK), Action needed (MID), Watch (GOOD), Strong (STAR). Each card has:
  - a header: stage, rate, P50, P75, gap to P50, UV lost, tier;
  - three columns: **What happened** · **Before next session** · **Expected recovery** (extra buyers and ¥ if the stage reached P50, then P75).
  A top banner shows the session's recoverable revenue. Stages with "Not enough data" get one neutral card with no instructions.
- **"Copy actions for host briefing"** (secondary button) copies every graded card's actions as plain text: "Host briefing · {host} · {session ID} · {date time}", then "Before the next session:", then one numbered "{stage}: {actions}" line per card. It also opens a **"Copied for host briefing"** dialog: a status line, the copied text exactly as it will paste, an "{n} actions · {c} characters · plain text" line and a single **Done** button. If the clipboard is blocked, the status line says to select and copy the text by hand.
- **Summary:** Funnel volume and **Stage performance** only (same components as Live Funnel). Next step here is the first action of that stage's Action Card; the CVR row has none.

### 5.5 Benchmark drawer (480px, stacks on top)

Opens from any tier Tag, P50/P75 value, Stage performance gap bar, median line, tag, or the scope-line link. Sections:

1. **Your value:** the value, its tier, its percentile, a benchmark track and a histogram of the group's session values with the value marked.
2. **Calculation group:** brand, platform, type; window dates; sessions included / excluded; number of hosts; stage minimum.
3. **How it is calculated:** the formula, the percentile method and the tier rule.
4. **All results for this group:** a table of P25 / P50 / P75 for the 5 stages, CVR, AOV and exposure per session, with the focused metric highlighted.

A Building group shows "Benchmark building: 14 of 20 sessions" instead of tiers.

### 5.6 Host Analysis

- Same page header and filter bar as Session Analytics. Breadcrumb: "Host Analysis". Host-level grades follow the Type filter; quadrant tags and the influencer map stay on the influencer group.
- **Influencer map** (chart card): a scatter of influencers. X = avg exposure per session (log scale), Y = AOV. Dashed lines mark the group's P50s (each opens the Benchmark drawer). Bubble size = GMV, colour = tag, a ring = borderline, hollow = not enough data. With Type = Self-operated the map is replaced by a note. Quadrant labels:

  | | Low reach | High reach |
  |---|---|---|
  | **High AOV** | Premium Niche | Flagship |
  | **Low AOV** | Under Review | Traffic Engine |

- **Leaderboard** (section with **Compare hosts**, primary button, in its header on the right; it starts host comparison, 5.8). Columns:
  - #, Host (type · tag), Sessions, GMV (with GMV / session), AOV, **CVR** (a plain number like AOV: no tier colour or tier word), Exposure / session
  - Funnel band: ① to ⑤ as tier-coloured cells with the rate and tier word (Tooltip: rate, tier, P25 · P50 · P75, UV; click opens the Benchmark drawer)
  - Last live, then a "View details" icon button

  Toolbar: search, a Tag filter, a Rates/Counts toggle (it switches the ① to ⑤ cells only; CVR always shows the rate), Columns. Every numeric column sorts both ways. Every host is ranked; hosts with too little data are greyed.
- **Tags:** Flagship (Chart 5 Violet), Traffic Engine (Chart 2 Teal), Premium Niche (Chart 3 Amber), Under Review (Chart 9 Slate), each shown as an outline Badge with a colour dot. Self-operated hosts are not tagged ("—"). Each tag's Tooltip explains why, e.g. "AOV ¥297 vs P50 ¥275 · Exposure 30.5K vs P50 23.9K per session".
- A row opens the **Host drawer** (wide):
  - Header: title and meta line, only Close on the right; scope row (benchmark group, tag); actions row (Compare with…, Open in Session Analytics); then KPIs and tabs Summary | Funnel | Sessions.
  - Summary: KPIs vs P50, the tag with suggested plays (the "why" sits in the tag's Tooltip), and a GMV / CVR trend.
  - Funnel: funnel volume and **Stage performance** (same component as Live Funnel).
  - Sessions: the host's sessions; a row opens the Session drawer, with "← Back to host".

### 5.7 Settings (Admin only; APAC Detail/Settings template)

- **Layout:** a left section nav (240px): Users & access, Data connections, Benchmark rules, Audit log.
- **Users & access:**
  - A selectable DataTable: Name, Email, Role (Badge), Brands, Status (Tag), Source (Manual / Okta), Last active.
  - Bulk actions: Assign brands, Remove brands, Deactivate.
  - **Invite user** (primary button): a Dialog with Email, Name, Role (Operator / Admin), Brands (checkboxes).
  - Clicking a row opens an **Edit access** Drawer (480px). **Deactivate** asks for confirmation in a Dialog.
- **Roles:** every user is an Operator and sees only their assigned brands. Admins also see Settings.

### 5.8 Host comparison (2–4 hosts)

- **Selection mode:** clicking **Compare hosts** (Leaderboard header) adds a checkbox column to the leaderboard and makes map dots selectable; the button reads "Selecting hosts…" and a second click cancels. A sticky selection bar reads "2 of 4 selected · [host chips ✕] · Compare (2) · Cancel".
- **Limits:** minimum 2, maximum 4 hosts. At 4, the other checkboxes are disabled with the Tooltip "You can compare up to 4 hosts".
- **Comparison view:** a wide drawer titled "Compare hosts", with the meta line "Thorne × Douyin · Last 90 days · graded against All types (n=137)".
  - **+ Add host** (actions row) returns to selection mode with the current picks kept. It shows only while fewer than 4 hosts are compared and reappears when one is removed.
  - **Host chips:** colour swatch, name, type and sessions, ✕. Removing a host updates the panel; removing one of the last two ends the comparison and closes the drawer.
  - Under them, the **Comparison panel**:
    - **Funnel, side by side:** one row per step rate, ① Entry rate to ⑤ Retention rate in %. Each row has one bar per host in its series colour with the value, and a "Tier vs {group}" column (e.g. "Tier vs All types") with the tier as coloured text, graded against the group the filters define. A one-line note says bars compare the hosts while tiers grade against the group.
    - **Outcome tiles:** CVR, Avg AOV, Avg GMV / session, Total GMV, Avg exposure / session, Sessions. Each lists every host on its own row, with the leader in bold. No leader chips.
    - **GMV per week:** a line per host.
    - **Biggest differences:** 1–3 computed sentences.
- **Own-type grading** only when there is no pooled All types group: then each tier shows its type, e.g. "GOOD / Influencer".
- **Colours:** hosts in selection order are Chart 1 Blue, Chart 2 Teal, Chart 3 Amber, Chart 5 Violet.
- **Shared component:** the Comparison panel is the same component as the Overview channel comparison (2 series in type colours, values side by side). Its layout is channel-comparison **Option A** (paired funnel rows + outcome tiles + insight sentence). It must scale to 4 series; a two-sided head-to-head layout won't.

### 5.9 Tooltips, responsive and dark mode

- **Chart tooltip** on every chart element (bar, segment, point, track, gap bar, heat cell): the APAC chart tooltip card with a bold title, one row per value with its series swatch, and a short note on what it means (value + comparison + meaning). Column charts highlight the hovered column.
- **Standard tooltip** (dark pill, 300ms delay) on any table cell whose text is actually truncated, with the full text.
- Tooltips stay inside the viewport and hide on scroll. On touch screens the first tap shows the tooltip and the second tap acts.
- **Responsive:** desktop first (≥ 1280px), fully readable on tablet (1024) and mobile (390). Between md and lg the sidebar is a 64px icon rail with the Session Analytics views in a flyout. Below md the sidebar goes off-canvas (sub-items included), the condensed header shows the title and the "Filters (n)" button, the filter bar becomes a "Filters (n)" button that opens a Filters drawer (Apply / Reset), KPI cards go to 1 column, tables scroll inside their card with Host pinned, drawers go full width, the language toggle moves into the avatar menu and host comparison shows one step per card with scrolling host chips. See spec 11.
- **Dark mode:** Light / Dark in the avatar menu, using APAC dark tokens; charts keep the chart palette.

## 6. States to show

Compare limit reached (4) · Benchmark building (page and Benchmark drawer) · Platform not connected (disabled option, "Not connected") · Not enough data · No sessions match (`Empty` with the active filters named) · Loading (skeletons) · Live session · No brand access (full-page empty state) · Error with Retry · Copied for host briefing (dialog).

## 7. Data

Use **only** the attached `02-prototype-data.json` and `02-sessions-last-30-days.csv`. Do not invent numbers. Synthetic data, as of 27 Oct 2026; current period = last 30 days (28 Sep – 27 Oct 2026). JSON map:

| Need | JSON path |
|---|---|
| Brand switcher, platform connection status | `brands[]` |
| Overview numbers (current, previous, tiers, weekly GMV trend, MoM/YoY, channel comparison) | `overview["Thorne|douyin|All"]` (keys are `Brand|platform|Type`) |
| Live Funnel | `live_funnel["Brand|platform|Type"]` |
| Benchmarks for the scope line and drawer | `benchmarks["Brand|platform|Type"]` |
| Histogram values for the Benchmark drawer | `benchmark_distributions_thorne_douyin[type][metric]` |
| Sessions table | `02-sessions-last-30-days.csv` |
| Session drawer (Action Cards with benchmarks and recovery) | `featured_sessions.influencer_example` (S00234, LisaWang) and `featured_sessions.self_operated_example` (S00112) |
| Host leaderboard and map (90-day window) | `hosts_90d[]` |
| Host drawer | `host_drawer_example` (康姐的小管家) |
| Settings users | `users[]` |
| Host comparison (4 hosts, 90 days) | `host_comparison_example.hosts[]` |
| Chinese / English terms | `05-terminology-zh-en.md` |

Data notes:

- Thorne × Douyin influencer AOV is skewed by one host, LisaWang (AOV about ¥2,100). This is intentional and realistic.
- YoY is high because the synthetic influencer programme was smaller a year ago.
- Percentages in the data are fractions (0.1304 = 13.04%). Show rates to one or two decimals.
- Names are Chinese; render them with Noto Sans SC.

**Action Card copy:** write it from the stage, the tier and the numbers. Example: "Only 15.6% of room entrants saw a product, vs a P50 of 27.1% for Thorne × Douyin influencers." / "Pin the hero product within the first 5 minutes and re-pin every 10 minutes; brief the host to show the product card while talking about it." / "+17 buyers, about +¥36K, at P50."
