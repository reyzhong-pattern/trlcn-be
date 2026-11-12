# 0010: Host Analysis data: leaderboard rows, greying, influencer map points

- **Status:** PROPOSED (decided by Rey in writing; Rey sets ACCEPTED, AGENTS.md rule 2)
- **Decided by:** Rey, 2026-11-10 (DQ-8, DQ-9, DQ-10) and 2026-11-12 (DQ-34; DQ-8 and DQ-10 revised to match the hi-fi mockup)
- **Proposed by:** Claude Code (step-05 algorithm spec), revised by Rey
- **Requirement IDs:** R24, R25, R26, R27, R28, BE-11, BE-17, BE-23
- **Supersedes / overrides:** spec R24 "hosts without sessions hidden" (`upstream/design-pack/03-product-spec-v0.4.md:1000`); the step-05 recommendations for DQ-9 ("any landed session ever") and DQ-34 ("official tag only in v1"); the 2026-11-10 "one collapsed row" form of DQ-8

## Context

- The spec leaves open which hosts the leaderboard and the influencer map show, and how hosts with little data look (`upstream/design-pack/03-product-spec-v0.4.md:566-579`, `:703`, `:936`, Q7 at `:1041`).
- Reference: the hi-fi mockup, artifact `Y6meVMkfzS7bB1NL7mszHB` at version `1794283411-4173` (as in `upstream/PIN.md`), board `project/Host-Analysis.dc.html`, as named by Rey.
- Evidence for DQ-9 and DQ-10: count audit 2026-11-10 (KC and THORNE room exports; not in this repo).

## Decision

**Two dimensions, never mixed.**
- **Tag values** (official tag, "Not enough data", borderline) follow **only the official 90-day tag** (ALG-31…ALG-36).
- **Which hosts appear, their rank, map position and metric values** follow the 90-day window and the **selected range**.

1. **Which hosts appear (DQ-9).**
   - Hosts with an `ok` session in [as_of − 89, as_of] (ALG-12).
   - The Hosts filter lists the same hosts, each with its `ok` session count in the range, including 0.
   - Only hosts with lives in the range can be compared.
   - Rejected: "any landed session ever". At Last 30 it adds a tail larger than the active list (THORNE 合作 333 vs 260 active; KC 239 vs 149).
2. **Hosts with no lives in the range (DQ-8).**
   - Each is an **individual leaderboard row**: the host, a rank after all hosts with lives (ordered by `host_id`), metric values null, "no lives in range" = true, grading status "Not enough data".
   - There is no collapsed "N hosts…" row.
3. **Greying (DQ-10).**
   - **Leaderboard and Host drawer only, range-based:** < 3 `ok` sessions or < 10 paid orders in the range.
   - A greyed host returns its values with grading status "Not enough data" and tiers null. Not used for the map.
   - Evidence: graded 合作 hosts at Last 30 are THORNE 24 of 260 and KC 14 of 149; the < 10 orders rule is the main cause.
   - Follow-up: DQ-36 (Day 2, per-cell grading of ①–③).
4. **Influencer map (DQ-34).**
   - Points = influencers with ≥ 1 `ok` session in the range, at their range exposure / session and AOV. No point otherwise.
   - Quadrant lines = the 90-day P50s.
   - Each point returns the official tag ("Not enough data" when < 3 `ok` sessions or < 10 paid orders in the 90-day window), borderline, and the range quadrant.
5. **Rendering** of all of the above ("—", badges, colours, hollow or ringed dots, size, tooltips, clicks): FE, per hi-fi (AGENTS.md rule 11).

## Consequences

- **ALG-30** (rows, rank, greying, Hosts filter) and **ALG-31** (Influencer map) carry the rules. ALG-22, ALG-29 and ALG-41 are scoped to match.
- **BE-11, BE-17, BE-23** change accordingly. R24 is recorded under "Departures from the spec" in `docs/requirements.md`.
- **Golden tests:**
  - a no-lives row ranked last with metric values null;
  - a Hosts filter entry with 0 sessions;
  - a host greyed on the leaderboard but with an official tag on the map;
  - a map point with tag "Not enough data" at its range position;
  - no point for a host without lives in the range.

## Evidence

- Rey's instructions of 2026-11-10 and 2026-11-12, copied by Claude Code.
- Count audit 2026-11-10 (numbers as Rey gave them; not in this repo).
- Mockup board `project/Host-Analysis.dc.html`, verified 2026-11-12 against artifact `Y6meVMkfzS7bB1NL7mszHB` at version `1794283411-4173` (an earlier read used a different artifact, which served `1793933571-41ce`; the points below are the same in both). The board's range is "Last 90 days". In it:
  - the no-lives host (李娜老师讲修行(臻健来)) is rank 14 of 14, with Sessions "0", "—" in the other metric cells, "No lives in this range" and a "Not enough data" badge;
  - 11 map dots for 14 hosts, none for the no-lives host.

## Open questions

- See the PR description for every place the docs still differ from the mockup.
