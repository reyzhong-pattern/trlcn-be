# 0010: Host Analysis data: everything follows the selected time range

- **Status:** PROPOSED (decided by Rey in writing; Rey sets ACCEPTED, AGENTS.md rule 2)
- **Decided by:** Rey, 2026-11-10 (DQ-8, DQ-9, DQ-10) and 2026-11-12 (DQ-34; DQ-8, DQ-9 and DQ-10 revised: "everything in Host Analysis uses the shell time range")
- **Proposed by:** Claude Code (step-05 algorithm spec), revised by Rey
- **Requirement IDs:** R24, R25, R26, R27, R28, BE-11, BE-12, BE-17, BE-23
- **Supersedes / overrides:**
  - spec §7.2 and §12 "hosts with no lives in the range are listed last" (`upstream/design-pack/03-product-spec-v0.4.md:579`, `:936`) and the hi-fi board's no-lives row; spec R24 "hosts without sessions hidden" (`:1000`) applies instead;
  - spec §8.2 tag window and thresholds: "the rolling benchmark window (90 days)" and "Benchmark group P50" (`:680-683`);
  - spec §8.3 change marker (`:699`) and §8.4 stability / hysteresis (`:706`, `:725`);
  - the step-05 recommendations for DQ-9 ("any landed session ever") and DQ-34 ("official tag only in v1");
  - earlier forms of this decision: one collapsed no-lives row (2026-11-10), individual no-lives rows, a 90-day host list, and "official 90-day tag + range quadrant" (2026-11-12, withdrawn the same day).

## Context

- The spec leaves open which hosts the leaderboard and the influencer map show, how hosts with little data look, and whether the map follows the range (`upstream/design-pack/03-product-spec-v0.4.md:566-579`, `:683`, `:703`, `:936`, Q7 at `:1041`).
- The spec contradicts itself on hosts with no lives: R24 hides them (`:1000`), §7.2 and §12 list them last (`:579`, `:936`). Rey chose R24.
- Time bases are in decision 0011: data is T-1, every range ends on `as_of`, and the benchmark [as_of − 89, as_of] is used only for tiers and Action Card P50/P75.

## Decision

**Everything in Host Analysis uses the selected (shell) time range.**

1. **Which hosts appear (DQ-9, DQ-8).**
   - The leaderboard lists only hosts with **≥ 1 `ok` session in the range**. Others are not returned (R24).
   - The Hosts filter lists the same hosts, each with its `ok` session count in the range.
   - Rank = range GMV descending (ties: DQ-31).
2. **Greying (DQ-10).** A host with **< 3 `ok` sessions or < 10 paid orders in the range** is greyed: its values are returned, tiers are null, and its tag is "Not enough data". Leaderboard and Host drawer.
3. **Tag (DQ-34).**
   - Tag = the quadrant of the host's **range** exposure per session and AOV, against the **P50 of the Influencer group's sessions in the range** (Q2 = b).
   - The leaderboard tag and the influencer map colour are the **same value**.
   - **No hysteresis, no change marker, no tag history.** The tag is recomputed for whatever range is selected.
   - Self-operated hosts: "Not tagged".
4. **Influencer map.** One point per listed influencer, at its range exposure per session and AOV; quadrant lines at the range P50s.
5. **Rendering** (colours, badges, "—", hollow or ringed dots, tooltips, clicks): FE, per hi-fi.

## Consequences

- **ALG-29, ALG-30** (rows, rank, greying, Hosts filter) and **ALG-31…ALG-33, ALG-36** (tag, map, CVR tier) carry the rules. **ALG-34, ALG-35, ALG-37** are removed (kept as stubs so IDs stay stable).
- **BE-11, BE-12, BE-17, BE-23** change accordingly. The departures from §7.2, §8.2–§8.5 and §12 are listed in `docs/requirements.md` › Departures from the spec.
- Nothing about tags is stored: no tag history. Decision 0005 items 2 and 3 still mention tag history; Rey to amend 0005.
- **Golden tests:**
  - a host with no `ok` session in the range is absent from the leaderboard, the Hosts filter and the map;
  - a greyed influencer has tiers null and tag "Not enough data" on both the leaderboard and the map;
  - the same host gets different tags at Last 7 and Last 30 days, because the range P50s and its range values differ;
  - the tag on day d does not depend on day d − 1 (no hysteresis).

## Evidence

- Rey's "locked rules" and change list of 2026-11-12, copied by Claude Code on 2026-11-12.
- Rey: in the sandbox this is option "b. P50 of range sessions", and host A at 30 days shows Premium Niche, by design. UNVERIFIED: the sandbox is not in this repo.
- Count audit 2026-11-10 for DQ-9 and DQ-10 (THORNE 合作 333 vs 260 active, KC 239 vs 149; graded 合作 hosts at Last 30: THORNE 24 of 260, KC 14 of 149). Numbers as Rey gave them; not in this repo.

## Open questions

- DQ-38: minimum and Building status for the range P50 lines (for example Last 7 days with few influencer sessions).
- DQ-36 (Day 2): per-cell grading of ①–③ for greyed hosts.
