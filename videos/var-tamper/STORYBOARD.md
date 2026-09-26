---
format: 1920x1080
duration: 48s
message: "Edit one row of history. Watch it get caught."
arc: sting (give them the edit, then the receipt)
audience: security-minded engineers and platform owners
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the verification answer (~33s)
---

## Video direction

- **Palette** — page #0d0d0d, surface #1a1a19, terminal wells #101010, ink
  #ffffff/#c3c2b7, muted #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a.
  Accent blue #3987e5 = structure, chain links. SEMANTIC LAW: green #0ca30c
  ONCE (end-card tick); red #d03b3b TWICE (the crack glyph, the `mallory`
  value); NO amber.
- **Type** — Barlow display lowercase 700–900 −0.02em; IBM Plex Mono chrome;
  verification JSON verbatim in mono (never uppercase-chromed).
- **Motion** — fromTo + power3; the zoom into entry 3 is the one camera move;
  the crack draws once; holds STILL.
- **Rhythm** — reveals on cue; the JSON answer lands on the sub-drop; bottom
  17% clear.
- **Never** — bounce, randomness, invented strings.

## Frame 1 — The invitation

- scene: Ghost watermark "1 row"; "edit one row of history." builds word-by-word; a tiny 4-block chain glyph at the bottom; hold
- duration: 3.008s
- poster: 4.5s
- transition_in: cut
- src: compositions/frames/01-hook.html
- status: animated
- voiceover: "Edit one row of history. Watch it get caught."
- type: hook
- blueprint: kinetic-type-beats (Reproduce)
- focal: the statement line
- asset_candidates: statement (typeset); mini chain glyph (authored)
- sfx: none

Scene 1 (0.0–1.0s): ghost seats. Scene 2 (1.0–3.4s): words land. Scene 3
(3.4–5.0s): "watch it get caught." second clause in blue; hold.

## Frame 2 — The chain, intact

- scene: A strip of 17 miniature chain blocks (01–17) docks left→right, 1px blue links; the well prints verbatim: `{"chain_valid": true, "length": 17, "signed_by": "var-key-1"}`; stamp `exit 0`
- duration: 6.507s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/02-chain.html
- status: animated
- voiceover: "Seventeen events in the chain — every one hash-linked to the last."
- type: product_intro
- blueprint: grid-card-assemble (Reproduce)
- focal: the intact chain strip
- asset_candidates: chain blocks ×17 (authored, mini variant of series chain); verify JSON (authored well)
- sfx: none

Scene 1 (0.0–3.2s): blocks cascade in groups (fast stagger).
Scene 2 (3.2–5.4s): JSON line types verbatim.
Scene 3 (5.4–7.0s): `exit 0` chip; hold.

## Frame 3 — The edit

- scene: Terminal well; the SQL types verbatim with block caret: `UPDATE events SET principal='mallory' WHERE seq=3;`; a small `demo.db · events` chrome sits above
- duration: 5.269s
- poster: 7.4s
- transition_in: cut
- src: compositions/frames/03-edit.html
- status: animated
- voiceover: "Now the edit. One statement. One principal, changed — alice becomes mallory."
- type: problem
- blueprint: prompt-type-submit-generate (Reproduce)
- focal: the typing SQL
- asset_candidates: terminal well (authored); SQL line (verbatim)
- sfx: none

Scene 1 (0.0–1.4s): well rises; caret blinks.
Scene 2 (1.4–5.6s): the SQL types verbatim.
Scene 3 (5.6–8.0s): submit beat (caret holds); hold.

## Frame 4 — The silence

- scene: The chain strip returns; camera pushes gently into entry 03; its event body shows `principal: mallory` in RED (red #2) while neighbors stay alice; a thin red crack glyph draws across block 03 (red #1); everything else calm
- duration: 5.163s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/04-crack.html
- status: animated
- voiceover: "Nothing complains. The record looks perfectly normal."
- type: problem
- blueprint: zoom-out-workspace-reveal (inverse — push-in on one block)
- focal: the cracked entry
- asset_candidates: chain strip continuation (handoff from 02); event body card (authored); crack glyph (authored SVG)
- sfx: none (the stillness IS the beat)

Scene 1 (0.0–1.8s): strip re-forms; gentle push-in to block 03.
Scene 2 (1.8–4.0s): event body card opens: `principal: mallory` (red).
Scene 3 (4.0–5.2s): crack draws once across the block.
Scene 4 (5.2–7.0s): hold STILL.

## Frame 5 — The answer

- scene: The well runs `var verify-bundle session_bundle.json --key demo.key`; the JSON answer types verbatim: `{"chain_valid": false, "error": "entry 3: hash mismatch (event modified or entries removed)"}`; the `false` renders in red; chip `exit 1` stamps last, on the sub-drop
- duration: 4.8s
- poster: 6.9s
- transition_in: cut
- src: compositions/frames/05-verify.html
- status: animated
- voiceover: "But verification re-walks every hash. Entry three doesn't match anymore."
- type: key_feature
- blueprint: prompt-type-submit-generate (Reproduce)
- focal: the verbatim JSON answer
- asset_candidates: well + command (authored); answer JSON (verbatim); exit chip
- sfx: riser into sub-drop aligned to `exit 1` stamp

Scene 1 (0.0–2.2s): command types.
Scene 2 (2.2–5.6s): answer JSON types verbatim; `false` red.
Scene 3 (5.6–7.5s): `exit 1` stamps; hold.

## Frame 6 — Named

- scene: The error line re-set center, large, mono: `entry 3: hash mismatch (event modified or entries removed)`; beneath, three words land one per beat: `named.` `located.` `undeniable.` — display ramp
- duration: 10.347s
- poster: 7.4s
- transition_in: cut
- src: compositions/frames/06-named.html
- status: animated
- voiceover: "Entry three: hash mismatch — event modified, or entries removed. Named. Located. Undeniable."
- type: key_feature
- blueprint: kinetic-type-beats (Reproduce)
- focal: the three-word verdict
- asset_candidates: error line (verbatim, mono); verdict words (typeset)
- sfx: none

Scene 1 (0.0–2.2s): the line re-sets center.
Scene 2 (2.2–6.0s): `named.` / `located.` / `undeniable.` land one per beat.
Scene 3 (6.0–8.0s): hold STILL.

## Frame 7 — Bookend

- scene: "tamper-evident, by construction." builds center; green tick draws after "construction" (green, the film's only green); resolves to end card lockup: ◈ + var-runtime + `OPEN SOURCE · github.com/signet-labs/var-runtime` + `proof-or-stop.`; dead still ≥1.5s
- duration: 4.075s
- poster: 6.3s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "Tamper-evident, by construction. var-runtime. Proof-or-Stop."
- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- focal: the end-card lockup
- asset_candidates: resolve line (typeset); end-card lockup (series family); ◈ mark (authored SVG)
- sfx: none

Scene 1 (0.0–2.4s): line builds; tick draws. Scene 2 (2.4–4.6s): line
clears fully BEFORE lockup; lockup assembles. Scene 3 (4.6–6.5s): DEAD
STILL ≥1.5s.
