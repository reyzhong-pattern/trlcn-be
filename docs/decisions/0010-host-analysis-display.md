# 0010: Host Analysis display: leaderboard rows, greying, influencer map

- **Status:** ACCEPTED (recorded by Claude Code on Rey's written instruction; see AGENTS.md rule 2 note in the PR)
- **Decided by:** Rey, 2026-11-10 (DQ-8, DQ-9, DQ-10) and 2026-11-12 (DQ-34; DQ-8 and DQ-10 revised to match the hi-fi mockup)
- **Proposed by:** Claude Code (step-05 algorithm spec), revised by Rey
- **Requirement IDs:** R24, R25, R26, R27, R28, BE-11, BE-17, BE-23
- **Supersedes / overrides:** spec R24 "hosts without sessions hidden" (`upstream/design-pack/03-product-spec-v0.4.md:1000`); the step-05 recommendations for DQ-9 ("any landed session ever") and DQ-34 ("official tag only in v1"); the 2026-11-10 "one collapsed row" form of DQ-8

## Context

- The spec leaves open which hosts the leaderboard and the influencer map show, and how hosts with little data look (`upstream/design-pack/03-product-spec-v0.4.md:566-579`, `:703`, `:936`, Q7 at `:1041`).
- Reference: the hi-fi mockup, version `1794283411-4173`, board `project/Host-Analysis.dc.html`, as named by Rey.
  - Claude Code could only read version `1793933571-41ce` of that board (see Evidence).
- Evidence for DQ-9 and DQ-10: count audit 2026-11-10 (KC and THORNE room exports; not in this repo).

## Decision

**Two dimensions, never mixed.**
- **Appearance** (tag colour, hollow, borderline ring) follows **only the official 90-day tag** (ALG-31…ALG-36).
- **Which hosts appear, where they sit and which values they show** follow the 90-day window and the **selected range**.

1. **Which hosts appear (DQ-9).**
   - Hosts with an `ok` session in [as_of − 89, as_of] (ALG-12).
   - The Hosts filter lists the same hosts, each with its `ok` session count in the range, including 0.
   - Only hosts with lives in the range can be compared.
   - Rejected: "any landed session ever". At Last 30 it adds a tail larger than the active list (THORNE 合作 333 vs 260 active; KC 239 vs 149).
2. **Hosts with no lives in the range (DQ-8).**
   - Each is an **individual leaderboard row**: the host name, a rank after all hosts with lives (ordered by `host_id`), "—" in every metric cell, "No lives in this range", and the "Not enough data" badge.
   - There is no collapsed "N hosts…" row.
3. **Greying (DQ-10).**
   - **Leaderboard and Host drawer only, range-based:** < 3 `ok` sessions or < 10 paid orders in the range.
   - A greyed host shows its values with "Not enough data", no tiers and n/a tier cells. Not used for the map.
   - Evidence: graded 合作 hosts at Last 30 are THORNE 24 of 260 and KC 14 of 149; the < 10 orders rule is the main cause.
   - Follow-up: DQ-36 (Day 2, per-cell grading of ①–③).
4. **Influencer map (DQ-34).**
   - Dots = influencers with ≥ 1 `ok` session in the range, positioned by their range exposure / session and AOV. No dot otherwise.
   - Quadrant lines = the 90-day P50s.
   - Colour = official tag. Hollow = official tag "Not enough data" (< 3 `ok` sessions or < 10 paid orders in the 90-day window, so no tag yet); a hollow dot is clickable and opens the host. Ring = borderline.
   - The tooltip shows the official tag and, when it differs, the range quadrant.

## Consequences

- **ALG-30** (rows, rank, greying, Hosts filter) and **ALG-31** (Influencer map) carry the rules. ALG-22, ALG-29 and ALG-41 are scoped to match.
- **BE-11, BE-17, BE-23** change accordingly. R24 is recorded under "Departures from the spec" in `docs/requirements.md`.
- **Golden tests:**
  - a no-lives row ranked last with "—";
  - a Hosts filter entry with 0 sessions;
  - a host greyed on the leaderboard but solid on the map;
  - a hollow dot (tag "Not enough data") at its range position;
  - no dot for a host without lives in the range.

## Evidence

- Rey's instructions of 2026-11-10 and 2026-11-12, copied by Claude Code.
- Count audit 2026-11-10 (numbers as Rey gave them; not in this repo).
- Mockup board `project/Host-Analysis.dc.html`. The read on 2026-11-12 served version `1793933571-41ce`, not `1794283411-4173`; that board's range is "Last 90 days". In it:
  - the no-lives host (李娜老师讲修行(臻健来)) is rank 14 of 14, with Sessions "0", "—" in the other metric cells, "No lives in this range" and a "Not enough data" badge;
  - 11 map dots for 14 hosts, none for the no-lives host;
  - "Not enough data" dots are transparent with a 2px grey border and are buttons;
  - dot size scales with GMV.

## Open questions

- See the PR description for every place the docs still differ from the mockup.
