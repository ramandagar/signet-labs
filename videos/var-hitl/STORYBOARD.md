---
format: 1920x1080
duration: 47s
message: "Some claims need a human. Chain the human to the proof."
arc: sign-off theater (halt, ask, sign, chain, admit)
audience: platform owners with compliance or sign-off requirements
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the ADMIT (~38s)
---

## Video direction

- **Palette** — page #0d0d0d, surface #1a1a19, terminal wells #101010, ink
  #ffffff/#c3c2b7, muted #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a.
  Accent blue #3987e5 = structure, the chain link, ticks. SEMANTIC LAW:
  amber #fab219 = the HALT band; green #0ca30c TWICE (ADMIT flip, end-card
  tick); NO red.
- **Type** — Barlow display lowercase 700–900 −0.02em; IBM Plex Mono chrome;
  machine strings verbatim.
- **Motion** — the approval card slides like a notification (one power3
  settle); the chain link draws from card INTO envelope; ADMIT flips on the
  sub-drop; holds STILL.
- **Rhythm** — bottom 17% clear; reveals on cue.
- **Never** — bounce, randomness, invented strings, red.

## Frame 1 — The thesis

- scene: "some claims need a human." builds center; second clause "chain the human to the proof." in blue; a tiny approval-card glyph seeds the idea
- duration: 3.413s
- poster: 5.0s
- transition_in: cut
- src: compositions/frames/01-hook.html
- status: animated
- voiceover: "Some claims need a human. Chain the human to the proof."
- type: hook
- blueprint: kinetic-type-beats (Reproduce)
- focal: the thesis line
- asset_candidates: statement (typeset); card glyph (authored)
- sfx: none

## Frame 2 — The halt

- scene: Decision card: the claim types `deploy_to_production` → verdict band snaps AMBER `HALT · EVIDENCE_MISSING`; the well prints verbatim `no approval -> HALT [EVIDENCE_MISSING]`; the missing field `approval_chain: []` glows hairline
- duration: 9.557s
- poster: 6.9s
- transition_in: cut
- src: compositions/frames/02-halt.html
- status: animated
- voiceover: "An agent wants to deploy to production. No approval in the chain — the claim halts. Evidence missing."
- type: problem
- blueprint: agent-progress-theater (Reproduce)
- focal: the amber halt band
- asset_candidates: decision card (authored); amber band; well line (verbatim)
- sfx: none

## Frame 3 — The ask

- scene: A Slack-style approval card slides in from the right and settles: header `approval requested`, rows `claim: deploy_to_production` / `requested_by: coder-1` / `role required: senior_engineer`, buttons `approve` / `deny` (hairline, inert)
- duration: 7.275s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/03-card.html
- status: animated
- voiceover: "The approval lands where humans live: who is asking, what claim, which role must sign."
- type: product_intro
- blueprint: device-surface-showcase (Adapt — one card, static stage)
- focal: the approval card
- asset_candidates: approval card (authored)
- sfx: none

## Frame 4 — The signature

- scene: A cursor-less click beat: the approve button fills ink once; a signature row prints `approved_by: eng.srña · role: senior_engineer · expires +3600s`; the card gains a signed seal
- duration: 6.08s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/04-sign.html
- status: animated
- voiceover: "A senior engineer reviews. Approves. The signature is real, scoped, and expiring."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the signature row
- asset_candidates: approve fill (authored); signature row (authored)
- sfx: none

## Frame 5 — Chained

- scene: Split stage: the signed card left, the envelope card right; a 1px blue chain link DRAWS from the signature into the envelope's `approval_chain: ['senior_engineer']` field as it types; the human is in the chain
- duration: 5.291s
- poster: 7.4s
- transition_in: cut
- src: compositions/frames/05-chain.html
- status: animated
- voiceover: "And the approval chains into the signed envelope — the human is now part of the proof."
- type: key_feature
- blueprint: camera-journey (Adapt — one link draw, no camera)
- focal: the chain link draw
- asset_candidates: signed card (continuity); envelope card (continuity of series envelope); link draw (authored)
- sfx: none

## Frame 6 — Admit

- scene: The decision card returns; verdict flips GREEN `ADMIT` on the sub-drop; the well prints verbatim `after approval -> ADMIT (envelope approval_chain now: ['senior_engineer'])`; dead-still hold
- duration: 3.179s
- poster: 5.4s
- transition_in: cut
- src: compositions/frames/06-admit.html
- status: animated
- voiceover: "Admit. The deploy proceeds — with a name attached."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the green admit flip
- asset_candidates: decision card (authored); green flip; well line (verbatim)
- sfx: riser (~2.2s) into sub-drop aligned to the flip

## Frame 7 — Bookend

- scene: "accountability, built in." center; green tick draws after "built in" (green #2); resolves to end card lockup (series lockup, URL verbatim); dead still ≥1.5s
- duration: 3.819s
- poster: 5.8s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "Accountability, built in. var-runtime. Proof-or-Stop."
- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- focal: the end-card lockup
- asset_candidates: resolve line (typeset); end-card lockup (series family)
- sfx: none

Scene 1 (0.0–1.6s): line builds; tick draws. Scene 2 (1.6–3.8s): clears
fully BEFORE lockup; lockup assembles. Scene 3 (3.8–6.0s): DEAD STILL ≥1.5s.
