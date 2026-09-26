---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Sixty seconds from clone to your first gated claim."
destination: youtube
aspect: 1920x1080
language: en
length: 60s
angle: demo
audience: engineers evaluating agent guardrails; want to touch the product now
style_preset: broadside
voice: am_michael
---

## Intent

Film 2 of the var-runtime launch series (docs/MASTER_VIDEO_PROMPT.md, slate V2 ·
60-SECOND INSTALL). The demo film: a terminal types the real clone-and-run
(`git clone … && python3 demo.py`), the REAL demo output streams (session →
HALT EVIDENCE_STALE → recovery `re_run_tests` → ADMIT → chain verified), and
the 5-line integration snippet builds beside it with `gate_claim` underlined.
Proof beat is product-in-motion only — no abstraction. Hook: "Sixty seconds
from clone to your first gated claim."

## Assets

- No site capture — no-capture path; brand tokens carried from videos/var-hero
  (frontend/style.css source of truth) into capture/extracted/tokens.json.
- Real demo output captured from `python3 demo.py` (this repo) — the terminal
  streams verbatim product strings, never invented ones.
- 5-line integration snippet verbatim from README.md.
- Design system: frame.md + .hyperframes/caption-skin.html + fonts carried from
  videos/var-hero (same house style, Broadside preset remixed onto brand).

## Customizations

- The film's spine IS the demo's arc: clone → session → HALT (amber) →
  recovery → ADMIT (the one green moment, music impact lands here) → 5-line
  snippet → chain verified → CTA bookend.
- `gate_claim` underlined in the snippet — the one function that matters.
- End card: `◈ var-runtime · github.com/signet-labs/var-runtime · Proof-or-Stop.`
  held dead still ≥1.5s.

## Notes

- Brand tokens: page #0d0d0d, surface #1a1a19, terminal wells #101010, ink
  #ffffff/#c3c2b7, muted #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a,
  accent blue #3987e5 (structure/keywords only), ADMIT green #0ca30c (≤2 uses),
  HALT amber #fab219 (every stop), incident red #d03b3b (≤2, none needed here).
- Type: Barlow display (lowercase, 700–900, −0.02em), IBM Plex Mono machine
  output (uppercase chrome 0.14em). Self-hosted woff2 from var-hero assets.
- Autonomous run; signed out of HeyGen → local engines (Kokoro am_michael,
  ~120 WPM calm male VO; MusicGen/local ambient bed).
- 9:16 cut delivered after the 16:9 master (re-frame, not re-animate).
