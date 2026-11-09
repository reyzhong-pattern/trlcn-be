# APAC Design System Skill

## When to use this skill
Invoke whenever the user asks you to design, implement, review, or generate UI for Pattern's internal tools and platforms. This skill ensures all output is consistent with the APAC design system.

---

## Design System Overview

**Brand:** Pattern (APAC internal tools + platform websites)
**Grid base:** 4px
**Theme:** Light + Dark mode (all tokens defined for both)
**Stack:** React + Tailwind CSS + shadcn/ui + Recharts

---

## FONTS

| Role | EN | CN | KR | JP |
|------|----|----|----|----|
| UI / body | Geist | Noto Sans SC | Noto Sans KR | Noto Sans JP |
| Monospace | Geist Mono | Geist Mono | Geist Mono | Geist Mono |
| Brand / display | Wix Madefor Display | Wix Madefor Display | Wix Madefor Display | Wix Madefor Display |

Font weights: `400` (regular) · `500` (medium) · `600` (semibold)

---

## TYPOGRAPHY SCALE

Format: `size / line-height` in px.

| Style | Size/LH | Font | Weight | Notes |
|-------|---------|------|--------|-------|
| title-lg | 72/84 | Wix Madefor Display | 600 | tracking: -0.5px |
| title-md | 60/72 | Wix Madefor Display | 600 | |
| title-sm | 48/56 | Wix Madefor Display | 600 | |
| heading-lg | 30/36 | Geist | 600 | |
| heading-md | 24/32 | Geist | 600 | |
| heading-sm | 20/28 | Geist | 600 | |
| heading-xs | 18/24 | Geist | 600 | |
| body-xl | 18/28 | Geist | 400 | |
| body-lg | 16/24 | Geist | 400 | |
| body-md | 14/24 | Geist | 400 | |
| body-sm | 12/18 | Geist | 400 | |
| body-xs | 11/12 | Geist | 400 | |
| label-lg | 16/20 | Geist | 500 | |
| label-md | 14/20 | Geist | 500 | |
| label-md-alt | 14/16 | Geist | 500 | tight |
| label-sm | 12/16 | Geist | 500 | |
| label-xs | 11/12 | Geist | 500 | |
| mono-md | 14/20 | Geist Mono | 400/600 | |
| mono-sm | 12/16 | Geist Mono | 400/600 | |
| metric-lg | 24/36 | Geist | 600 | KPI numbers |
| metric-md | 20/32 | Geist | 600 | |
| caption | 11/16 | Geist | 500 | UPPERCASE |

---

## COLOR TOKENS

### Brand
```
brand-primary:     #3A55FF
brand-near-black:  #090A0F
```

### Semantic — Light / Dark

**Background**
```
bg-page:          #FFFFFF  /  #090A0F
bg-subtle:        #FAFAFA  /  #090A0F
bg-muted:         #F5F5F5  /  #171717
bg-overlay:       rgba(0,0,0,0.6)  /  #000000
```

**Surface**
```
surface-base:            #FFFFFF  /  #0A0A0A
surface-raised:          #FFFFFF  /  #171717
surface-accent:          #F5F5F5  /  #262626
surface-sidebar:         #FAFAFA  /  #0A0A0A
surface-primary-subtle:  #E9EBFF  /  #10103D
```

**Text**
```
text-primary:      #0A0A0A  /  #FAFAFA
text-secondary:    #404040  /  #D4D4D4
text-tertiary:     #525252  /  #A3A3A3
text-disabled:     #A3A3A3  /  #737373
text-on-primary:   #FFFFFF  /  #FFFFFF
text-destructive:  #CC2B2B  /  #F87272
```

**General (interactive)**
```
general-primary:              #3A55FF  /  #3A55FF
general-primary-hover:        #3334AD  /  #666DFF
general-secondary:            #F5F5F5  /  #262626
general-secondary-hover:      #FAFAFA  /  #171717
general-ghost:                transparent
general-ghost-hover:          rgba(0,0,0,0.05)  /  rgba(255,255,255,0.08)
general-destructive:          #F04842  /  #A32222
general-destructive-fg:       #FFFFFF
general-destructive-border:   #CC2B2B  /  #F87272
general-destructive-subtle:   #FEF0F0  /  #4B0D0D
```

**Outline / Border**
```
outline-default:      #E5E5E5  /  #404040
outline-strong:       #A3A3A3  /  #737373
outline-focus:        rgba(58,85,255,0.5)  /  #4C4FFF
outline-focus-error:  #F9C4C4  /  #781818
outline-sidebar:      #E5E5E5  /  #262626
```

**State**
```
state-success:          #1AC773  /  #18A965
state-success-subtle:   #E6F9F0  /  #083F2C
state-warning:          #F97316  /  #EA580C
state-warning-subtle:   #FFF3E8  /  #431407
state-info:             #009BFF  /  #0087DF
state-info-subtle:      #E2F3FF  /  #002B47
state-destructive:      #F04842  /  #A32222
state-destructive-subtle: #FEF0F0  /  #4B0D0D
```

**Icon**
```
icon-default:  #404040  /  #E5E5E5
icon-muted:    #737373  /  #737373
icon-accent:   #3A55FF  /  #666DFF

(Branding collection — for use on colored/filled surfaces)
icon/reverse:  #FFFFFF  /  #ADE0FF  (White light · Blue/200 dark)
```

**Sidebar**
```
sidebar-fg:           #404040  /  #D4D4D4
sidebar-accent:       #F5F5F5  /  #171717
sidebar-accent-fg:    #171717  /  #F5F5F5
sidebar-primary:      #3A55FF  /  #FAFAFA
sidebar-primary-fg:   #FAFAFA  /  #171717
sidebar-ring:         #D4D4D4  /  #404040
```

### Primitive Scales (key stops)

**Neutral:** 50 `#FAFAFA` · 100 `#F5F5F5` · 200 `#E5E5E5` · 300 `#D4D4D4` · 400 `#A3A3A3` · 500 `#737373` · 600 `#525252` · 700 `#404040` · 800 `#262626` · 900 `#171717` · 950 `#0A0A0A`

**Red (destructive):** 50 `#FEF0F0` · 100 `#FCDCDC` · 200 `#F9C4C4` · 400 `#F87272` · 500 `#F04842` · 600 `#CC2B2B` · 700 `#A32222`

**Blue:** 200 `#ADE0FF` · 400 `#22B3FF` · 500 `#009BFF` · 600 `#0087DF`

**Indigo:** 300 `#949BFF` · 400 `#666DFF` · 500 `#4C4FFF` · 600 `#3F41D6` · 700 `#3334AD` · 950 `#10103D`

**Green:** 400 `#3FC88E` · 500 `#1AC773` · 600 `#18A965` · 950 `#083F2C`

**Orange:** 400 `#FB923C` · 500 `#F97316` · 600 `#EA580C`

**Yellow:** 400 `#FBBF24` · 500 `#FACC15` · 600 `#EAB308`

---

## SPACING

Base: **4px**. Tokens: `0`=2px · `1`=4px · `2`=8px · `3`=12px · `4`=16px · `5`=20px · `6`=24px · `8`=32px · `10`=40px · `12`=48px · `16`=64px · `20`=80px · `24`=96px

### Spacing Idioms

| Context | Token | px | Notes |
|---------|-------|----|-------|
| Card padding — compact | `spacing-3` | 12px | Dense dashboard cards, DataTable-adjacent panels |
| Card padding — default | `spacing-4` | 16px | Standard content cards |
| Card padding — featured | `spacing-6` | 24px | Metric/KPI cards, hero panels |
| Card grid gap | `spacing-4` | 16px | Gap between cards in a row/grid |
| Section gap | `spacing-6` | 24px | Vertical gap between major page sections |
| Form field vertical gap | `spacing-4` | 16px | Gap between stacked form fields |
| Label-to-input gap | `spacing-1` | 4px | Space between field label and its control |
| Inline element gap (icon + label) | `spacing-1` | 4px | Inside buttons, nav items, badges, breadcrumbs |
| Page horizontal padding | responsive | 24 / 32 / 40px | 24px at md · 32px at lg · 40px at xl |

---

## BORDER RADIUS

`radius-2`=2px · `radius-4`=4px · `radius-6`=6px · `radius-8`=8px · `radius-10`=10px · `radius-12`=12px · `radius-16`=16px · `radius-24`=24px · `radius-32`=32px · `radius-full`=999px

---

## SHADOWS

> Dark mode: shadows are invisible — use `outline-default` borders instead.

