<!-- Rules: AGENTS.md. One PR per task, from its own branch. Never push straight to main. -->

## Task

Task file: `docs/tasks/...` (or link) · Requirement IDs: <!-- e.g. R9, LAND-1 -->
Author: <!-- GrokBot / Claude Code / human --> · Reviewer: <!-- must not be the author; GrokBot PRs need a Claude Code review in a fresh session -->

## What changed

<!-- Bullet list. Every claim about code or data cites path:line, or is marked UNVERIFIED. -->
-

## Tests run (real output)

<!-- Paste the exact commands and their real, unedited output. "Tests pass" without output is not accepted. If no tests apply, say why. -->
```text
$ <command>
<output>
```

## What wasn't done

<!-- Anything in the task's scope that this PR does not do, and why. -->
-

## Open questions

<!-- New items also go into docs/decision-queue.md with an owner. -->
-

## Checklist

- [ ] Every statement about code or data cites `path:line` or is marked UNVERIFIED
- [ ] Tests run, with real output pasted above
- [ ] No decision set to ACCEPTED by an agent (only Rey accepts; agents write PROPOSED)
- [ ] No real brand data committed; nothing added under `data/`
- [ ] No secrets (keys, tokens, passwords, DB URLs with credentials) in any file
- [ ] `/upstream` unchanged (or this PR is a re-vendor with an updated `upstream/PIN.md`)
- [ ] No Fetch code, no automation of Compass or any platform UI
- [ ] Health tier and recoverable revenue kept separate; no number computed by an LLM
- [ ] Contract changes (if any) are in `contract/openapi.yaml` and noted for FE
