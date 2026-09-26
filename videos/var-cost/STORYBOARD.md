---
format: 1920x1080
duration: 50s
message: "The meter was always running."
arc: the-gauge (arithmetic that ends in a clean stop)
audience: teams burning money on unattended agent loops
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the hard stop (~33s)
---

## Video direction

- **Palette** — page #0d0d0d, surface #1a1a19, terminal wells #101010, ink
  #ffffff/#c3c2b7, muted #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a.
  Accent blue #3987e5 = gauge fill, numerals, structure. SEMANTIC LAW: amber
  #fab219 = the ONE hard stop (BUDGET_EXCEEDED band); green #0ca30c ONCE
  (end-card tick); NO red.
- **Type** — Barlow display lowercase 700–900 −0.02em; gauge numerals in IBM
  Plex Mono with tabular figures (font-variant-numeric: tabular-nums);
  machine strings verbatim.
- **Motion** — gauge counts via stepped deterministic increments (index
  math); the route chip flips once (no bounce); the stop band snaps; holds
  STILL.
- **Rhythm** — reveals on the spoken number; the stop lands on the sub-drop;
  bottom 17% clear.
- **Never** — bounce, randomness, invented strings, red, green beyond the
  tick.

## Frame 1 — The meter

- scene: Ghost watermark "$"; "the meter was always running." builds word-by-word; a tiny mono meter chip `$0.1854` blinks once; hold
- duration: 1.749s
- poster: 4.0s
- transition_in: cut
- src: compositions/frames/01-hook.html
- status: animated
- voiceover: "The meter was always running."
- type: hook
- blueprint: kinetic-type-beats (Reproduce)
- focal: the statement line
- asset_candidates: statement (typeset); meter chip (mono)
- sfx: none

## Frame 2 — Everything is counted

- scene: The well types the usage dict verbatim: `usage : {'tokens': 75500, 'usd': 0.1854, 'wall_clock_seconds': 0.012} (15.1% of budget)`; three small chips under it: `TOKENS` / `USD` / `WALL-CLOCK`
- duration: 7.403s
- poster: 6.9s
- transition_in: cut
- src: compositions/frames/02-metered.html
- status: animated
- voiceover: "Tokens, dollars, wall-clock — every call metered, per session."
- type: product_intro
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the verbatim usage line
- asset_candidates: well (authored); usage line (verbatim); chips ×3
- sfx: none

## Frame 3 — Stakes-based routing

- scene: Two call cards side by side: LEFT `plan_change → routed to : flagship cost=$0.18` (heavy border); RIGHT `pr_description → cheap model: fast ($0.0054)`; a small `irreversible` / `reversible` mono tag on each
- duration: 10.731s
- poster: 9.4s
- transition_in: cut
- src: compositions/frames/03-routing.html
- status: animated
- voiceover: "Planning a delicate change? Irreversible work — it routes to the flagship model. Writing a PR description? The fast model does it for a fraction of a cent."
- type: key_feature
- blueprint: comparison-split (Adapt — flat panels, mirrored entrance)
- focal: the two price tags
- asset_candidates: call cards ×2 (authored); price lines (verbatim)
- sfx: none

## Frame 4 — The climb and the flip

- scene: HERO GAUGE: a wide horizontal budget bar, blue fill, tabular numeral readout counts 62 → 79 (%); at 80 the route chip flips `FLAGSHIP → FAST` with a single tick sound-cue; count resumes 80 → 100
- duration: 6.656s
- poster: 7.4s
- transition_in: cut
- src: compositions/frames/04-gauge.html
- status: animated
- voiceover: "Watch the gauge. Sixty-two percent. Seventy-nine — and the route flips cheap before you reach the line."
- type: key_feature
- blueprint: dataviz-countup (Reproduce)
- focal: the gauge readout
- asset_candidates: gauge bar (authored); numerals (tabular mono); route chip (authored)
- sfx: none

## Frame 5 — Hard stop

- scene: The gauge hits 100 — freezes; the amber band snaps in: `session stopped : BUDGET_EXCEEDED — budget exceeded: ['usd']`; everything above desaturates one step; ripple once; DEAD STILL hold
- duration: 7.317s
- poster: 7.9s
- transition_in: cut
- src: compositions/frames/05-stop.html
- status: animated
- voiceover: "At 100 — hard stop. Budget exceeded. The session halts mid-run, on budget."
- type: key_feature
- blueprint: agent-progress-theater (Adapt — the receipt)
- focal: the amber stop band
- asset_candidates: frozen gauge (continuity); stop band (amber, verbatim)
- sfx: riser (~2.2s) into sub-drop aligned to the band snap

## Frame 6 — Enforced, not suggested

- scene: "budgets enforced — not suggested." builds center; "enforced" ink, "suggested" muted with a thin strikethrough draw
- duration: 2.347s
- poster: 5.4s
- transition_in: cut
- src: compositions/frames/06-enforced.html
- status: animated
- voiceover: "Budgets enforced — not suggested."
- type: benefits
- blueprint: kinetic-type-beats (Reproduce)
- focal: the statement line
- asset_candidates: statement (typeset); strikethrough draw (authored)
- sfx: none

## Frame 7 — Bookend

- scene: green tick draws after "Proof-or-Stop." line center (green, the film's only green); resolves to end card lockup: ◈ + var-runtime + `OPEN SOURCE · github.com/signet-labs/var-runtime` + `proof-or-stop.`; dead still ≥1.5s
- duration: 2.005s
- poster: 5.8s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "var-runtime. Proof-or-Stop."
- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- focal: the end-card lockup
- asset_candidates: resolve line (typeset); end-card lockup (series family); ◈ mark (authored SVG)
- sfx: none

Scene 1 (0.0–1.6s): `var-runtime. proof-or-stop.` center; tick draws.
Scene 2 (1.6–3.8s): clears fully BEFORE lockup; lockup assembles (exact
series lockup, URL verbatim). Scene 3 (3.8–6.0s): DEAD STILL ≥1.5s.
