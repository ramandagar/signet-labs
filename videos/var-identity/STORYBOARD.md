---
format: 1920x1080
duration: 55s
message: "MCP doesn't say who's calling. We do."
arc: mechanism-reveal (build the envelope, dock it, verify it, answer for it)
audience: platform/agent engineers wiring MCP tools
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the verified pill (~34s)
---

## Video direction

- **Palette** — page #0d0d0d, surface #1a1a19, terminal wells #101010, ink
  #ffffff/#c3c2b7, muted #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a.
  Accent blue #3987e5 = structure, seal ring, keywords. SEMANTIC LAW: green
  #0ca30c exactly TWICE (verified pill, end-card tick); NO amber, NO red in
  this film.
- **Type** — Barlow display lowercase 700–900 −0.02em; IBM Plex Mono chrome
  0.14em; machine strings verbatim in mono.
- **Motion** — fromTo + long-tail power3; the envelope dock is the signature
  move (card travels on a 1px blue rail into the slot, 0.6s power3.inOut);
  seal ring draws once; holds STILL.
- **Rhythm** — reveals on the spoken cue; the verified pill lands on the
  sub-drop; bottom 17% clear for captions.
- **Never** — browser chrome, AI gradients, bokeh, bounce, randomness,
  invented strings, green outside the two sanctioned moments.

## Frame 1 — Who's calling

- scene: Ghost watermark "?"; "who's calling?" builds word-by-word; a mono tool-call glyph `tools/call` pulses once with a small `?` chip; hold
- duration: 2.987s
- poster: 4.0s
- transition_in: cut
- src: compositions/frames/01-hook.html
- status: animated
- voiceover: "MCP doesn't say who's calling. We do."
- type: hook
- blueprint: kinetic-type-beats (Reproduce)
- focal: the who's-calling statement
- asset_candidates: statement line (typeset); tool-call glyph + ? chip (authored HTML)
- sfx: none

Scene 1 (0.0–1.0s): canvas + grid; ghost "?" seats behind center.
Scene 2 (1.0–2.8s): "who's calling?" builds word-by-word center; "we do."
lands second line in accent blue at 3.2s.
Scene 3 (3.2–4.5s): settle; hold still.

## Frame 2 — The call

- scene: A tool-call card enters: mono header `tools/call`, params block (`name: "read_file"`, `path: "src/auth.py"`); an EMPTY `_meta` slot at the card's foot glows hairline-blue — the vacancy is the point
- duration: 4.117s
- poster: 5.5s
- transition_in: cut
- src: compositions/frames/02-call.html
- status: animated
- voiceover: "Every tool call your agent makes carries a signed envelope."
- type: product_intro
- blueprint: agent-progress-theater (Adapt)
- focal: the empty _meta slot
- asset_candidates: tool-call card (authored HTML); _meta slot (authored)
- sfx: none

Scene 1 (0.0–2.0s): card rises in; header `tools/call` types.
Scene 2 (2.0–4.2s): params block types (`name: "read_file"` /
`path: "src/auth.py"`).
Scene 3 (4.2–6.0s): the empty `_meta` slot highlights (hairline blue, label
`_meta · empty`); hold.

## Frame 3 — The envelope assembles

- scene: Left of stage the envelope card builds field-by-field on the VO cue: `principal: alice@company.com` / `agent: coder-1` / `permissions: read:repo, run:tests` / `approval_chain: []` / `expiry: +300s`; the blue seal ring draws closed around the card's corner seal as the last field lands
- duration: 7.872s
- poster: 10.8s
- transition_in: cut
- src: compositions/frames/03-envelope.html
- status: animated
- voiceover: "Inside: the principal — a real human. The agent — and exactly what it may do. An approval chain. And an expiry."
- type: key_feature
- blueprint: grid-card-assemble (Reproduce)
- focal: the assembled envelope card
- asset_candidates: envelope card (authored HTML); field rows (authored); seal ring (authored SVG draw-on)
- sfx: none

Beats: field rows land one per spoken cue (principal 0.3s / agent+perms
2.9s / approval_chain 6.3s / expiry 8.3s); seal ring draws 9.6–10.6s; hold.

