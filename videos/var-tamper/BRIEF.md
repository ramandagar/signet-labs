---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Edit one row of history. Watch it get caught."
destination: youtube
aspect: 1920x1080
language: en
length: 48s
angle: feature-deep-dive
audience: security-minded engineers and platform owners
style_preset: broadside
voice: am_michael
---

## Intent

Film 6 of the var-runtime launch series (docs/MASTER_VIDEO_PROMPT.md, slate
V6 · TAMPER EVIDENCE). A terminal types the SQL edit (`UPDATE events SET
principal='mallory' WHERE seq=3;`), the chain link cracks red, and
verification answers verbatim. Hook: "Edit one row of history. Watch it get
caught."

## Assets

- No site capture — no-capture path; brand tokens carried from var-hero.
- REAL captured output from this repo (demo bundle tampered, then verified):
  clean verify `{"chain_valid": true, "length": 17, "signed_by":
  "var-key-1"}` exit 0; after the edit, `var verify-bundle` answers
  `{"chain_valid": false, "error": "entry 3: hash mismatch (event modified
  or entries removed)"}` exit 1. These strings are verbatim product output.
- Design system: frame.md + caption skin + fonts carried from var-hero.

## Customizations

- Chain strip of 17 miniature blocks; entry 3 zooms and cracks RED (red use
  #1); the tampered principal `mallory` shows in the event body (red use #2).
- The verification JSON prints verbatim; `exit 1` lands as the punchline.
- Green appears ONCE (end-card tick). No amber.
- End card: `◈ var-runtime · github.com/signet-labs/var-runtime ·
  Proof-or-Stop.` dead still ≥1.5s.

## Notes

- Autonomous run; local engines (Kokoro am_michael,
  HYPERFRAMES_PYTHON=/Users/raman/.venvs/hf-tts/bin/python).