```
shadow-subtle:  0 1px 2px rgba(0,0,0,0.05)
shadow-card:    0 2px 4px rgba(0,0,0,0.10)
shadow-hover:   0 4px 12px rgba(0,0,0,0.10)
shadow-modal:   0 8px 24px rgba(0,0,0,0.10)
shadow-float:   0 16px 40px rgba(0,0,0,0.15)
shadow-brand:   0 4px 16px rgba(58,85,255,0.24)
ring-focus:     0 0 0 2px rgba(58,85,255,0.5)  (both modes)
ring-error:     0 0 0 3px #F9C4C4  (light)  /  0 0 0 3px #781818  (dark)
```

---

## CHART COLORS

10 data series. Charts 1–5 = Primary; 6–10 = Supporting.

| # | Light | Dark |
|---|-------|------|
| 1 Blue | `#4F72FF` | `#7A96FF` |
| 2 Teal | `#38BFA8` | `#5FD4BE` |
| 3 Amber | `#F59E42` | `#FBBC72` |
| 4 Pink | `#E05C7A` | `#F08EA5` |
| 5 Violet | `#8B6CF6` | `#A98FFF` |
| 6 Green | `#34C97E` | `#5FDDA0` |
| 7 Sky | `#60A5FA` | `#93BFFD` |
| 8 Salmon | `#FB8B6B` | `#FCAA90` |
| 9 Slate | `#94A3B8` | `#B8C5D3` |
| 10 Yellow | `#F0C35A` | `#F5D47E` |

Sequential: start Chart 1. Diverging: Chart 1 (positive pole) + Chart 4 (negative pole).

---

## Z-INDEX SCALE

**Rule:** the pinned shell (sidebar, top bar, pinned page header) always sits **below every overlay**. Every Drawer, Sheet and Dialog renders its own full-viewport overlay, so it covers the sidebar and top bar as well as the content. Nothing inside the page content may rise above the pinned shell.

| Layer | z-index | Elements |
|-------|---------|----------|
| Dropdown (in page) | 100 | Select dropdowns, Combobox menus, context menus and Popovers opened from page content |
| Sticky (in content) | 200 | Sticky table headers, sticky selection / bulk-action bars inside the content area |
| Pinned page header | 210 | Page header block pinned under the top bar (see *Pinned shell and condensing page header*) |
| Top bar | 220 | 48px top bar, pinned |
| Sidebar | 230 | Full-height sidebar, pinned (≥ md); includes the icon-rail flyout menu |
| Floating | 250 | Floating action buttons (FAB), floating AI query box |
| Drawer overlay / Drawer | 300 / 310 | Drawer/Sheet overlay and panel |
| Stacked drawer overlay / Drawer | 320 / 330 | A second drawer opened from inside a drawer (e.g. a standard drawer over a wide detail drawer); each level adds its own overlay |
| Modal | 400 | Dialog (standard + full-screen) and its overlay; the off-canvas sidebar drawer below md |
| Toast + Tooltip | 500 | Toast notifications, Tooltip, chart tooltip (always on top) |

**Notes:**
- **Stacking contexts:** a dropdown or Popover opened from *inside* a pinned layer (e.g. a filter Select in the pinned page header, the brand switcher in the sidebar) is positioned within that layer. It shows above page content and below every overlay. Do not portal it to a higher layer.
- **Sticky offsets:** sticky elements inside the content stick *below* the pinned shell: `top` = top bar (48px) + condensed page header (52px) + 16px gap, instead of `top: 0`.
- **Floating AI assistant:** a floating AI assistant that persists across the session uses z-index **250**. It appears above the pinned shell but dismisses naturally when a Drawer or Modal opens.

---

## PAGE TEMPLATES

Five standard templates. All assume the Page Shell as the outer frame: **sidebar spans full viewport height** (primary nav tier); top bar and content area sit in the column to the right of the sidebar.

### Shell outer structure (all templates)
```
[Sidebar 280px full-height] | [Content column fills remainder]
                               [Top bar 48px]
                               [Content area]
```
Breadcrumb in top bar always reflects: Active Sidebar Section → Page → Sub-page (where applicable). When a sidebar section has sub-items, see *Two-level side navigation* for the breadcrumb rule.

The sidebar, top bar and (on analytics and list pages) the page header block are pinned while the content scrolls. See *Pinned shell and condensing page header*.

### 1. Dashboard
- **Shell:** Sidebar full height (Overview active) · Top bar breadcrumb: "Overview / Dashboard"
- **Page header:** `heading-md` title (left) + optional one-line description (`body-sm` / `text-tertiary`, 2px below the title) + date range Select/DatePicker (right) · 24px bottom margin · pinned and condensing when the page has filters
- **Row 1 — Metric cards:** 4× Data Metric Card in a 4-column grid · `spacing-4` gap · card padding 24px (featured)
- **Row 2 — Charts:** 2× chart card in a 2-column grid · `spacing-4` gap · card padding 16px · each card: `label-lg` title top-left + chart below

### 2. List Page (DataTable)
- **Shell:** Sidebar full height (relevant section active, e.g. Orders) · Top bar breadcrumb: "Orders"
- **Page header:** `heading-md` title (left) + optional one-line description (`body-sm` / `text-tertiary`) + primary Button "Add [entity]" (right) · 24px bottom margin
- **Filter bar:** search Input + optional Select filters in a horizontal row · `outline-default` bottom border · 16px V padding · 24px bottom margin
- **DataTable:** full-width · column headers `label-md` · row height 48px default
- **Pagination:** right-aligned below table · `spacing-6` top margin

### 3. Detail / Settings Page
- **Shell:** Sidebar full height (parent section active, e.g. Partners) · Top bar breadcrumb: "Partners / Levi Strauss & Co. / Settings" — breadcrumb shows the drill-down path from sidebar
- **Layout:** two-column within content area · left column 240px (section nav) · right column fills remainder · `spacing-8` column gap
- **Left:** vertical section list · `label-md` nav items · `surface-accent` active fill
- **Right — Section:** `heading-sm` + `outline-default` divider below · 24px margin below divider · form fields at `spacing-4` gap · `label-md` labels · `spacing-1` label-to-input gap
- **Footer:** sticky or inline Save/Cancel buttons (primary + ghost) · `spacing-8` top margin

### 4. Form Page (Multi-step Wizard)
- **Container:** full-screen overlay covering the entire viewport including the sidebar · centered column max-width 600px
- **Step indicator:** horizontal step pills at top · active step uses `general-primary` · inactive `surface-accent` · `caption` step labels
- **Form content:** `heading-sm` step title · `body-md` description · fields at `spacing-4` gap
- **Footer actions:** Back (ghost) left + Next/Submit (primary) right · `outline-default` top border · 20px V padding

### 5. Drawer Detail Panel
- **Modal by default:** the drawer slides in from the right edge of the viewport over a full-viewport overlay (`bg-overlay`) that covers the sidebar, top bar and pinned page header. Focus is trapped inside the drawer and returns to the trigger (e.g. the table row) on close. Overlay click and Escape dismiss it.
- **Width:** 480px (default) · `surface-raised` bg · Light: `shadow-modal` · Dark: `outline-default` left border instead of shadow
- **Wide variant (detail panels with tabs):** 75% of the content column, min 720px, max 1080px; full width below md. One wide drawer at a time: opening another detail from inside it replaces its content and shows a "← Back to [previous]" link.
- **Stacked drawer:** a standard 480px drawer may open over a wide drawer (e.g. a definition or rubric panel). It adds its own overlay on top of the wide drawer (z-index 320 / 330). Never stack more than two.
- **Motion:** slide in `translateX(100%) → 0` over 280ms `cubic-bezier(0.22, 1, 0.36, 1)` while the overlay fades in over 200ms. Slide out over 200ms `cubic-bezier(0.4, 0, 1, 1)`, then unmount. With `prefers-reduced-motion`, fade only (120ms). Changing the drawer's content in place (Prev / Next, refocusing) does not replay the motion.
- **Header:** `heading-xs` entity title (left) + close IconButton (right) · `outline-default` bottom border · 16px V padding
- **Body:** scrollable · 24px padding · sections separated by `heading-sm` + divider
- **Footer (if editable):** Save (primary) + Cancel (ghost) · `outline-default` top border · 16px V padding · sticky at bottom
- **Exception (non-modal side panel):** only when the user must keep working in the page alongside the panel (e.g. side-by-side editing), the panel may open inside the content column without an overlay, with the sidebar left usable. Pass `modal={false}` and say so explicitly in the spec.

