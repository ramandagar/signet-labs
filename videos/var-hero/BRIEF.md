---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Your agent says done. Prove it."
destination: x-feed
aspect: 1920x1080
language: en
length: 40s
angle: launch
audience: engineering leaders running autonomous agents in production
style_preset: terminal-dark
voice: am_michael
---

## Intent

Hero launch video for var-runtime — the Verifiable Agent Runtime, an
open-source control layer that intercepts every critical agent action and
demands mechanically verifiable evidence before the lifecycle advances
(Proof-or-Stop). Modeled on the Raycast/Linear launch genre per
docs/video-research.md: hook in ≤8s, calm ~120 WPM male VO over precise
motion, 4 beats (Hook → Tension → Proof → CTA bookend), dark canvas, one
accent system (ADMIT green / HALT amber), real product UI, no stock.

## Assets

- /tmp/dashboard.png — real console screenshot (connected state, live data: sessions, gate chips, budget gauge) — Proof beat
- /tmp/landing.png — real landing page screenshot (hero + features) — CTA beat base
- frontend/style.css — the product's actual design tokens (source of truth for color/type)

## Customizations

- Gate HALT→ADMIT sequence rendered as the actual decision object animating (checks: fresh / bound / hash / signed)
- Tamper-detection moment: one chain link edited → verification names the broken entry
- Bookend CTA restating the hook line + repo URL

## Notes

- Brand tokens (validated on dark surface): page #0d0d0d, surface #1a1a19, ink #ffffff/#c3c2b7, muted #898781, series blue #3987e5, ADMIT/status good #0ca30c, HALT/warning #fab219, critical #d03b3b. Type: system-ui; machine output in ui-monospace.
- Accent color = meaning, never decoration. Green only for ADMIT, amber only for HALT.
- Autonomous run; user reviews the finished video 1 before videos 2–10 proceed.
- HeyGen signed out: Kokoro local voice (am_michael, calm male per research), MusicGen unavailable — ambient bed generated locally if needed.