## Frame 4 — Into _meta

- scene: The envelope card travels right on a 1px blue rail and docks INTO the tool call's _meta slot (scale settle); the JWT line prints verbatim in the well: `io.var.identity.envelope = eyJhbGciOiJIUzI1NiIs…`
- duration: 10.624s
- poster: 8.4s
- transition_in: cut
- src: compositions/frames/04-dock.html
- status: animated
- voiceover: "The envelope rides the call itself — in the MCP underscore-meta slot. No side channel. No trust-me."
- type: key_feature
- blueprint: camera-journey (Adapt — one motivated move)
- focal: the docking moment
- asset_candidates: envelope card (continuity handoff from 03); rail (authored); well + JWT line (authored)
- sfx: none

Scene 1 (0.0–1.2s): both cards on stage; slot glows.
Scene 2 (1.2–2.6s): envelope docks (rail draws, card travels, settles at
scale 0.62 into the slot).
Scene 3 (2.6–6.4s): the JWT line types verbatim in the well.
Scene 4 (6.4–9.0s): `no side channel · no trust-me` chips land small under
the well; hold.

## Frame 5 — Verified

- scene: Server-side check rows tick: `signature ✓` / `expiry ✓` / `scope ✓`; the VERIFIED pill flips GREEN on the sub-drop with one ripple; dead-still hold
- duration: 9.472s
- poster: 7.6s
- transition_in: cut
- src: compositions/frames/05-verified.html
- status: animated
- voiceover: "The server verifies the signature, checks the expiry, enforces the scope — per user, per call."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the green verified pill
- asset_candidates: check rows (authored); verified pill (authored); ripple (authored)
- sfx: riser (~2.2s) into sub-drop aligned to the pill flip

Scene 1 (0.0–4.6s): three rows tick blue one per cue (signature 0.4 /
expiry 1.9 / scope 3.4) with chrome `per user · per call · not once at
login` appearing 4.4s.
Scene 2 (4.6–5.4s): bed dip; pill flips GREEN `verified` exactly on the
drop; single ripple.
Scene 3 (5.4–9.0s): DEAD STILL hold.

## Frame 6 — The audit answers

- scene: The well prints verbatim: `audit query : 8 events acted on behalf of alice@…`; four audit rows land beneath (tool reads/writes/commits with `as: alice@company.com`)
- duration: 7.723s
- poster: 8.4s
- transition_in: cut
- src: compositions/frames/06-audit.html
- status: animated
- voiceover: "And afterward, the audit trail answers: eight events, acted on behalf of alice."
- type: benefits
- blueprint: transcript-scroll-artifact-reveal (Adapt — rows land, no camera)
- focal: the audit answer line
- asset_candidates: answer line (authored well); audit rows ×4 (authored)
- sfx: none

Scene 1 (0.0–2.6s): the answer line types verbatim.
Scene 2 (2.6–6.4s): four rows land one per beat: `read_file src/auth.py ·
as alice@company.com` / `write_file src/auth.py · as alice@company.com` /
`run_tests commit_def456 · initiated alice@company.com` / `gate_claim
tests_passed · ADMIT`.
Scene 3 (6.4–9.0s): payoff line lands: `not the agent — alice` (typeset,
ink, the audit's point); hold STILL.

## Frame 7 — Bookend

- scene: "every call, signed." builds center; green tick draws after "signed" (green #2); resolves to end card lockup: ◈ + var-runtime + `OPEN SOURCE · github.com/signet-labs/var-runtime` + `proof-or-stop.`; dead still ≥1.5s
- duration: 3.392s
- poster: 6.3s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "Every call, signed. var-runtime. Proof-or-Stop."
- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- focal: the end-card lockup
- asset_candidates: resolve line (typeset); end-card lockup (series family); ◈ mark (authored SVG)
- sfx: none

Scene 1 (0.0–2.4s): line builds; green tick draws after "signed".
Scene 2 (2.4–4.6s): line clears (fully out BEFORE the lockup arrives — no
overlap); lockup assembles.
Scene 3 (4.6–6.5s): DEAD STILL ≥1.5s.
