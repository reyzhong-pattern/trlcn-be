# ingest/ — Land layer (LAND-1)

**No code yet.** Scope only.

- **Input:** room-export files (one row per live session) plus the file log, handed over by Fetch ([../docs/scope.md](../docs/scope.md)). Fetch itself is out of scope; nothing here downloads from Compass or automates any platform UI.
- **Does:** map columns ([../docs/data-model/room-export.md](../docs/data-model/room-export.md); names UNVERIFIED), apply quarantine rules ([../docs/data-model/quarantine-rules.md](../docs/data-model/quarantine-rules.md); PROPOSED), cross-check Compass's ratio columns, record lineage, land session records idempotently.
- **Does not:** compute benchmarks, tiers or revenue (that is Score); land the product export (later, decision 0002).
- **Data:** real files live only under `data/` (git-ignored). Tests use synthetic fixtures.
- Target storage (Supabase schema, tables): TBD.