---

## PAGE SHELL

```
┌──────────┬──────────────────────────────────────┐
│          │  Top bar (48px, pinned)              │
│ Sidebar  │  breadcrumb · search · avatar        │
│ 280px    ├──────────────────────────────────────┤
│ full h   │  Page header (pinned · condenses)    │
│ pinned   ├──────────────────────────────────────┤
│          │  Content area                        │
│          │  H-pad 16/24/32/40px · top-pad 24px  │
│ (64px    │  max-width 1440px                    │
│ collapsed│                                      │
│)         │                                      │
└──────────┴──────────────────────────────────────┘
```

**Layout hierarchy:** Sidebar is the primary navigation tier and spans the full viewport height — it is structurally above the top bar. The top bar lives inside the content column (to the right of the sidebar). The breadcrumb in the top bar describes the path drilling down from the active sidebar section (e.g., Partners → Levi Strauss & Co. → Settings).

| Zone | Spec |
|------|------|
| Sidebar — expanded | 280px wide · full viewport height · `surface-sidebar` bg · `outline-sidebar` right border |
| Sidebar — collapsed | 64px wide · full viewport height · icon-only · same bg and border |
| Sidebar nav item | `label-md` 14/500 · 20px icon · 4px icon-label gap · 12px V padding · `sidebar-accent` fill on active · `sidebar-accent-fg` text color on active |
| Sidebar sub-item | See *Two-level side navigation* · 36px row · label aligned with the parent label · 1px `outline-default` guide line |
| Sidebar top | Brand logo/mark anchors the top-left of the entire layout |
| Top bar | 48px tall · sits inside content column (right of sidebar) · `surface-sidebar` bg · `outline-default` bottom border · H-pad matches content padding |
| Top bar — left | Breadcrumb (`body-sm` / `text-secondary`) — path drills down from active sidebar item |
| Top bar — right | Global search (optional, can be hidden) · user avatar |
| Page header block | Title (+ description), primary control, filter bar and scope line as one block · pinned under the top bar · condenses to one 52px row on scroll (see below) |
| Content area | `bg-page` bg · H-pad: 16px(<md)/24px(md)/32px(lg)/40px(xl) · top-pad: 24px · max-width 1440px |

**Responsive sidebar — three states:**

| Viewport | Sidebar state | Behavior |
|----------|--------------|----------|
| ≥ lg (1280px) | **280px expanded** | Default desktop state. User can manually collapse to 64px icon-only via a toggle. Sub-items show under their parent. |
| md–lg (768px–1280px) | **64px icon-only** | Auto-collapses. Labels hidden; icons centered. Item label shown in a Tooltip on hover. A parent with sub-items opens a flyout menu instead of a Tooltip. |
| < md (768px) | **Off-canvas drawer** | Sidebar hidden entirely. Hamburger icon appears in the top bar and opens the sidebar as a full-height Drawer overlay (z-index 400), with sub-items shown as in the expanded state. |

In all states ≥ md the sidebar is **pinned**: `position: sticky; top: 0; height: 100vh` (z-index 230), so navigation stays reachable at any scroll position.


### Two-level side navigation (module views as sub-items)

Use this when a sidebar module has a few sibling **views** of the same subject that share one context (the same filters, time range and scope). For example, *Orders* → Overview · Returns · Fulfilment. The views move out of an in-page tab row into the sidebar. That way they stay reachable at any scroll position, each view gets its own page header, URL and breadcrumb, and the page saves the height of a tab row.

**When to use it, and when not**

| Situation | Use |
|---|---|
| 2–4 sibling views of one module that share filters and context, each a full page | **Sub-items under the module** (this pattern) |
| Views that need different filters or different scope | Separate sidebar modules |
| Switching content inside a card, drawer or dialog | `Tabs` (`line` variant) |
| More than 4 views, or views several levels deep | Rethink the IA. Use a section nav inside the page (Detail / Settings template) rather than a third sidebar level |

**Model: the parent is the landing view.** The parent item is itself a page: the module's landing view, usually its Overview. Its sub-items are the other views. Clicking the parent always opens the landing view. There is no separate "Overview" sub-item in the expanded sidebar. The breadcrumb names only the module on the landing view and "Module / View" on a sub-item.

```
ANALYTICS
▣ Orders                ← parent = landing view (Overview); active fill when it is open
  │ Returns             ← sub-items: 36px rows, label aligned with the parent label
  │ Fulfilment  ◀ open  ← active sub-item: sidebar-accent fill, weight 600
◫ Customers
```

**Anatomy and specs**

| Element | Spec |
|---|---|
| Parent item | Standard nav item (44px: 12px V padding, 20px icon, `label-md`) |
| Sub-item list | Indented under the parent · 1px `outline-default` guide line on the left, aligned with the centre of the parent icon (22px from the item edge) · 2px gap between rows |
| Sub-item | 36px tall · `label-md` at weight 400 · `sidebar-fg` · text aligned with the parent label · 8px radius · no icon |
| Sub-item, active | `sidebar-accent` fill · `sidebar-accent-fg` · weight 600 · `aria-current="page"` |
| Parent, its own view open | Active nav item (`sidebar-accent` fill) · `aria-current="page"` |
| Parent, a sub-item open | Weight 600 · `text-primary` · **no fill** (one filled item per sidebar) |
| Group semantics | Sub-items in an element with `role="group"` and `aria-label` = parent label |

**Expanding and collapsing**
- **Default: always visible.** Sub-items are shown whenever the sidebar is expanded. This suits sidebars with one or two multi-view modules.
- **Optional collapse:** when a sidebar has several multi-view modules, a parent may get a 16px chevron (right, `icon-muted`) that collapses its sub-items. The module that contains the open view is always expanded and cannot be collapsed. Other modules remember their state per user. Clicking the parent label still navigates; only the chevron toggles. Use `defaultExpandedItemIds` / `expandedItemIds` on `Sidebar`.

**Icon rail (64px: md–lg, or collapsed by the user at ≥ lg)**
- Sub-items are hidden. The parent icon shows the **active fill whenever any of its views is open**.
- Hovering or focusing the parent opens a **flyout menu** to the right of the rail instead of the label Tooltip. The flyout has:
  - a heading with the module name (`label-sm` 12/600 `text-tertiary`);
  - one 36px row per view, *including* the landing view (e.g. "Overview");
  - the active view with the `sidebar-accent` fill.

  The panel uses `surface-raised`, an `outline-default` border, `shadow-float`, `radius-8`, 4px padding and a 200px minimum width. It is offset 10px from the rail, and that gap is part of the hover target so the pointer can cross it.
- The flyout stays inside the sidebar's layer (z-index 230) and is closed by Escape, by leaving it or by choosing a view. It does not open below md.

**Off-canvas (< md)**: the drawer shows the expanded layout, sub-items included. Choosing any item closes the drawer.

**Behaviour**
- Switching views keeps the module's filters, time range and scope, and opens the new view **at the top of the page**: scroll resets, and a condensed header expands again.
- Each view has its own URL, page title and description. The browser Back button returns to the previous view.
- Keyboard: Tab reaches the parent and each sub-item in order. In the rail, focusing the parent opens the flyout, Arrow keys move through it, and Enter navigates.

**Do / Don't**
- **Do** keep one filled item in the sidebar at any time.
- **Do** give every view its own page header title and a one-line description, so views are distinguishable without tabs.
- **Do** keep the views' filters identical. If one view needs a different filter, it is a different module.
- **Don't** add an in-page tab row that duplicates the sub-items.
- **Don't** nest a third level in the sidebar.
- **Don't** show a Tooltip and the flyout at the same time on the rail.

### Pinned shell and condensing page header

On analytics and list pages the user often scrolls far down and still needs the filters and navigation. The shell therefore stays in place, and the page header block shrinks instead of scrolling away.

**Pinned layers (≥ md):** sidebar (sticky, full height) · top bar (sticky, `top: 0`) · page header block (sticky, `top: 48px`). The z-indexes are 230 / 220 / 210 (see Z-INDEX SCALE).

**Page header block:** one block holding the title + optional one-line description (left), the primary control (time range or primary Button, right), the filter bar and the scope line. It uses a `bg-page` background that bleeds to the content edges (negative margins equal to the page padding), so content scrolls cleanly underneath.

**Condensed state**

