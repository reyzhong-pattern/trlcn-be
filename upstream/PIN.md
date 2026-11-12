# upstream/PIN.md — what is vendored, from where

`/upstream` is **read-only** (AGENTS.md rule 6). Files are copied byte-for-byte; never edit them here.

## Design pack

| Field | Value |
|---|---|
| Repo | `github.com/patterninc/Trend-Vision-Live_C` |
| Commit | `a0dd5501d386291b712ae3bb423fb7e996332763` (short `a0dd550`) |
| Commit date | 2026-11-06 14:37:53 +0800 ("Add files via upload") |
| Date copied | 2026-11-09 |
| Copied by | Claude Code, `git clone --depth 1`, HEAD verified = `a0dd550`, files copied unchanged |
| Destination | `upstream/design-pack/` |

### Files present at a0dd550 (15 files; this is everything in the commit)

| File | Bytes | sha256 |
|---|---|---|
| `00-START-HERE.md` | 6648 | `0bbefbc930bb843bd3b89dcc264beee763a737d4c4426aeee303bfc28554a304` |
| `01-design-brief.md` | 25334 | `486fd6383861f68fd72537024b632db30b364ea2d0d2eddd41f71ad719e311ac` |
| `02-prototype-data.json` | 271946 | `b8bf6a27f057728fd9af82a97d7b7337f79b99a5a65ad881026016d7e290d288` |
| `02-sessions-last-30-days.csv` | 86354 | `29edc94fbc598a93c59b1b116db52c4e30f172b6d6dfa8ef82315aeb8556eeef` |
| `03-product-spec-v0.4.md` | 113490 | `f31bb69195e1b5c74334bba9ec500fdae05f4a5bc591c0d547dc644a479930e4` |
| `04-APAC-Design-System-SKILL.md` | 68514 | `5d59bd0558cfa149682fc72c4805f3e01b20ecee45dbd52ff81da0f07f20468a` |
| `05-terminology-zh-en.md` | 4463 | `00077c28a8679cd21e26994c729c6ae81087d79cb43c54c043933d382c353b5b` |
| `README.md` | 1324 | `325629bc35aa92accbe8c848905c684dad4b7d11beb728045f63c7c8633ce132` |
| `accounts.csv` | 6737 | `f039f9a09bb0088269ebb8d3356a0fbfa14dfea8f608c33f5c2eb4175af5d943` |
| `benchmarks.csv` | 5420 | `2b1d63eaeec4495418a47c50623878b9a5a688ae2f1470fca80ee2744b8972e4` |
| `generate_demo_data.py` | 21312 | `55f3f96ad33057c6220fb7a6de96108dea677ab7831383ca1fb6ac1ef2c17f97` |
| `host_tags.csv` | 14993 | `710e0358959d1eca3837ff560bd8fa5eb967591b9fb133c2e99d9fce61694bdc` |
| `platform_connections.csv` | 627 | `7964f3861dd00f22bcb428a3dcf985419149adc42340a2dafb2a4892c66209fb` |
| `sessions.csv` | 1354643 | `fba27b749bd30842b8afa3924054fd2ee2066ad4bde02f03a4d1989778beb02b` |
| `users.csv` | 591 | `53c4cfa6f8cdb8661b59f97ed72c53e5497f9b2a24a4360b97f73410feabd37d` |

Verify with:

```bash
cd upstream/design-pack && sha256sum -c ../design-pack.sha256
```

([design-pack.sha256](design-pack.sha256) holds the same hashes in `sha256sum` format.)

### Referenced but not in the repo

`00-START-HERE.md` lists these, but they are **not present** at a0dd550:

- `prompts/` (round-1 … round-6 prompts, `round-1b-make-it-clickable.md`, `prototype-after-round-2 … 5.md`, `round-1-patch-v0.3.md`, `feedback-templates.md`) — `upstream/design-pack/00-START-HERE.md:17-20`
- `demo-data/` — `upstream/design-pack/00-START-HERE.md:16`. The demo data files and `generate_demo_data.py` sit at the repo root instead of in a `demo-data/` folder.
- `Pattern-brand asset/` (`Logo_full.svg`, `Logomark_blue.svg`) — `upstream/design-pack/00-START-HERE.md:15`

The spec also refers to `demo-data/` (`upstream/design-pack/03-product-spec-v0.4.md:6`).

### Notes on content

- The pack's README says all data is **synthetic** (`upstream/design-pack/README.md:1-3`); the generator says "All values are synthetic" (`upstream/design-pack/generate_demo_data.py:1-3`). It uses real brand names (Thorne, KELO-COTE, Swanson) with synthetic numbers; `users.csv` uses `example.com` addresses. Treat it as synthetic input only.
- `generate_demo_data.py` does not grade like the spec. Never use its outputs (tier, weakest-stage, recoverable columns, `benchmarks.csv`) as expected values. See [tests/golden/README.md](../tests/golden/README.md).
- The spec's requirement table (section 15) has no **R23**: it goes from R22 to R24 (`upstream/design-pack/03-product-spec-v0.4.md:999-1000`).

## Hi-fi mockup (reference only, not pinned)

| Field | Value |
|---|---|
| What | claude.ai Design artifact (hi-fi mockup) |
| URL | https://claude.ai/artifact/Y6meVMkfzS7bB1NL7mszHB |
| Version | `1794283411-4173` |
| Status | **Reference only.** It cannot be pinned or vendored; its content can change. Not copied into this repo. |

Decision [0004](../docs/decisions/0004-hifi-wins-and-resolved-rules.md) says the hi-fi wins over the spec and older methods where they conflict, and the mockup's behaviour wins where the spec is silent. Any claim about the mockup's behaviour names the version above, or is marked UNVERIFIED.
