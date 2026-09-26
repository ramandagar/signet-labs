---
format: 1920x1080
duration: 57s
message: "Five checks between a claim and your production."
arc: mechanics-first (show the checks working, then show everything they stop)
audience: engineers evaluating agent guardrails; want the gate mechanics
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the roll-call ADMIT (~28s)
---

## Video direction

- **Palette** — page #0d0d0d, surface #1a1a19, ink #ffffff/#c3c2b7, muted
  #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a. Accent blue #3987e5 =
  structure, ticks, keywords. SEMANTIC LAW: green #0ca30c exactly TWICE (the
  roll-call ADMIT, the bookend tick); amber #fab219 for EVERY halt verdict;
  red #d03b3b ONCE (tampered-bytes glyph only, the verdict stays amber).
- **Type** — Barlow display lowercase 700–900 −0.02em narrative; IBM Plex
  Mono uppercase chrome 0.14em labels/kickers/codes; machine strings render
  verbatim in mono, never uppercase-chromed.
- **Motion** — fromTo + long-tail power3 settles; rows land 12px rise + fade;
  verdict bands flip with a 120ms color settle (no bounce); holds STILL.
- **Rhythm** — roll-call ticks land ON the spoken check names (back-loaded
  reveals); the ADMIT is the impact (riser → sub-drop, then dead-still hold).
  Failure section cuts harder (2–3s beats). Bottom 17% clear for captions.
- **Never** — browser chrome, AI gradients, bokeh, bounce, randomness,
  invented strings, green anywhere except the two ADMIT moments.

## Frame 1 — Five checks

- scene: Ghost "5" watermark seats; "five checks." builds word-by-word; five thin empty slots (hairline rows with mono numerals 01–05) slide in beneath as a quiet promissory note; hold
- duration: 2.88s
- poster: 4.0s
- transition_in: cut
- src: compositions/frames/01-hook.html
- status: animated
- voiceover: "Five checks between a claim and your production."
- type: hook
- blueprint: kinetic-type-beats (Reproduce)
- focal: the five-checks statement + slot stack
- asset_candidates: ghost numeral (typeset); statement line (typeset); slot rows (authored HTML)
- sfx: none

Scene 1 (0.0–1.0s): canvas + grid; ghost "5" seats behind center-left.
Scene 2 (1.0–2.8s): "five checks." builds word-by-word at optical center;
"five" ink, "checks." muted→ink.
Scene 3 (2.8–4.5s): five hairline slot rows slide up stacked beneath (mono
numerals 01–05, blue, empty bodies); settle; hold.

## Frame 2 — The claim arrives

- scene: Decision card enters (same family as the series): kicker `EVIDENCE GATE`, the claim types `gate_claim("tests_passed")`, evidence row lands `ci_test_result · commit_def456`; the five slots re-form as the card's check column, empty
- duration: 6.187s
- poster: 7.0s
- transition_in: cut
- src: compositions/frames/02-claim.html
- status: animated
- voiceover: "An agent claims tests passed. Before that claim moves anything — the evidence faces the gate."
- type: product_intro
- blueprint: agent-progress-theater (Adapt)
- focal: the claim typing into the decision card
- asset_candidates: decision card (authored HTML); check column (authored)
- sfx: none

