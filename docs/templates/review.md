# Review: PR <owner/repo#N> — <title>

<!-- Rules: AGENTS.md. The reviewer is never the author. GrokBot PRs are reviewed by Claude Code in a fresh session. -->

- **Reviewer:** <!-- agent / person; session that did NOT write the code -->
- **Author:** <!-- -->
- **Task / requirement IDs:** <!-- -->
- **Verdict:** APPROVE / REQUEST CHANGES / COMMENT <!-- an agent's verdict is advice; Rey merges -->

## What changed (as verified by the reviewer)

<!-- Cite path:line for each item. Anything the reviewer could not verify is marked UNVERIFIED. -->
-

## Tests (re-run by the reviewer, real output)

```text
$ <command>
<output>
```

## Rule checks

- [ ] Evidence: every claim in the PR cites `path:line` or is marked UNVERIFIED
- [ ] Tests: commands and real output present, and re-run here
- [ ] Decisions: no agent set a decision to ACCEPTED; new decisions are PROPOSED
- [ ] Matches spec → accepted decisions → contract (cite any conflict)
- [ ] No real brand data; nothing committed under `data/`
- [ ] No secrets in any file
- [ ] `/upstream` unchanged
- [ ] No Fetch code; no automation of Compass or any platform UI
- [ ] Health tier and recoverable revenue are separate; no LLM-computed numbers
- [ ] Brand access enforced in the database for any new read path (AUTH-1, R30)

## Findings

| # | Severity | File:line | Finding | Suggested fix |
|---|---|---|---|---|
| 1 | | | | |

## What wasn't reviewed

-

## Open questions

<!-- Also add to docs/decision-queue.md with an owner. -->
-
