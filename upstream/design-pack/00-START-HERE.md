# Claude Design pack: TrendVision Live — Performance Analytics

This pack lets you direct Claude Design through the first prototype in six rounds of artboards. Claude Design pairs a chat with a canvas of artboards. You describe what you want, it builds artboards beside the conversation, and you refine them through chat, inline comments or direct edits on the canvas.

## What is in the pack

| File | Purpose | When to attach |
|---|---|---|
| `01-design-brief.md` | Condensed brief: product, shell, vocabulary, every screen, states, data map | Round 1 (and any new chat) |
| `02-prototype-data.json` | Pre-computed demo numbers: overview, funnel, benchmarks, featured sessions with Action Cards, hosts, users | Round 1 (and any new chat) |
| `02-sessions-last-30-days.csv` | 347 sessions (28 Sep – 27 Oct 2026, plus one live session) for the tables | Rounds 1 and 4 |
| `03-product-spec-v0.4.md` | Full spec (source of truth), as a reference for details the brief leaves out | Round 1, as reference |
| `05-terminology-zh-en.md` | Fixed Chinese / English terms for every label | Round 1 (and any new chat) |
| `04-APAC-Design-System-SKILL.md` | The APAC Design System | Only if your organization's design system in Claude Design is not already APAC |
| `Pattern-brand asset/` | Pattern logo files: `Logo_full.svg` (expanded sidebar header), `Logomark_blue.svg` (collapsed 64px sidebar, favicon) | Round 1, for the sidebar logo |
| `demo-data/` | The full synthetic dataset and its generator (for engineering; the design agent only needs the 02 files) | Not needed in Claude Design |
| `prompts/round-1 … round-6` | The prompt to paste for each round | One per round |
| `prompts/round-1b-make-it-clickable.md`, `prompts/prototype-after-round-2 … 5.md` | Build, then extend, the one clickable prototype | After each round is approved |
| `prompts/round-1-patch-v0.3.md` | Patch for a round 1 already in progress: Host wording, 中文/EN toggle, shared Comparison panel | Once, if round 1 started before 29 Oct |
| `prompts/feedback-templates.md` | Wording for precise feedback | While reviewing |

All data is synthetic (as of 27 Oct 2026), built from the demo dataset in `demo-data/`.

## Steps

1. **Check the design system first.** New Claude Design projects inherit your organization's design system. If APAC is already set up as your organization's design system, don't attach file 04. If it isn't, ask whoever manages it to import APAC (from the GitHub repo, the design files, or `/design-sync` in Claude Code), or attach file 04 in round 1 as a fallback.
2. **Start a design.** In a Claude conversation, pick **Output → Design** in the message box (or open a Design template from the Artifacts tab). Keep the whole prototype in this **one project and chat**, so components and decisions carry from round to round.
3. **Round 1:** attach the files listed at the top of `prompts/round-1-overview-sessions-drawers.md` and paste everything below the `---` line. Claude will list the 7 artboards and its assumptions first. Correct anything wrong before it builds.
4. **Review round 1** on the canvas:
   - Leave inline comments on artboards, or write feedback in chat using `feedback-templates.md`.
   - Be specific: name the artboard and the element, and give exact values.
   - If a direction is unclear, ask for 2–3 alternatives of that one part.
   - Approve the round before moving on.
4a. **Round 1 started before 29 Oct?** Paste `prompts/round-1-patch-v0.3.md` once, with the updated files 01, 02 (JSON) and 05 attached. It applies the Host wording, the 中文 / EN toggle and the shared Comparison panel to your existing artboards.
4b. **Make it clickable:** after round 1 is approved, paste `prompts/round-1b-make-it-clickable.md`. It creates one interactive artboard, "P · Clickable prototype" (tabs, filters, table search and sort, drawers, Benchmark drawer, language toggle).
5. **Rounds 2–5, each followed by its prototype step:** run the round, review and approve its static artboards, then run `prompts/prototype-after-round-N.md`. That step extends the same prototype, so it always covers everything built so far:
   - Round 2 (Live Funnel, Host Analysis, host comparison) → `prototype-after-round-2.md`
   - Round 3 (Settings) → `prototype-after-round-3.md`
   - Round 4 (states) → `prototype-after-round-4.md` (states appear where they really happen)
   - Round 5 (responsive, dark) → `prototype-after-round-5.md` (resizing and theme switching)

   Why the static artboards come first each time: they are easier to comment on and fix; wiring a screen that hasn't been approved means wiring it twice.
6. **Round 6:** run the review prompt (it includes a click-by-click walkthrough of the prototype), let Claude fix what it finds, then use the handoff prompt to export the bundle for Claude Code.

## Round plan

| Round | Artboards | Covers |
|---|---|---|
| 1 | 7 | Shell (with 中文/EN toggle), Overview (All types, Influencer only, 中文), Sessions, Session drawer (Action Cards, Summary), Benchmark drawer; Comparison panel component |
| 1b | 1 | "P · Clickable prototype": the round 1 screens wired together |
| 2 | 7 | Live Funnel (Influencer, All types), Host Analysis, Host drawer (Summary, Sessions), compare selection, Host comparison |
| 2P | — | Prototype extended: Live Funnel, Host Analysis, host drawer, compare flow |
| 3 | 6 | Settings: users, invite, edit access, deactivate, data connections, no brand access |
| 3P | — | Prototype extended: Settings, demo "view as" roles |
| 4 | 8 | States: platform not connected, benchmark building, empty, loading, live / not enough data, error, compare limit |
| 4P | — | Prototype extended: states triggered by real use, simulated error |
| 5 | 7 | Tablet and mobile layouts, filters drawer, dark mode, host comparison on mobile |
| 5P | — | Prototype made responsive, with light / dark theme |
| 6 | — | Review against the design system, consistency, hierarchy, accessibility; handoff to Claude Code |

## Tips and known limits

- **No version history yet:** before a big change, ask Claude to duplicate the artboard first ("Duplicate 1.4 as 1.4b, then change…").
- **Comments:** inline comments sometimes don't appear. If one goes missing, check the comments view or paste the feedback into chat.
- **Record decisions in chat** ("Decision: … Reason: …"), so they carry into the handoff to Claude Code.
- **New chat:** re-attach files 01 and 02 and say which artboards already exist.
- **Standalone version:** the claude.ai/design version closes on 14 Dec 2026. Use Claude Design inside Claude (or `/design` in Claude Code).
