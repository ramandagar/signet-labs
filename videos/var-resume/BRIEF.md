---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Minute 38 of 40. The process dies. Nothing is lost."
destination: youtube
aspect: 1920x1080
language: en
length: 50s
angle: feature-deep-dive
audience: engineers running long unattended agent sessions
style_preset: broadside
voice: am_michael
---

## Intent

Film 5 of the var-runtime launch series (docs/MASTER_VIDEO_PROMPT.md, slate
V5 · CRASH → RESUME). A session card mid-work (tick rail, meter running)
dies — one still beat — then relaunches, restores at the exact step, meter
UNCHANGED (that's the point). Hook: "Minute 38 of 40. The process dies.
Nothing is lost."

## Assets

- No site capture — no-capture path; brand tokens carried from var-hero.
- Verbatim strings from `python3 demo.py` STEP 6: `*** agent process crashes
  mid-PR-creation ***` / `resumed at step 7 — meter restored: {'tokens':
  75500, 'usd': 0.1854, 'wall_clock_seconds': 0.0}` / `no re-execution: 7
  completed tool results intact`.
- Design system: frame.md + caption skin + fonts carried from var-hero.

## Customizations

- The death beat: red X + `exit 1` mono line, then ONE still beat (0.5s,
  nothing moves) — the only red moment in the film.
- Restore bar sweeps, ticks re-arm, meter UNCHANGED — the meter is the hero.
- End card: `◈ var-runtime · github.com/signet-labs/var-runtime ·
  Proof-or-Stop.` dead still ≥1.5s; green budget: resume tick (#1) + end-card
  tick (#2).

## Notes

- Autonomous run; local engines (Kokoro am_michael,
  HYPERFRAMES_PYTHON=/Users/raman/.venvs/hf-tts/bin/python).
