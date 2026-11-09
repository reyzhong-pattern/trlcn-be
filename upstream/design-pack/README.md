# TrendVision Live demo data (synthetic)

Synthetic multi-platform data for prototyping Performance Analytics. It is not real performance data.

- **Brands:** Thorne, KELO-COTE, Swanson
- **Platforms:** Douyin, RED, Tmall, JD. Two brand × platform pairs are deliberately not connected: KELO-COTE × JD and Swanson × RED.
- **Period:** completed sessions from 1 Sep 2025 to 27 Oct 2026, plus one live session on 28 Oct 2026
- **Benchmarks and tags:** as of 27 Oct 2026, over a 90-day rolling window with a minimum of 20 sessions

| File | Content |
|---|---|
| `sessions.csv` | One row per session: funnel counts, orders, GMV, rates, tiers, weakest stage, recoverable revenue |
| `accounts.csv` | Accounts and KOLs per brand × platform × type |
| `benchmarks.csv` | P25/P50/P75 per Brand × Platform × Type |
| `host_tags.csv` | Account-level aggregates and Reach × AOV tags (influencers only) |
| `platform_connections.csv` | Connection status and annual GMV (simulating the MCP value) |
| `users.csv` | Fictional users for the Settings prototype |

Files are UTF-8 with BOM, so they open correctly in Excel with Chinese names.

Regenerate with `python3 generate_demo_data.py <output_dir>`; the fixed seed gives the same output every time. Field definitions and built-in scenarios are in the product spec, Appendix A.
