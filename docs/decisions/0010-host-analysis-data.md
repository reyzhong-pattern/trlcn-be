# 0010: Host Analysis data: three checks per host

- **Status:** PROPOSED (decided by Rey in writing; Rey sets ACCEPTED, AGENTS.md rule 2)
- **Decided by:** Rey, 2026-11-10 (DQ-8, DQ-9, DQ-10), 2026-11-12 (DQ-34) and 2026-11-13 (DQ-8, DQ-9 and DQ-10 revised: the three checks below; DQ-39)
- **Proposed by:** Claude Code (step-05 algorithm spec), revised by Rey
- **Requirement IDs:** R24, R25, R26, R27, R28, BE-11, BE-12, BE-17, BE-23
- **Supersedes / overrides:**
  - spec R24 "hosts without sessions hidden" (`upstream/design-pack/03-product-spec-v0.4.md:1000`); spec §7.2 and §12 "hosts with no lives in the range are listed last" (`:579`, `:936`) and the hi-fi board's no-lives row apply instead;
  - spec §8.2 tag window and thresholds: "the rolling benchmark window (90 days)" and "Benchmark group P50" (`:680-683`), for the quadrant (the "enough data" check keeps the 90-day window);
  - spec §8.3 change marker (`:699`) and §8.4 stability / hysteresis (`:706`, `:725`);
  - the step-05 recommendations for DQ-9 ("any landed session ever") and DQ-34 ("official tag only in v1");
  - earlier forms of this decision: one collapsed no-lives row (2026-11-10); "only hosts live in the range, greying in the range" (2026-11-12); "official 90-day tag + range quadrant" (2026-11-12, withdrawn the same day).

## Context

- The spec leaves open which hosts the leaderboard and the influencer map show, how hosts with little data look, and whether the map follows the range (`upstream/design-pack/03-product-spec-v0.4.md:566-579`, `:683`, `:703`, `:936`, Q7 at `:1041`).
- The spec contradicts itself on hosts with no lives: R24 hides them (`:1000`), §7.2 and §12 list them last (`:579`, `:936`). Rey chose §7.2 / §12 on 2026-11-13.
- A range can start before as_of − 89: presets Custom and This quarter (up to 92 days) (`:195`). So a host can be live in the range with no session in the 90-day window.
- Time bases are in decision 0011: data is T-1, the benchmark is [as_of − 89, as_of].

## Decision

**Host list:** every host of the brand × platform (and of the Type filter's type) with **≥ 1 `ok` session in [as_of − 89, as_of] or in the selected range** (DQ-9). The Hosts filter lists the same hosts, each with its `ok` session count in the range, including 0.

Then each listed host goes through three checks, in order.

1. **Live in the range? (DQ-8)**
   - **Yes:** a leaderboard row with range values, ranked by range GMV descending (ties: DQ-31), and, for an influencer, a point on the influencer map. It can be compared.
   - **No:** a leaderboard row with the host only: ranked after all hosts with lives (by `host_id`), metric values null, "no lives in range" = true, no tag, no tiers. **No map point.** It cannot be compared.
2. **Enough data? (DQ-10)** Counted over **[as_of − 89, as_of]**:
   - **< 3 `ok` sessions or < 10 paid orders → "Not enough data"**: values still returned, tiers null, tag "Not enough data". Leaderboard, Host drawer and map.
   - Otherwise: tiers and tag as below.
   - The same window for every range, even one that ends before `as_of` (Last month, a Custom end date) (DQ-39). Rejected: the 90 days ending on the range's last day.
3. **Tag = quadrant (DQ-34).**
   - The quadrant of the host's **range** exposure per session and AOV, against the **P50 of the Influencer group's `ok` sessions in the range** (Q2 = b).
   - The leaderboard tag and the map colour are the **same value**.
   - **No hysteresis, no change marker, no tag history.** Recomputed for whatever range is selected.
   - Self-operated hosts: "Not tagged".

**Rendering** (colours, badges, "—", hollow or ringed dots, tooltips, clicks): FE, per hi-fi.

## Consequences

- **ALG-29, ALG-30** (rows, rank, check 1, check 2, Hosts filter) and **ALG-31…ALG-33, ALG-36** (map, tag, CVR tier) carry the rules. **ALG-34, ALG-35, ALG-37** are removed (kept as stubs so IDs stay stable).
- **C6:** the 90-day window now also feeds the "enough data" check. Decision 0011 item 3 ("Nothing else does") needs the same exception; Rey to amend 0011.
- **BE-11, BE-12, BE-17, BE-23** change accordingly. The departures from R24, §8.2–§8.5 are listed in `docs/requirements.md` › Departures from the spec.
- Nothing about tags is stored: no tag history. Decision 0005 items 2 and 3 still mention tag history; Rey to amend 0005.
- A host can be "enough data" over 90 days but have only 1 session in the range. It is graded and tagged on that 1 session (per-cell minimums of ALG-22 still apply to tiers).
- **Golden tests:**
  - a host live in the window but not in the range is a host-only row (values null, no tag) and has no map point;
  - a host live only in a Custom range that starts before the window is listed, has a map point, and is "Not enough data" (0 window sessions);
  - a host with no `ok` session in the window or the range is absent;
  - an influencer with < 3 sessions or < 10 orders in the window is "Not enough data" on both the leaderboard and the map;
  - the same host gets different tags at Last 7 and Last 30 days, because the range P50s and its range values differ;
  - the tag on day d does not depend on day d − 1 (no hysteresis).

## Evidence

- Rey's rules of 2026-11-13 in chat ("3 step": live in range → row and map point; enough data over as_of − 89 … as_of; tag by the range quadrant), and Rey's choice of host list option 1 (window ∪ range). Copied by Claude Code on 2026-11-13.
- Rey: in the sandbox the quadrant is option "b. P50 of range sessions", and host A at 30 days shows Premium Niche, by design. UNVERIFIED: the sandbox is not in this repo.
- Count audit 2026-11-10 (KC and THORNE room exports; not in this repo): "any landed session ever" gives THORNE 合作 333 hosts and KC 239. The audit's 260 / 149 are hosts live at Last 30, not in the 90-day window; the window counts are not recorded. Numbers as Rey gave them.

## Open questions

- DQ-38: minimum and Building status for the range P50 lines (for example Last 7 days with few influencer sessions).
- DQ-36 (Day 2): per-cell grading of ①–③ for hosts with "Not enough data".