| | Expanded (top of page) | Condensed (after scrolling) |
|---|---|---|
| Trigger | scrollTop < 8px | scrollTop > 28px (hysteresis avoids flicker) |
| Layout | Title + description / primary control on row 1; filter bar; scope line | One row, 52px tall: title · filter controls · primary control |
| Title | `heading-md` | 16/24, weight 600, no wrap |
| Filter controls | 36px, with visible labels | 32px (segmented items 28px); labels visually hidden but kept for screen readers |
| Description, scope line | Shown | Hidden |
| Edge | Filter bar bottom border | `outline-default` bottom border + soft shadow `0 6px 12px -10px rgba(0,0,0,0.28)` |

- **No content jump:** the block keeps its expanded height in the page flow. When condensed, its bottom margin grows by (expanded height − 52px), so the content below never moves.
- Dropdowns and Popovers of the filter controls open from the condensed row, 38px below its controls.
- **Responsive:** below lg the condensed primary control drops its secondary text (e.g. the date span of a time range). Below md the expanded block stacks (title, primary control at full width, "Filters (n)" button, scope line), and the condensed row shows the title and the "Filters (n)" button only.
- Pages without filters (e.g. Settings) keep a plain, non-pinned page header.
- Opening a Drawer or Dialog never changes the header state. The overlay simply covers it.

---

## BREAKPOINTS & LAYOUT CONSTRAINTS

| Breakpoint | Min-width | Description |
|------------|-----------|-------------|
| `sm` | 640px | Mobile landscape / small tablet |
| `md` | 768px | Tablet portrait |
| `lg` | 1280px | Desktop (primary target) |
| `xl` | 1440px | Wide desktop |

**Content max-width:** 1440px, centered. Content fills full width below 1440px.
**Page horizontal padding:** 16px below `md` · 24px at `md` · 32px at `lg` · 40px at `xl` (the top bar uses the same horizontal padding)

### Responsive UI Rules

#### Sidebar (three-state)
| Viewport | State | Detail |
|----------|-------|--------|
| ≥ lg (1280px) | 280px expanded, pinned | User-toggleable to 64px icon-only; sub-items under their parent |
| md–lg (768px–1280px) | 64px icon-only (auto), pinned | Labels hidden; icon Tooltip on hover; a parent with sub-items opens a flyout of its views and shows the active fill when any of them is open |
| < md (768px) | Off-canvas | Hamburger in top bar → full-height Drawer overlay; sub-items shown as when expanded |

#### Page header action button
Every page template has a header row: `heading-md` page title (left) + primary action Button (right).

| Viewport | Layout |
|----------|--------|
| ≥ md (768px) | Horizontal flex row — title left, button right (`whitespace-nowrap` on button) |
| < md (768px) | Vertical stack — title on top, button below at full width (`w-full`) |

Apply `flex-col gap-3` on the header container at `< md`; `flex-row items-center justify-between` at `≥ md`.

#### Pinned page header block
| Viewport | Expanded | Condensed |
|----------|----------|-----------|
| ≥ lg (1280px) | Title + description left, primary control right; filter bar in one row; scope line | One 52px row: title · filters · primary control |
| md–lg | Same; the filter bar may wrap to two rows | Same; primary control drops secondary text |
| < md | Stacked: title, primary control full width, "Filters (n)" button, scope line | Title + "Filters (n)" button |

---

## TYPOGRAPHY PLACEMENT RULES

| Context | Style | Size / Weight |
|---------|-------|---------------|
| Page title (top of page) | `heading-md` | 24px / 600 |
| Section header (within page/panel) | `heading-sm` + divider line below | 20px / 600 |
| Modal / Drawer title | `heading-sm` | 20px / 600 |
| Card / panel title | `label-lg` | 16px / 500 |
| Table column header | `label-md` | 14px / 500 |
| Sidebar nav item (inactive) | `label-md` | 14px / 500 |
| Sidebar nav item (active) | `label-md` | 14px / 500 · `sidebar-accent-fg` color |
| Body / paragraph text | `body-md` | 14px / 400 |
| Secondary / supporting text | `body-sm` | 12px / 400 — `text-secondary` color |
| Field labels | `label-md` | 14px / 500 |
| Metric / KPI numbers | `metric-lg` or `metric-md` | 24px or 20px / 600 |
| Captions, timestamp, meta | `body-sm` or `caption` | 12px / 400–500 — `text-tertiary` color |

---

## OVERLAY & FEEDBACK DECISION TREE

### Overlay pattern

| Pattern | When to use |
|---------|-------------|
| **Tooltip** | Read-only labels and definitions only. Hover-triggered. No interactive content inside. |
| **Popover** | Contextual detail panels, mini-forms, contextual menus. Click-triggered. |
| **Dialog — Standard** | Destructive confirms + short forms (≤5 fields). Blocks the page. |
| **Drawer / Sheet** | Long forms (>5 fields) and detail/edit panels. Modal by default (overlay covers the sidebar and top bar); the page stays visible behind the overlay for context. |
| **Dialog — Full-screen** | New tasks that involve multi-step forms or wizards. Replaces the entire viewport. |

### Feedback pattern

| Pattern | When to fire |
|---------|-------------|
| **Toast** | Async background results: save success, export complete, clipboard copy. 4s auto-dismiss; errors persist. |
| **Inline validation** | Form field errors shown on blur; live-correct after first blur. |
| **Dialog confirm** | Before destructive or irreversible actions (delete, revoke, bulk remove). |

---

## INTERACTION RULES

| Rule | Value |
|------|-------|
| Transition duration | 150ms |
| Easing | ease-out |
| Enter/exit animation | fade + scale (0.95→1.0) |
| Focus rings | `:focus-visible` only (keyboard nav) |
| Disabled | `opacity: 0.5`, `cursor: not-allowed`, `pointer-events: none` |
| Active/pressed | One step darker fill than hover |
| Table row hover | `bg-subtle` background only |
| Toast position | Top-right; 4s auto-dismiss; errors persist |
| Tooltip delay | 300ms in, instant out |
| Tooltip appearance | Always dark pill — `#171717` bg + `#FAFAFA` text in both light and dark mode (never inverts) |
| Sidebar active | Filled `sidebar-accent` chip — exactly one filled item at a time |
| Sidebar parent with an open sub-item | Weight 600, `text-primary`, no fill; on the icon rail the parent icon takes the fill |
| Sidebar flyout (icon rail) | Opens on hover or focus of a parent with sub-items; 10px hover bridge; Escape closes |
| View switch (sidebar sub-items) | Keeps filters; scrolls to top; condensed header expands |
| Pinned page header | Condense after 28px of scroll, expand below 8px; keeps its flow height (no content jump) |
| Drawer motion | Slide in 280ms `cubic-bezier(0.22,1,0.36,1)` + overlay fade 200ms; slide out 200ms `cubic-bezier(0.4,0,1,1)`; reduced motion: fade 120ms |
| Modal overlays | Drawers and Dialogs cover the whole viewport, the pinned sidebar and top bar included |
| Page loading | Skeleton screens (no full-page spinners) |
| Form validation | On blur; live correction after first blur |
| Button loading | Spinner replaces icon+label; button stays same size in disabled state |
| Chart tooltip | Recharts crosshair + tooltip card; all series at X position |

---

## COMPONENT LIBRARY

### Defined in APAC Figma (use these specs verbatim)

| Component | Variants | Sizes | States |
|-----------|----------|-------|--------|
| **Button** | Primary · Secondary · Outline · Ghost · Destructive | Mini · Small · Default · Large | Default · Hover&Active · Focus · Disabled |
| **Icon Button** | Primary · Secondary · Outline · Ghost · Destructive | Mini · Small · Default · Large | Default · Hover&Active · Focus · Disabled |
| **Badge** | Primary · Secondary · Outline · Ghost · Destructive | Mini · Small · Default · Large | Default · Focus |
| **Checkbox** | Bare · Group · Rich Group | — | Default · Focus · Error · Disabled |
| **Radio** | Bare · Group · Rich Group | — | Default · Focus · Error · Disabled |
| **Input** | Default · Round | Mini · Small · Regular · Large | Empty · Value · Focus · Error · Disabled |
| **Textarea** | Default · Round | — | Empty · Value · Focus · Error · Disabled |
| **Input Field** | Text · Select · Radio · Textarea · Checkbox | — | Layout: Vertical / Horizontal |
| **Select / Combobox** | Select · Combobox | Mini · Small · Regular · Large · Fit | Default · Hover · Focus · Error · Disabled |
| **Tabs** | Cell · Group · Counter | Small · Regular · Large | Inactive · Active · Hover · Disabled |
| **Breadcrumb** | — | — | Default · Hover · Active per item |
| **Progress** | Bar · Labeled | — | Value 0–100% |
| **Tooltip** | Top · Bottom · Left · Right | — | Open |
| **Dialog** | Standard · Alert | Small · Medium · Large | — |
| **Date Picker** | Single · Range · Free Type | — | Calendar day: Today · Selected · Range · Hover |
| **Empty State** | Default · Dotted · Background · Dotted+BG | — | — |
| **Data Table** | — | — | Cell: Default · Hover · Active · Disabled |
| **Data Metric Card** | Change Index · Progress Bar footer | — | Positive · Negative · Neutral delta |
| **Charts** | Line · Area · Bar · Horizontal Bar · Pie · Donut · Radar | — | Recharts-based |

