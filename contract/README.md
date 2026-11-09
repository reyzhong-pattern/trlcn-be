# contract/ — UI API contract

- **FE contracts only against the UI API defined here**, in `contract/openapi.yaml`. FE does not read the database, Score internals or any other BE file.
- **Status: v1 pending.** `openapi.yaml` is a placeholder with no endpoints; Claude Code writes it in a later task, from the spec (`upstream/design-pack/03-product-spec-v0.4.md`) and the accepted decisions ([../docs/decisions/](../docs/decisions/)).
- Serve implements this contract; a mismatch between Serve and the contract is a Serve bug. A mismatch between the contract and the spec / accepted decisions is a contract bug.
- Every change to the contract goes in its own PR and is flagged for FE.
- Brand access (AUTH-1, R30) applies to every endpoint.
