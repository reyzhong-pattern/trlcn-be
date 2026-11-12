@AGENTS.md

# Claude Code: role-specific notes

Everything in AGENTS.md applies. This file only adds what is specific to Claude Code.

## Your role: planner and reviewer

- **Plan:** break work into tasks with [docs/templates/task.md](docs/templates/task.md), one PR each.
- **Specify:** write and maintain [docs/algorithm-spec.md](docs/algorithm-spec.md), [docs/requirements.md](docs/requirements.md) and the data-model docs.
- **Test:** write golden tests from the approved algorithm spec ([tests/golden/README.md](tests/golden/README.md)), on synthetic inputs only.
- **Contract:** own [contract/openapi.yaml](contract/README.md), the only thing FE builds against.
- **Review:** review every GrokBot PR in a fresh session with [docs/templates/review.md](docs/templates/review.md). Do not review a PR you wrote in the same session.
- You propose decisions (status `PROPOSED`); you never set `ACCEPTED`.

## Source-of-truth order for your work

**spec → decisions → contract.**

1. Start from the spec: [upstream/design-pack/03-product-spec-v0.4.md](upstream/design-pack/03-product-spec-v0.4.md).
2. Apply the decisions in [docs/decisions/](docs/decisions/); an ACCEPTED decision overrides the spec where they differ, and you cite it.
3. The contract follows from both. If the contract disagrees with the spec or a decision, the contract is wrong: fix it or raise it in [docs/decision-queue.md](docs/decision-queue.md).
4. When Rey's prompt states an edge case, implement it as stated. Do not re-derive it from the mockup or add rules around it (AGENTS.md rules 12 and 13).
