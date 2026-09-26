---
workflow: product-launch-video
flow: automation
storyboard: no
message: "The meter was always running."
destination: youtube
aspect: 1920x1080
language: en
length: 50s
angle: feature-deep-dive
audience: teams burning money on unattended agent loops
style_preset: broadside
voice: am_michael
---

## Intent

Film 7 of the var-runtime launch series (docs/MASTER_VIDEO_PROMPT.md, slate
V7 · COST GOVERNOR). Budget gauge counts 62→79→100% (tabular numerals, blue
fill); route chip flips flagship→fast at 80%; clean amber `BUDGET_EXCEEDED —
session stopped` band ends the run. Hook: "The meter was always running."

## Assets

- No site capture — no-capture path; brand tokens carried from var-hero.
- Verbatim strings from `python3 demo.py`: `routed to : flagship cost=$0.18`
  / `PR-description call routed to cheap model: fast ($0.0054)` / `usage :
  {'tokens': 75500, 'usd': 0.1854, 'wall_clock_seconds': 0.012} (15.1% of
  budget)` / `session stopped : BUDGET_EXCEEDED — BUDGET_EXCEEDED: budget
  exceeded: ['usd']`.
- Design system: frame.md + caption skin + fonts carried from var-hero.

## Customizations

- The gauge is the hero object: tabular numerals, blue fill, one needle.
- Route chip flips flagship→fast at the 80% mark (stakes-based routing).
- The stop band is AMBER (BUDGET_EXCEEDED is a stop — semantic law); green
  appears ONCE (end-card tick); NO red.
- End card: `◈ var-runtime · github.com/signet-labs/var-runtime ·
  Proof-or-Stop.` dead still ≥1.5s.

## Notes

- Autonomous run; local engines (Kokoro am_michael,
  HYPERFRAMES_PYTHON=/Users/raman/.venvs/hf-tts/bin/python).