### Storybook-Confirmed Components (in code, not yet in Figma)

These components exist in `@patterninc/apac-ui` and are documented in the live Storybook, but do not yet have Figma specs. Use the details below when implementing or reviewing them.

| Component | Description | Props / Variants | Stories |
|-----------|-------------|------------------|---------|
| **Popover** | Displays rich content in a portal, triggered by a button or other element. | Supports `align`: start · end · center | Default · Align Start · Align End |
| **Skeleton** | Loading placeholder that mimics the shape of content before it renders. Compose multiple elements for complex layouts. | `shape`: `rectangular` (default) · `circular` · `text`; `className` for sizing | Default (rect) · Circular · Text · Card Placeholder (composite) |
| **Drawer** | Side panel overlay; prop-driven or compound API. | `side`: right (default) · left; `footerLayout`; `modal`; `dismissible` | Default · Form Example · Sides · Scrollable Content · Compound · Non Dismissible · Non Modal |
| **Pagination** | Page navigation with optional summary + page-size selector. | `totalItems`*; controlled/uncontrolled `page`/`pageSize`; `labels` for localisation | Default · Controlled · Uncontrolled · Compact · Empty · Disabled · Localized · Responsive · Compound |
| **ScrollArea** | Styled scroll container. | `type`; vertical · horizontal · both axes | Default · On Scroll · Automatic · Horizontal · Both Axes · Always Visible |
| **Sidebar** | App navigation shell. | `variant`: sidebar · floating · inset; `collapsible`: icon · offcanvas · none; `side` | Default · Floating · Inset · Right Side · Offcanvas · Non Collapsible · Controlled · Mobile · Compound · Menu Primitives |
| **Stepper** | Multi-step progress indicator. | `content`: title · compact · description; `currentStep` | Default · Compact · With Titles · With Descriptions · All Completed · Design States · Mobile · Narrow Container · Primitives |
| **Switch** | On/off toggle. | `size`: default · sm | Default · Sizes · States · Controlled · With Field |
| **Tag** | Semantic status label. | `variant`: neutral · positive · negative · warning · informative | Default · Positive · Warning · Informative · Negative · Variants · Responsive |
| **Toaster** | Sonner-based toast notifications. | `toast()` + `.success/.info/.warning/.error/.loading/.promise`; `action` | Default · Types · With Description · With Action · Promise Toast · With Close Button |
| **Table** | Base composable table primitives: `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell`, `TableFooter`, `TableCaption`. **Distinct from DataTable** — Table is layout-only; DataTable adds config-driven columns, built-in checkbox selection, and sorting. | — | Default · Sortable Headers · With Selectable Rows · Loading (uses Skeleton cells) |

Progress and Data Metric Card (Figma-defined above) now also have Storybook APIs — see `Progress` and `DataMetric` in the Component API Reference.