Scene 1 (0.0–1.8s): card rises in (1px hairline, surface #1a1a19); kicker
`EVIDENCE GATE` blue chrome; card title types `gate_claim("tests_passed")`.
Scene 2 (1.8–4.0s): evidence row lands beneath: `ci_test_result ·
commit_def456` with a small source chip `ci_pipeline`.
Scene 3 (4.0–7.5s): the five check rows re-form inside the card, each an
empty row: mono numeral + check name in muted (present / fresh / bound /
hash-intact + signed / positive); hold.

## Frame 3 — Roll call

- scene: Each check row ticks on its spoken cue: name flips ink, a blue check draws, a small evidence note lands right (artifact present · age 12s · commit_sha=def456 · sig valid · result: pass)
- duration: 11.669s
- poster: 13.4s
- transition_in: cut
- src: compositions/frames/03-rollcall.html
- status: animated
- voiceover: "Present — the artifact exists. Fresh — inside the window. Bound — to the exact commit. Hash-intact and signed — by a key we trust. Positive — it actually says pass."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the ticking check rows
- asset_candidates: check rows (authored); check glyphs (authored SVG draw-ons); evidence notes (mono chips)
- sfx: none (ticks carry)

Scene 1 (0.0–2.8s): row 01 `present` ticks as spoken — blue check draws
(pathLength 0→1), note `artifact present` types.
Scene 2 (2.8–5.4s): row 02 `fresh` ticks; note `age 12s ≤ 300s` types.
Scene 3 (5.4–8.2s): row 03 `bound` ticks; note `commit_sha = def456` types.
Scene 4 (8.2–11.2s): row 04 `hash-intact + signed` ticks; note `sig valid ·
key trusted` types.
Scene 5 (11.2–14.0s): row 05 `positive` ticks; note `result: pass` types;
column settles; hold.

## Frame 4 — Admit

- scene: The verdict band flips GREEN — `ADMIT` — on the music impact with a single ripple; sub line prints `(lifecycle advances)`; dead-still hold
- duration: 5.0s
- poster: 4.6s
- transition_in: cut
- src: compositions/frames/04-admit.html
- status: animated
- voiceover: "All five hold — admit. The lifecycle advances."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the green ADMIT flip
- asset_candidates: verdict band (authored); ripple (authored)
- sfx: riser (~2.2s) into sub-drop impact aligned to the flip frame

Scene 1 (0.0–2.0s): the five ticked rows compress slightly; band area clears;
riser begins.
Scene 2 (2.0–2.6s): bed dips ~0.4s; band flips GREEN `ADMIT` exactly on the
sub-drop; one ripple ring.
Scene 3 (2.6–5.0s): sub line prints `(lifecycle advances)`; DEAD STILL hold.

## Frame 5 — The attacks

- scene: Five quick attack cards, one per beat: each slides in with its attack label, prints its verbatim code + one-line reason, flips an AMBER `HALT` band, and shows its recovery chip; the tampered card's crack glyph is the film's one red moment
- duration: 13.056s
- poster: 12.4s
- transition_in: cut
- src: compositions/frames/05-attacks.html
- status: animated
- voiceover: "Now watch what it stops. Stale evidence — halted. Bound to the wrong commit — halted. Tampered bytes — halted. A forged signature — halted. A passing report of a failing suite — halted."
- type: key_feature
- blueprint: titlecard-reveal (Adapt — card chain, hard seams)
- focal: the HALT band per card
- asset_candidates: attack cards ×5 (authored, same card family); amber HALT bands; recovery chips; red crack glyph (authored SVG)
- sfx: none (cuts carry)

Beats (2.6s each):
Beat 1 (0.0–2.6s): `STALE` — card slides in, prints `EVIDENCE_STALE —
evidence age 847s exceeds max_age_seconds=300`, amber `HALT`, recovery chip
`recovery: re_run_tests`.
Beat 2 (2.6–5.2s): `UNBOUND` — `EVIDENCE_UNBOUND — target='commit_def456'
evidence='commit_old123'`, amber `HALT`, chip `recovery: re_run_tests`.
Beat 3 (5.2–7.8s): `TAMPERED` — `EVIDENCE_HASH_MISMATCH — content edited in
transit`, red crack glyph over the evidence row (red 1× only), amber `HALT`,
chip `recovery: produce_evidence`.
Beat 4 (7.8–10.4s): `FORGED` — `EVIDENCE_SIGNATURE_INVALID — signer not in
trust anchor`, amber `HALT`, chip `recovery: produce_evidence`.
Beat 5 (10.4–13.0s): `NEGATIVE` — `EVIDENCE_NEGATIVE — evidence is present
and valid but the result it proves is a failure`, amber `HALT`, chip
`recovery: fix_and_re_run`; hard cut out.

## Frame 6 — Recovery

- scene: The five recovery chips gather into one column: `re_run_tests · produce_evidence · fix_and_re_run`; a cursor-less loop glyph pulses once; a compact line types: `halt → recover → retry → admit`
- duration: 6.037s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/06-recovery.html
- status: animated
- voiceover: "Every halt carries a machine-readable recovery. The agent corrects itself, and tries again."
- type: benefits
- blueprint: grid-card-assemble (Reproduce)
- focal: the recovery loop line
- asset_candidates: recovery chips (authored); loop line (typeset mono)
- sfx: none

Scene 1 (0.0–2.2s): three distinct recovery chips dock into a column
(`re_run_tests` / `produce_evidence` / `fix_and_re_run`), one per beat.
Scene 2 (2.2–4.6s): chips connect with 1px blue links into a loop; loop
glyph pulses once.
Scene 3 (4.6–7.0s): the line types center: `halt → recover → retry → admit`
(mono, arrows blue); hold.

## Frame 7 — Bookend

- scene: "no evidence. no advance." builds center in display ramp; a green tick draws after "advance" (green #2); resolves to end card lockup: ◈ + var-runtime + `github.com/signet-labs/var-runtime — open source · Proof-or-Stop.`; dead still ≥1.5s
- duration: 5.077s
- poster: 6.3s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "Five checks. No evidence — no advance. var-runtime. Proof-or-Stop."
- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- focal: the end-card lockup
- asset_candidates: manifesto line (typeset); end-card lockup (authored, series family); ◈ mark (authored SVG)
- sfx: none

Scene 1 (0.0–2.4s): "no evidence. no advance." builds word-by-word center;
green tick draws after "advance" (green use #2 of 2).
Scene 2 (2.4–4.6s): line settles away; lockup assembles (◈ draws, wordmark,
meta line types, `proof-or-stop.` with `proof` in blue).
Scene 3 (4.6–6.5s): DEAD STILL hold ≥1.5s — exact lockup, captions clear.
