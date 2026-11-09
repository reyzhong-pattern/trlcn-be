# tests/golden/ — expected outputs

- **Expected outputs come from a small reference implementation written from the approved algorithm spec** ([../../docs/algorithm-spec.md](../../docs/algorithm-spec.md), once approved by Rey), run on **synthetic inputs** only.
- The reference is small and readable on purpose (no performance tricks), so a reviewer can check it line by line against the spec and decisions 0001 and 0004.
- **Never use the design pack's generator outputs as expected values.** `upstream/design-pack/generate_demo_data.py` does not grade like the spec: it uses the 90 days before each session and excludes the session itself (`upstream/design-pack/generate_demo_data.py:209`), has no All types group (it groups by brand × platform × type only, `:196` and `:251`), and grades session tier when entered > 0 (`:237`). Its tier, weakest-stage and recoverable columns, `benchmarks.csv` and `host_tags.csv` are therefore not expected outputs. Its **inputs** (funnel counts, orders, GMV) may be used as synthetic inputs.
- No real brand data in this folder. Fixtures are synthetic and small.
- Status: no tests yet.