**Usage notes:**
- **Popover**: `radius-12` + `surface-raised` background. Light mode: `shadow-float`. Dark mode: `outline-default` border instead of shadow. Fade+scale entrance (150ms). Dismiss on outside click.
- **Skeleton**: animate with a subtle shimmer (pulse). Base color: `surface-accent` (#F5F5F5 light / #262626 dark). Shimmer highlight: `surface-base` (#FFFFFF light / #171717 dark). Match shape to the content being replaced — `rectangular` for cards/blocks, `text` for lines of text, `circular` for avatars.
- **Table**: use `Table` (base) when you need manual composition. Use `DataTable` when you need column config, sorting, or row selection out of the box. The Loading story pattern: render Table with Skeleton cells instead of real data.

---

### Not yet in APAC Figma → use shadcn/ui base + APAC tokens

For components not listed above (Avatar, Navigation bar, Accordion, Command palette, Spinner, etc.):

1. **Start from the shadcn/ui component spec** for structure, anatomy, and accessibility.
2. **Apply APAC tokens** — replace all shadcn defaults:
   - Primary color → `#3A55FF`
   - Background → `bg-page` / `surface-base`
   - Text → `text-primary` / `text-secondary`
   - Border → `outline-default`
   - Radius → match the component type (inputs: `radius-8`, cards: `radius-12`, full pills: `radius-full`)
   - Shadows → use the elevation scale (`shadow-card` for cards, `shadow-modal` for overlays)
   - Font → Geist (EN), `label-md` for UI controls, `body-md` for body text
3. **Apply APAC motion rules** (150ms ease-out, fade+scale for overlays).
4. **Apply APAC interaction rules** (focus-visible rings, disabled opacity, ghost hover).

---

## ICONS

Style: outlined stroke (Lucide-style).

### Icon Sizes

| Size | px | Use |
|------|----|-----|
| Micro | 12px | Inside badges, tags, compact chips |
| Inline | 16px | Inline with body text, table cells, dense UI |
| UI | 20px | Buttons, nav items, form controls, tooltips |
| Page | 24px | Navigation anchors, empty-state illustrations, page-level actions |

### Icon Color Rules

| Context | Color |
|---------|-------|
| Default UI | `icon-default` (#404040 light / #E5E5E5 dark) |
| Interactive / branded | `icon-accent` (#3A55FF light / #666DFF dark) |
| On any filled / colored surface | `icon/reverse` — #FFFFFF light · #ADE0FF (Blue/200) dark |
| Muted / secondary | `icon-muted` (#737373) |

---

## DESIGN DECISIONS

- Shadows are invisible in dark mode — rely on `outline-default` borders for elevation signaling.
- Hover and Active are the same visual state; Active adds one darker fill step.
- The Neutral scale is the primary gray scale. Indigo (not Blue) maps to the brand interactive color.
- The `brand-primary` (`#3A55FF`) maps to Indigo-500 in the primitive scale.
- CJK line heights are ~4px taller than EN equivalents.
- Chart colors are categorical, not semantic — always use the chart palette for data series, never state colors.
- The `metric-*` type styles are reserved for KPI numbers in dashboard cards.
- The navigation shell (sidebar, top bar, pinned page header) is pinned and always sits below overlays. A module's sibling views are sidebar sub-items, not page tabs (since 2026-11).
- Drawers are modal by default and cover the sidebar. This replaces the earlier rule that a drawer opens inside the content column with the sidebar usable.

---

## COMPONENT API REFERENCE

> Source of truth: [Storybook](https://doc-apac-ui.patternasia.com.cn) — package `@patterninc/apac-ui`
> Last synced: 2026-10-28 (v1.3)
> Components are listed alphabetically. Props marked `*` are required.

---

### Badge

```tsx
import { Badge } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `variant` | `"primary" \| "secondary" \| "ghost" \| "destructive" \| "outline"` | `"primary"` | Visual style |
| `children` | `ReactNode` | — | Badge label/content |
| `asChild` | `boolean` | `false` | Renders as Radix Slot — merges props onto child element |

---

### Breadcrumbs

```tsx
import { Breadcrumbs } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `items` * | `BreadcrumbItemData[]` | — | Each item: `{ label: string; href?: string }` |
| `separator` | `ReactNode` | `/` | Custom separator between items |

---

### Button

```tsx
import { Button } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `variant` | `"default" \| "outline" \| "secondary" \| "ghost" \| "destructive" \| "link"` | `"default"` | Visual style |
| `size` | `"default" \| "xs" \| "sm" \| "lg" \| "xl" \| "icon" \| "icon-xs" \| "icon-sm" \| "icon-lg"` | `"default"` | `icon-*` sizes for icon-only buttons |
| `rounded` | `boolean` | `false` | Fully rounded (`rounded-full`) |
| `asChild` | `boolean` | `false` | Renders as Radix Slot |
| `disabled` | `boolean` | `false` | Non-interactive + visually dimmed |
| `className` | `string` | — | Additional class names |

---

### Calendar

```tsx
import { Calendar } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `mode` | `string` | — | Calendar selection mode |
| `numberOfMonths` | `number` | `1` | Number of months to display |

**Note:** `Calendar` is a low-level primitive; prefer `DatePicker` for form usage.

---

### Checkbox

```tsx
import { Checkbox } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `label` | `ReactNode` | — | Label rendered alongside the checkbox |
| `checked` | `boolean` | — | Controlled checked state |
| `onCheckedChange` | `(checked: boolean) => void` | — | Fired on toggle |
| `card` | `boolean` | `false` | Wraps in a card-style container |
| `flipped` | `boolean` | `false` | Places checkbox indicator on the right (card mode) |
| `hasError` | `boolean` | `false` | Error state |
| `disabled` | `boolean` | `false` | Non-interactive |
| `asChild` | `boolean` | `false` | Renders as Radix Slot |

---

### DataMetric

```tsx
import { DataMetric } from "@patterninc/apac-ui"
// DataMetricStateContent = { title; description?; ... } — used by emptyState / errorState
```

KPI card for dashboards (Figma: **Data Metric Card**). Props depend on `variant` and `status`: Storybook marks all of the starred props as required because they belong to different variants.

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `variant` * | `"compare" \| "progress"` | — | `compare` = change index footer · `progress` = progress-bar footer |
| `title` * | `ReactNode` | — | Metric title at the top of the card |
| `category` | `ReactNode` | — | Optional category below the title |
| `tooltip` | `ReactNode` | — | Rich tooltip content beside the title |
| `tooltipAriaLabel` | `string` | — | Localized accessible name for the tooltip trigger |
| `prefix` | `ReactNode` | — | Content before the value (e.g. `"¥"`) |
| `value` * | `ReactNode` | — | Display-ready primary value |
| `suffix` | `ReactNode` | — | Content after the value (e.g. `"Rmb"`) |
| `change` * (compare) | `ReactNode` | — | Display-ready change incl. sign/unit (e.g. `"-14.7%"`) |
| `comparisonLabel` * (compare) | `ReactNode` | — | Localized context, e.g. `"vs last month"` |
| `sentiment` * (compare) | `"positive" \| "negative" \| "neutral"` | — | Business meaning of the change, independent of numeric direction |
| `progress` * (progress) | `number` | — | Percentage used to size the bar |
| `progressLabel` * (progress) | `ReactNode` | — | Localized label below the bar |
| `progressValue` | `string` | — | Display override; defaults to the un-clamped progress value |
| `status` | `"ready" \| "loading" \| "empty" \| "error"` | — | Card state |
| `emptyState` * (status empty) | `DataMetricStateContent` | — | Content when `status="empty"` |
| `errorState` * (status error) | `DataMetricStateContent` | — | Content when `status="error"` |
| `className` | `string` | — | Additional class names |

Use `metric-*` type tokens for the value (see Design Decisions).

---

### DataTable

```tsx
import { DataTable } from "@patterninc/apac-ui"
// Column type: DataTableColumn<TData> = { header: string; accessorKey?: keyof TData; cell?: (row: TData, index: number) => ReactNode; align?: "left" | "center" | "right"; sortable?: boolean; width?: string | number }
// Sort type: DataTableSortState = { columnId: string; direction: "asc" | "desc" } | null
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `columns` * | `DataTableColumn<TData>[]` | — | Column config: `header`, `accessorKey` or `cell` renderer, optional `align`, `sortable`, `width` |
| `data` * | `TData[]` | — | Row data array |
| `getRowId` | `(row: TData, index: number) => string` | row index | Supply when rows can be reordered/filtered for stable selection |
| `selectable` | `boolean` | `false` | Adds checkbox column and enables row selection |
| `selectedRowIds` | `string[]` | — | Controlled selection |
| `defaultSelectedRowIds` | `string[]` | `[]` | Uncontrolled default selection |
| `onSelectedRowIdsChange` | `(ids: string[]) => void` | — | Fired when selection changes |
| `isRowSelectable` | `(row: TData) => boolean` | always true | Per-row selectability |
| `sort` | `DataTableSortState` | `null` | Controlled sort — DataTable does NOT sort rows itself; sort data externally |
| `onSortChange` | `(sort: DataTableSortState) => void` | — | Fired when a sortable column header is clicked |
| `onRowClick` | `(row: TData, index: number) => void` | — | Fired on row click |
| `rowClassName` | `string \| (row: TData, index: number) => string` | — | Additional class per row |
| `emptyState` | `ReactNode` | `"No results."` | Shown when data is empty |
| `loading` | `boolean` | `false` | Shows skeleton rows |
| `loadingRowCount` | `number` | `5` | Number of skeleton rows when loading |
| `pagination` | `object` | — | Controlled external pagination config (see `Pagination`). `data` must contain only the current page |
| `containerClassName` | `string` | — | Additional class for the wrapper rendered when pagination is enabled |
| `error` | `boolean` | `false` | Replaces body rows with `errorState`. `loading` takes precedence over `error` |
| `errorState` | `{ title; description?; icon?; moreContent? }` | — | Structured error content. Required when `error` is true |
| `className` | `string` | — | Additional class for the table element |

---

### DatePicker

```tsx
import { DatePicker } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `isRange` | `boolean` | `false` | Date-range mode; `value` becomes `DateRange` |
| `value` | `Date \| DateRange` | — | Controlled value |
| `onChange` | `(value: Date \| DateRange) => void` | — | Fired on date selection |
| `placeholder` | `string` | — | Trigger placeholder text |
| `dateFormat` | `string` | — | date-fns format string (e.g. `"dd/MM/yyyy"`) |
| `showTime` | `boolean` | `false` | Shows time picker alongside calendar |
| `timeValue` | `string` | — | Controlled time value (when `showTime` true) |
| `onTimeChange` | `(time: string) => void` | — | Fired on time change |
| `disabled` | `boolean` | `false` | Disables the picker |
| `calendarProps` | `Omit<DayPickerProps, "onSelect" \| "selected" \| "mode">` | — | Passed through to the underlying `Calendar` |
| `align` | `"start" \| "center" \| "end"` | — | Alignment of the popover content |
| `className` | `string` | — | Additional class names |

---

### Dialog

```tsx
import { Dialog } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `trigger` | `ReactNode` | — | Element that opens the dialog when clicked |
| `title` | `ReactNode` | — | Dialog header title |
| `description` | `ReactNode` | — | Text below the title |
| `footer` | `ReactNode` | — | Footer slot — usually action Buttons |
| `children` | `ReactNode` | — | Main body content |
| `size` | `"default" \| "sm" \| "lg" \| "full"` | `"default"` | Max-width on larger viewports; `full` fills the viewport |
| `open` | `boolean` | — | Controlled open state |
| `defaultOpen` | `boolean` | — | Uncontrolled default open state |
| `onOpenChange` | `(open: boolean) => void` | — | Fired on open state change |
| `showCloseButton` | `boolean` | `false` | Whether to render the built-in close ✕ button. **Changed in v1.3** — Storybook now reports `false` (was `true`); confirm in code before relying on it |
| `closeButtonVariant` | `"button" \| "icon"` | `"icon"` | Style of the header close button |
| `footerLayout` | `"end" \| "full-width"` | `"end"` | Footer action layout |
| `fullScreenOnMobile` | `boolean` | `false` | Dialog fills the whole viewport on mobile |
| `accessibleTitle` | `string` | `"Dialog"` | Visually hidden screen-reader name used when `title` is omitted |
| `className` | `string` | — | Additional class for the dialog content |

Use `DialogClose` (with `asChild`) to wrap a Cancel button in the footer.

---

### Drawer

```tsx
import { Drawer } from "@patterninc/apac-ui"
// Compound API (as used in Storybook): DrawerContainer, DrawerTrigger, DrawerContent, DrawerHeader, DrawerTitle, DrawerBody, DrawerFooter
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `trigger` | `ReactNode` | — | Element that opens the drawer |
| `title` | `ReactNode` | — | Header title |
| `accessibleTitle` | `string` | `"Drawer"` | Screen-reader name used when `title` is omitted |
| `description` | `ReactNode` | — | Text at the top of the body |
| `children` | `ReactNode` | — | Body content; scrolls when it exceeds the viewport |
| `footer` | `ReactNode` | — | Footer slot — usually action Buttons |
| `footerLayout` | `"end" \| "full-width"` | `"end"` | Footer action layout |
| `side` | `"right" \| "left"` | `"right"` | Edge the drawer enters from |
| `showCloseButton` | `boolean` | `true` | Render the close ✕ button |
| `open` | `boolean` | — | Controlled open state |
| `defaultOpen` | `boolean` | — | Uncontrolled default open state |
| `onOpenChange` | `(open: boolean) => void` | — | Fired on open state change |
| `modal` | `boolean` | — | Block focus/interaction outside the drawer |
| `dismissible` | `boolean` | `true` | Overlay click / Escape can dismiss |
| `className` | `string` | — | Additional class for the drawer content |

Follow the Drawer Detail Panel template: modal by default (`modal` true, the overlay covers the sidebar and top bar), 480px or the wide variant, with the motion rules there. Use `modal={false}` only for the documented non-modal side-panel exception. Note `showCloseButton` defaults to `true` here but `false` on Dialog.

---

### Empty (Empty State)

```tsx
import { Empty } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title` | `string` | — | Heading of the empty state |
| `description` | `ReactNode` | — | Supporting text below the title |
| `icon` | `ReactNode` | — | Icon to display above the title |
| `moreContent` | `ReactNode` | — | Additional content below description (e.g. action buttons) |
| `variant` | `"default" \| "outline" \| "background" \| "outline-dashed"` | `"default"` | Visual container style |

---

### Field

```tsx
import { Field } from "@patterninc/apac-ui"
// Wraps any input control (Input, Select, Textarea, Checkbox, Radio) with label, helper text, and error.
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `label` | `string` | — | Label text displayed above the input |
| `helperText` | `string` | — | Helper text below the input |
| `error` | `string` | — | Error message below the input (replaces helperText) |
| `required` | `boolean` | `false` | Adds required indicator to label |
| `disabled` | `boolean` | `false` | Passes disabled state to child control |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | Layout direction of label + control |
| `children` | `ReactNode` | — | The form control (Input, Select, etc.) |

---

### IconButton

```tsx
import { IconButton } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `icon` | `ReactNode` | — | Icon element to display (e.g. `<PlusIcon />`) |
| `aria-label` | `string` | — | Required for accessibility |
| `variant` | `"default" \| "outline" \| "secondary" \| "ghost" \| "destructive"` | `"default"` | Visual style |
| `size` | `"default" \| "lg" \| "sm" \| "xs"` | `"default"` | Button dimensions |
| `rounded` | `boolean` | `false` | Fully rounded (`rounded-full`) |
| `asChild` | `boolean` | `false` | Renders as Radix Slot |
| `disabled` | `boolean` | `false` | Non-interactive + visually dimmed |

---

### Input

```tsx
import { Input } from "@patterninc/apac-ui"
// Extend with <Field> for label, helperText, and error.
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `placeholder` | `string` | — | Placeholder text |
| `variant` | `"default" \| "rounded"` | `"default"` | Visual style |
| `type` | `"text" \| "password" \| "email" \| "number" \| "search" \| "tel" \| "url"` | `"text"` | HTML input type |
| `disabled` | `boolean` | `false` | Non-interactive |

Native `<input>` props (`value`, `onChange`, `name`, etc.) are forwarded.

---

### Pagination

```tsx
import { Pagination } from "@patterninc/apac-ui"
// Compound API (as used in Storybook): PaginationContainer, PaginationContent, PaginationItem, PaginationLink, PaginationButton, PaginationPrevious, PaginationNext, PaginationEllipsis
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `totalItems` * | `number` | — | Total records across all pages |
| `page` | `number` | — | Controlled current page |
| `pageSize` | `number` | — | Controlled page size |
| `defaultPage` | `number` | — | Uncontrolled initial page |
| `defaultPageSize` | `number` | — | Uncontrolled initial page size |
| `onPaginationChange` | `(pagination: PaginationState) => void` | — | Called with the complete next pagination state |
| `pageSizeOptions` | `number[]` | `[10, 20, 50, 100]` | Selectable page sizes |
| `boundaryCount` | `number` | — | Always-visible pages at each end |
| `siblingCount` | `number` | — | Pages shown each side of the current page |
| `showSummary` | `boolean` | — | Item-range summary (hidden on mobile / small containers) |
| `showPageSize` | `boolean` | — | Page-size selector (hidden on mobile / small containers) |
| `showFirstLast` | `boolean` | — | First/last controls on desktop |
| `showPageNumbers` | `boolean` | — | Numbered page controls on desktop |
| `disabled` | `boolean` | — | Disables every control |
| `labels` | `Partial<PaginationLabels>` | — | Override built-in English labels (use for CJK localisation) |
| `renderSummary` | `(details: PaginationSummaryDetails) => ReactNode` | — | Custom item-range summary |

List pages: right-aligned below the DataTable. For DataTable-integrated paging use DataTable's `pagination` prop.

---

### Popover

```tsx
import { Popover, PopoverTrigger, PopoverContent } from "@patterninc/apac-ui"
```

Compose using `Popover` (root) + `PopoverTrigger` + `PopoverContent`. Full prop table not yet published in Storybook (re-checked 2026-10-28 — docs page still shows only Default / Align Start / Align End examples).

| Notable | Value |
|---------|-------|
| `align` | `"start" \| "center" \| "end"` |
| Elevation (light) | `shadow-float` |
| Elevation (dark) | `outline-default` border |
| Border radius | `radius-12` |
| Background | `surface-raised` |
| Enter/exit | fade + scale 150ms |

---

### Progress

```tsx
import { Progress } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `value` | `number \| null` | `0` | Current value |
| `max` | `number` | `100` | Maximum value |
| `label` | `ReactNode` | `"Usage"` | Label below the track |
| `valueLabel` | `string` | — | Custom value text opposite the label |
| `showLabels` | `boolean` | `true` | Show label + value text (`false` = bar only) |
| `getValueLabel` | `(value: number, max: number) => string` | — | Accessible value description |
| `barClassName` | `string` | — | Classes for the bar |
| `progressBarProps` | `Omit<ProgressProps, "className" \| "ref" \| "children" \| "asChild" \| "value" \| "max" \| "getValueLabel">` | — | Passed to the bar primitive |
| `className` | `string` | — | Additional class names |

---

### Radio

```tsx
import { Radio } from "@patterninc/apac-ui"
// RadioItem = { label: string; value: string; disabled?: boolean }
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `items` * | `RadioItem[]` | — | Array of radio options |
| `value` | `string` | — | Controlled selected value |
| `defaultValue` | `string` | — | Uncontrolled default value |
| `onValueChange` | `(value: string) => void` | — | Fired on selection change |
| `orientation` | `"vertical" \| "horizontal"` | — | Layout direction |
| `card` | `boolean` | `false` | Card-style container per item |
| `flipped` | `boolean` | `false` | Radio indicator on right (card mode) |
| `hasError` | `boolean` | `false` | Error state |
| `disabled` | `boolean` | `false` | Disables entire group |
| `name` | `string` | — | Name attribute for form submission |
| `className` | `string` | — | Additional class for the group |

---

### ScrollArea

```tsx
import { ScrollArea } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `type` | Radix ScrollArea `type` | — | Scrollbar visibility (stories: On Scroll · Automatic · Always Visible) |
| `viewportRef` | `Ref<HTMLDivElement>` | — | Ref to the scrollable viewport |
| `asChild` | `boolean` | `false` | Renders as Radix Slot |

Size with `className` (e.g. `h-72`). Supports vertical, horizontal and both axes.

---

### Select

```tsx
import { Select } from "@patterninc/apac-ui"
// SelectOption = { label: string; value: string; icon?: ReactNode; description?: string; disabled?: boolean; destructive?: boolean }
// Groups: { groupLabel: string; items: SelectOption[] }
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `items` * | `SelectOption[] \| SelectGroup[]` | — | Flat list or grouped list of options |
| `placeholder` | `string` | `"Select an item"` | Shown when nothing is selected |
| `value` | `string` | — | Controlled value |
| `defaultValue` | `string` | — | Uncontrolled default value |
| `onValueChange` | `(value: string) => void` | — | Fired on selection |
| `label` | `string` | — | Floating label in 2-line trigger mode |
| `size` | `"default" \| "lg" \| "sm" \| "mini"` | `"default"` | Trigger size |
| `itemSize` | `"default" \| "lg"` | `"default"` | Menu item size |
| `hasError` | `boolean` | `false` | Error state |
| `disabled` | `boolean` | `false` | Non-interactive |
| `required` | `boolean` | `false` | HTML required attribute |
| `name` | `string` | — | Name for form submission |
| `className` | `string` | — | Additional class for the trigger |

---

### Sidebar

```tsx
import { Sidebar } from "@patterninc/apac-ui"
// Compound API (as used in Storybook): SidebarProvider, SidebarContainer, SidebarHeader, SidebarContent, SidebarGroup, SidebarGroupLabel, SidebarGroupContent,
// SidebarMenu, SidebarMenuItem, SidebarMenuButton, SidebarMenuBadge, SidebarMenuSub, SidebarMenuSubItem, SidebarMenuSubButton, SidebarSeparator, SidebarFooter, SidebarRail, SidebarInset, SidebarTrigger
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `groups` * | `SidebarGroupConfig[]` | — | Navigation groups config |
| `header` | `ReactNode` | — | Header slot (brand logo) |
| `footer` | `ReactNode` | — | Footer slot |
| `renderLink` | `SidebarRenderLink` | — | Custom link renderer (router integration) |
| `expandedItemIds` | `string[]` | — | Controlled expanded nested items |
| `defaultExpandedItemIds` | `string[]` | — | Uncontrolled expanded items |
| `onExpandedItemIdsChange` | `(ids: string[]) => void` | — | Fired when expanded items change |
| `variant` | `"sidebar" \| "floating" \| "inset"` | see note | Storybook reports default `"default"`, which is not in the union — likely `"sidebar"`; confirm in code |
| `side` | `"left" \| "right"` | `"left"` | Edge |
| `collapsible` | `"icon" \| "offcanvas" \| "none"` | `"icon"` | Collapse behaviour |
| `mobileLabel` | `string` | `"Navigation"` | Accessible title for the mobile drawer |

Map to the Page Shell three-state rule: ≥lg expanded 280px · md–lg `collapsible="icon"` (64px, label Tooltip via `SidebarMenuButton tooltip`) · <md off-canvas drawer. `SidebarProvider` supports `defaultOpen` and `keyboardShortcut`.

**Two-level navigation** (see PAGE SHELL › *Two-level side navigation*): render the parent as a `SidebarMenuButton` that navigates to the landing view (`isActive` only when that view is open). Render its views as `SidebarMenuSub` › `SidebarMenuSubItem` › `SidebarMenuSubButton` (`isActive` on the open view). Keep sub-items expanded with `defaultExpandedItemIds` / `expandedItemIds`, and add a chevron only under the optional-collapse rule. In icon mode shadcn hides `SidebarMenuSub`. Supply the flyout yourself with a `DropdownMenu` (or `HoverCard`) anchored to the parent button, `side="right"`, `align="start"`, opened on hover and focus. Drop the parent's `tooltip` while the flyout is available. Make the sidebar sticky (`sticky top-0 h-svh`, z-index 230).

---

### Skeleton

```tsx
import { Skeleton } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `shape` | `"rectangular" \| "circular" \| "text"` | `"rectangular"` | Matches the shape of replaced content |
| `className` | `string` | — | Use for sizing (width/height) |

Colors: base = `surface-accent` · shimmer highlight = `surface-base` (both mode-aware). Animate with pulse. Compose multiples for complex placeholders.

---

### Stepper

```tsx
import { Stepper } from "@patterninc/apac-ui"
// Primitives: StepperItem, StepperIndicator, StepperConnector — state: "upcoming" | "current" | "completed"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `steps` * | `StepperStep[]` | — | Step definitions |
| `currentStep` | `number` | `0` | Zero-based current step; earlier steps render completed. Pass `steps.length` to complete all |
| `content` | `"title" \| "compact" \| "description"` | `"title"` | Per-step content density |
| `completedLabel` | `ReactNode` | `"Completed"` | Screen-reader text for completed steps |
| `aria-label` | `string` | — | Accessible name |

Use for the Form Page (multi-step wizard) step pills.

---

### Switch

```tsx
import { Switch } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `size` | `"default" \| "sm"` | `"default"` | Track size |
| `checked` / `defaultChecked` | `boolean` | — | Controlled / uncontrolled state |
| `onCheckedChange` | `(checked: boolean) => void` | — | Fired on toggle |
| `disabled` | `boolean` | `false` | Non-interactive |
| `aria-label` | `string` | — | Required when no visible label |
| `asChild` | `boolean` | `false` | Renders as Radix Slot |

With a label: wrap in `Field` and use `FieldLabel htmlFor` + `FieldMessage` (Storybook "With Field" story).

---

### Table (Base Primitives)

```tsx
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, TableFooter, TableCaption } from "@patterninc/apac-ui"
```

Composable layout-only primitives. No built-in sorting or selection — use `DataTable` for those.

| Primitive | Purpose |
|-----------|---------|
| `Table` | Root `<table>` wrapper |
| `TableHeader` | `<thead>` |
| `TableBody` | `<tbody>` |
| `TableFooter` | `<tfoot>` |
| `TableRow` | `<tr>` — hover: `bg-subtle` |
| `TableHead` | `<th>` — `label-md` text |
| `TableCell` | `<td>` — `body-md` text |
| `TableCaption` | `<caption>` — `body-sm text-tertiary` |

Use `Skeleton` cells inside `TableRow` for loading states.

---

### Tabs

```tsx
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@patterninc/apac-ui"
```

| Prop (on `Tabs`) | Type | Default | Notes |
|------------------|------|---------|-------|
| `defaultValue` | `string` | — | Active tab by default (uncontrolled) |
| `orientation` | `"horizontal" \| "vertical"` | `"horizontal"` | Layout direction |
| `className` | `string` | — | Additional class for root |
| `asChild` | `boolean` | `false` | Renders as Radix Slot |

Sizes (apply via `TabsList` or `TabsTrigger`): `sm` · `default` · `lg`
Variants: `default` (filled pill) · `line` (underline indicator)

Use `line` Tabs to switch content inside a card, drawer or dialog. Do not use a page-level tab row for a module's sibling views; make them sidebar sub-items instead (PAGE SHELL › *Two-level side navigation*).

---

### Tag

```tsx
import { Tag } from "@patterninc/apac-ui"
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `variant` | `"neutral" \| "positive" \| "negative" \| "warning" \| "informative"` | `"neutral"` | Semantic status color |
| `children` | `ReactNode` | — | Tag label |

Use Tag for status (semantic) labels; use Badge for brand/emphasis styles.

---

### Textarea

```tsx
import { Textarea } from "@patterninc/apac-ui"
// Extend with <Field> for label, helperText, and error.
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `placeholder` | `string` | — | Placeholder text |
| `variant` | `"default" \| "rounded"` | `"default"` | Visual style |
| `disabled` | `boolean` | `false` | Non-interactive |

Native `<textarea>` props (`value`, `onChange`, `name`, `rows`, etc.) are forwarded.

---

### Toaster (Toast)

```tsx
import { Toaster, toast } from "@patterninc/apac-ui"
// Sonner-based. Mount <Toaster /> once at the app root, then call toast() anywhere.
// toast("msg") · toast.success · toast.info · toast.warning · toast.error · toast.loading · toast.promise
// toast("Item archived", { description, action: { label: "Undo", onClick } })
```

| Prop (on `Toaster`) | Type | Default | Notes |
|---------------------|------|---------|-------|
| `theme` | `"light" \| "dark" \| "system"` | — | Color scheme |
| `position` | Sonner position | `bottom-right` (Sonner default) | **APAC rule: set `position="top-right"`** |
| `closeButton` | `boolean` | — | Close button on every toast |
| `expand` | `boolean` | — | Stack expanded by default |

APAC rules: top-right, 4s auto-dismiss, errors persist; z-index 500.

---

### Tooltip

```tsx
import { Tooltip, TooltipContent, TooltipTrigger, TooltipProvider } from "@patterninc/apac-ui"
// Must be wrapped in <TooltipProvider> to work correctly.
```

| Prop (on `Tooltip`) | Type | Default | Notes |
|---------------------|------|---------|-------|
| `open` | `boolean` | — | Controlled open state |
| `defaultOpen` | `boolean` | — | Uncontrolled default open state |
| `onOpenChange` | `(open: boolean) => void` | — | Fired on open state change |

`TooltipContent` supports `side`: `"top" \| "bottom" \| "left" \| "right"` and custom delay via `delayDuration`.

**Design rules:** always dark pill (`#171717` bg / `#FAFAFA` text) in both light and dark mode. 300ms hover-in delay, instant dismiss. z-index 500 (top layer). Read-only — no interactive content inside.

---

> **API sync schedule:** Bi-weekly. Check Storybook for new or changed components and update this section accordingly. Any new component appearing in Storybook before the next sync should be implemented with shadcn/ui base + APAC tokens until the API is confirmed.
