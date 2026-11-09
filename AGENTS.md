# AGENTS.md — rules for every agent and human working in this repo

This is the single rules file. Every agent (Claude Code, GrokBot, any other) reads it before doing anything.
Agent-specific files (for example [CLAUDE.md](CLAUDE.md)) add role details; they never relax a rule here.

## What this repo is

Backend for **TrendVision Live — Performance Analytics** (Session Analytics, Host Analysis, Settings; brand-scoped).

- Product source of truth: [upstream/design-pack/03-product-spec-v0.4.md](upstream/design-pack/03-product-spec-v0.4.md), as overridden by [docs/decisions/](docs/decisions/).
- The hi-fi mockup is a **reference only** (see [upstream/PIN.md](upstream/PIN.md)).
- Layers in this repo: **Land → Score → Serve → Access** ([docs/scope.md](docs/scope.md)). **Fetch is out of scope.**
- Vocabulary: [docs/glossary.md](docs/glossary.md). "R1" etc. are requirement IDs; the Compass file is the **room export**.

## Roles

| Who | Role |
|---|---|
| **Rey** (human) | Decides. The only person who sets a decision to ACCEPTED. Approves merges. |
| **FE** (human) | Builds the frontend against [contract/openapi.yaml](contract/README.md) in this repo, and nothing else. |
| **GrokBot** (coding agent) | Builds the backend: Land, Score, Serve, Access. |
| **Claude Code** (agent) | Plans, writes specs, tests and the API contract, and reviews. |

## Rules

1. **No self-review.** GrokBot never reviews its own work. Every GrokBot PR gets a Claude Code review, run in a **fresh session** that did not write the code, using [docs/templates/review.md](docs/templates/review.md).
2. **Only Rey accepts.** Only Rey sets a decision to `ACCEPTED`. Agents write decisions as `PROPOSED` and add open items to [docs/decision-queue.md](docs/decision-queue.md). An agent never edits the status of a decision to ACCEPTED, REJECTED or SUPERSEDED.
3. **Never commit or push straight to `main`.** One PR per task, from its own branch, using [.github/pull_request_template.md](.github/pull_request_template.md). Tasks are written with [docs/templates/task.md](docs/templates/task.md).
4. **Evidence rule.** Any statement about code or data cites a file path and line (for example `upstream/design-pack/03-product-spec-v0.4.md:261`), or is marked **UNVERIFIED**. "Tests pass" means the command and its real output are pasted in the PR.
5. **No real brand data, no secrets.** Never commit real brand or platform data (Compass exports, database dumps, screenshots of real numbers). Real files live under `data/`, which is git-ignored ([.gitignore](.gitignore)). No passwords, API keys, tokens or database URLs with credentials in any file, including tests, docs and examples. Use environment variables and placeholders.
6. **`/upstream` is read-only.** Vendored files are never edited. To update them, re-vendor a new commit and update [upstream/PIN.md](upstream/PIN.md) in its own PR.
7. **Fetch is out of scope.** This repo does not download files from Compass or any platform. **Never automate Compass or any platform UI** (no browser automation, no scraping, no headless login). Land starts from raw files and a file log handed over by Fetch.
8. **Two separate answers.** Health tier (STAR/GOOD/MID/WEAK) and recoverable revenue (¥) are separate outputs, computed separately, and never combined into one score.
9. **LLMs explain, the pipeline computes.** An LLM may explain numbers (for example Action Card text), but never computes, rounds, estimates or changes them. Every number shown comes from the Score layer.
10. **No database connections from agents during bootstrap tasks** unless the task file explicitly allows it. Which Supabase schemas the build uses is decided during building.

## Source-of-truth order

Read in this order: **spec v0.4 → decisions ([docs/decisions/](docs/decisions/)) → [contract](contract/README.md)**. The spec is the base; an ACCEPTED decision overrides the spec on the point it decides; the contract must follow both. PROPOSED decisions override nothing.
Decision 0004 says the hi-fi wins over the spec and older methods where they conflict, and the mockup's behaviour wins where the spec is silent.
The demo generator (`upstream/design-pack/generate_demo_data.py`) is **not** a source of expected outputs (see [tests/golden/README.md](tests/golden/README.md)).

## Where things are

| Path | What |
|---|---|
| [docs/scope.md](docs/scope.md) | The four layers and what each owns |
| [docs/requirements.md](docs/requirements.md) | Requirement list (spec section 15 + LAND-1, AC-1, AUTH-1) |
| [docs/algorithm-spec.md](docs/algorithm-spec.md) | Scoring algorithm (template; filled in the next step) |
| [docs/data-model/](docs/data-model/) | Room export model, quarantine rules |
| [docs/decisions/](docs/decisions/) | Decision records |
| [docs/decision-queue.md](docs/decision-queue.md) | Open decisions with owners |
| [docs/templates/](docs/templates/) | Task, decision and review templates |
| [contract/](contract/README.md) | UI API contract (OpenAPI) for FE |
| [ingest/](ingest/README.md) | Land layer (LAND-1) |
| [tests/golden/](tests/golden/README.md) | Golden expected outputs |
| [upstream/](upstream/PIN.md) | Vendored design pack (read-only) |
