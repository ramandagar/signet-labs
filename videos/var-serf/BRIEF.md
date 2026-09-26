---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Agents don't fail. They're classified."
destination: youtube
aspect: 1920x1080
language: en
length: 48s
angle: feature-deep-dive
audience: engineers building resilient agent pipelines
style_preset: broadside
voice: am_michael
---

## Intent

Film 8 of the var-runtime launch series (docs/MASTER_VIDEO_PROMPT.md, slate
V8 · SERF SELF-CORRECTION). A flaky tool throws 503 → the structured error
object lands (category DEPENDENCY, recovery fallback_or_retry, backoff
[5, 15, 60]) → the agent retries on schedule → success. Hook: "Agents don't
fail. They're classified."

## Assets

- No site capture — no-capture path; brand tokens carried from var-hero.
- Verbatim strings from var_runtime/errors.py: 503 → DEPENDENCY; RECOVERY
  DEPENDENCY = {"strategy": "fallback_or_retry", "max_retries": 3,
  "backoff_seconds": [5, 15, 60]}; demo line `-> {'query': 'affected
  packages', 'results': ['pkg-a', 'pkg-b']} (after structured-error retry)`.
- Design system: frame.md + caption skin + fonts carried from var-hero.

## Customizations

- The raw error (`503 Service Unavailable`) strikes through; the structured
  object assembles field-by-field in its place.
- Backoff schedule renders as three mono ticks `5s · 15s · 60s`; retry
  lands on the sub-drop as the success row prints.
- Success row + end-card tick are the film's only greens (2). No amber, no
  red (the 503 itself is ink/muted — classification removes the drama).
- End card: series lockup, dead still ≥1.5s.

## Notes

- Autonomous run; local engines (Kokoro am_michael,
  HYPERFRAMES_PYTHON=/Users/raman/.venvs/hf-tts/bin/python).
