# trlcn-be — TrendVision Live: Performance Analytics (backend)

Backend for TrendVision Live — Performance Analytics: Session Analytics, Host Analysis and Settings, brand-scoped.

**Status: bootstrap.** Docs and scaffolding only. No application code yet.

## Start here

1. [AGENTS.md](AGENTS.md) — rules for every agent and human (Claude Code also reads [CLAUDE.md](CLAUDE.md)).
2. [docs/scope.md](docs/scope.md) — the four layers: Land → Score → Serve → Access. Fetch is out of scope.
3. [docs/requirements.md](docs/requirements.md) — R1–R45 (spec section 15) plus LAND-1, AC-1, AUTH-1.
4. [docs/decisions/](docs/decisions/) and [docs/decision-queue.md](docs/decision-queue.md).
5. [docs/glossary.md](docs/glossary.md).

## Layout

| Path | What |
|---|---|
| [upstream/](upstream/PIN.md) | Vendored design pack @ a0dd550 (read-only); [upstream/PIN.md](upstream/PIN.md) |
| [docs/](docs/) | Scope, requirements, glossary, algorithm spec, data model, decisions, templates |
| [contract/](contract/README.md) | UI API contract for FE (v1 pending) |
| [ingest/](ingest/README.md) | Land layer (LAND-1), no code yet |
| [tests/golden/](tests/golden/README.md) | Golden expected outputs (none yet) |

Real data files belong under `data/`, which git ignores. Never commit real brand data or secrets.
