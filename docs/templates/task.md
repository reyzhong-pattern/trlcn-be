# Task: <short title>

<!-- Copy to docs/tasks/NNNN-<slug>.md. Rules: AGENTS.md. One task = one branch = one PR. -->

- **ID:** TASK-NNNN
- **Layer:** Land / Score / Serve / Access / Docs / Contract
- **Requirement IDs:** <!-- e.g. R8, R9, LAND-1 -->
- **Assignee:** <!-- GrokBot / Claude Code / human -->
- **Reviewer:** <!-- never the assignee; GrokBot work → Claude Code in a fresh session -->
- **Branch:** `task/NNNN-<slug>` (never `main`)
- **Database access allowed:** no / yes (which project, which schema, read or write — never credentials in this file)

## Goal

<!-- One or two sentences: what is true when this is done. -->

## Inputs and sources

<!-- Cite path:line for every spec, decision or data reference. Anything not checked is marked UNVERIFIED. -->
- Spec: `upstream/design-pack/03-product-spec-v0.4.md:<line>`
- Decisions: `docs/decisions/NNNN-*.md`

## In scope

-

## Out of scope

- Fetch (getting files from Compass); any automation of a platform UI
- <!-- anything else -->

## Acceptance criteria

<!-- Each one testable. Name the test or command that proves it. -->
- [ ]

## Evidence required in the PR

- [ ] Commands run and their real output
- [ ] `path:line` citations for every claim about code or data, or UNVERIFIED
- [ ] What wasn't done, and open questions (also added to `docs/decision-queue.md` with an owner)

## Constraints (from AGENTS.md)

- No real brand data in git; real files only under `data/` (git-ignored)
- No secrets in any file
- `/upstream` is read-only
- Agents do not set decisions to ACCEPTED
- Health tier and recoverable revenue are separate outputs; an LLM never computes a number
