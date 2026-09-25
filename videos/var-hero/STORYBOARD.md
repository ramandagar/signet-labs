---
format: 1920x1080
duration: 83s
message: "Your agent says done. Prove it."
arc: PAS (pain known and urgent: agents self-report completion)
audience: engineering leaders running autonomous agents in production
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the ADMIT moment
---

## Video direction

- **Palette** — canvas near-black, surface +1; ink white/warm-gray; one
  accent blue. Status scarce: green exactly twice (ADMIT badge, final tick);
  amber = every stop; red once (tamper). Machine output mono; narrative in
  display ramp.
- **Motion** — long-tail settles only; `fromTo` entrances; VO-paced reveals
  (back ~50%, nothing at t=0); holds = subtle jitter at most.
- **Rhythm** — the ADMIT flip is the impact (BGM sub-drop lands on it,
  ~49s in the extended cut): flip then HOLD still. 05b–05d are the
  product-in-motion middle (research: Cursor-style grounded demos). F7
  near-still card chain.
- **Never** — browser chrome (except terminal), AI gradients, bokeh, bounce,
  front-load-freeze, floating screensaver, infinite loops, randomness.
- **Caption band** — bottom ~17% clear.

## Frame 1 — Says.

- scene: Agent claims land as big type — "tests passed", "payment sent", "shipped" — then the word SAYS. lands alone in warning amber
- duration: 5.163s
- poster: 4s
- transition_in: cut
- src: compositions/frames/01-says.html
- status: animated
- voiceover: "Your AI agent says tests passed. Says payments sent. Says shipped. Says."
- type: hook
- blueprint: kinetic-type-beats (Reproduce)
- focal: the swapped claim line (typeset, no asset)
- sfx: none (BGM accents carry)

Signature: the in-place hard-cut word-swap.
Scene 1 (0.0–1.0s): bare canvas, 3-layer depth (field + faint grid + vignette);
"Your AI agent says" enters per-word staggered,
centered, display ramp, ~50% width; smooth settle, no camera.
Scene 2 (1.0–3.2s): the tail hard-cut swaps (`discrete-text-sequence`) —
"tests passed" → "payments sent" → "shipped" — one per VO cue, prefix fixed;
mono ✓ glyphs punctuate in accent blue.
Scene 3 (3.2–5.2s): line collapses; "SAYS." slams dead-center in amber
(beat-slam register, smooth, no bounce); holds still to the cut.

## Frame 2 — Says is not evidence

- scene: A green log line "✓ All tests passed" types itself, then desaturates and is struck through by EVIDENCE_STALE — 847s old, bound to the wrong commit
- duration: 8.661s
- transition_in: cut
- src: compositions/frames/02-not-evidence.html
- status: animated
- voiceover: "A log line is not evidence. Fresh matters. Bound to the exact commit matters. You find out downstream — when it's expensive."
- type: pain_point
- blueprint: typewriter-reveal (Adapt)
- focal: terminal-simulator (installed block) running the log line
- roles: terminal = cutout hero, dim canvas = background
- sfx: none

Adapt: type-and-edit signature kept — the edit is the strike-through; payoff
= the two failed checks. Terminal via `terminal-simulator` block, brand-styled.
Scene 1 (0.0–2.2s): dark terminal (cutout ~55%, upper-third, shadow-stack);
"✓ All tests passed — agent self-report" types on with caret, reading
green-as-claimed.
Scene 2 (2.2–4.4s): on "not evidence" the line desaturates + strike sweep; verdict types beneath in amber mono: "EVIDENCE_STALE
— age 847s > max 300s".
Scene 3 (4.4–6.6s): second row on its cue: "EVIDENCE_UNBOUND — bound
commit_old123 ≠ commit_def456" (`code-typing`); rows stack, amber pills.
Scene 4 (6.6–8.7s): rows hold; display line lands low-center: "you find out
downstream"; jitter only; hold to cut.

## Frame 3 — Proof-or-Stop

- scene: The runtime intercepts: gate object slams HALT in amber between the agent and the action; recovery instructions stream beneath it
- duration: 11.883s
- transition_in: cut
- src: compositions/frames/03-proof-or-stop.html
- status: animated
- voiceover: "var-runtime intercepts every critical action. No valid evidence — the lifecycle stops. With machine-readable recovery, so the agent corrects itself and tries again."
- type: product_intro
- blueprint: kinetic-type-beats (Adapt)
- focal: the gate diagram (CLAIM → GATE → HALT)
- sfx: none

Adapt: full-screen beats, each its own move, resolving on the payoff — and
the payoff beat is the HALT object, not a word.
Scene 1 (0.0–2.6s): "var-runtime" + "intercepts every critical action"
per-word staggered; asymmetric 60/40 upper-third, display ramp.
Scene 2 (2.6–5.5s): rail self-draws (`svg-path-draw`): AGENT → GATE ◈ →
ACTION, accent-blue connectors, mono labels; center, ~70% width.
Scene 3 (5.5–8.2s): on "stops": GATE blooms, HALT badge slams between gate and action in amber
(beat-slam register, smooth); ACTION dims to 30%.
Scene 4 (8.2–11.9s): recovery streams under the rail, token-typed:
"recovery: re_run_tests" · "strategy: retry"; hold, subtle jitter, to cut.

## Frame 4 — Five lines

- scene: A terminal types `python3 demo.py` and the real 2-second lifecycle streams past; then the 5-line integration snippet pins beside it
- duration: 8.256s
- transition_in: cut
- src: compositions/frames/03b-install.html
- status: animated
- voiceover: "And it's small. One runtime, five lines, zero dependencies. Wrap any framework's tool calls — the gate does the rest."
- type: feature_showcase
- blueprint: prompt-type-submit-generate (Reproduce)
- focal: the terminal running demo.py
- roles: terminal = cutout hero, snippet card = supporting, canvas = background
- sfx: none

Signature: the ask types, the machine answers.
Scene 1 (0.0–2.5s): dark terminal hero (continuity with 02); `$ python3
demo.py` types with caret; a shimmer beat.
Scene 2 (2.5–5.5s): the REAL demo output streams fast (token-typed, mono):
session started → HALT EVIDENCE_STALE → re-run → ADMIT → chain verified —
each line landing on its own beat, green/amber semantic.
Scene 3 (5.5–8.5s): a snippet card pins beside the terminal (five lines of
the README integration code, blue keywords); one accent underline draws
under "gate_claim"; hold to cut.

## Frame 5 — The checks run

- scene: The actual decision object builds line by line — fresh ✓ · bound:commit_sha ✓ · content_hash ✓ · signed ✓ — each check landing on its own beat
- duration: 7.104s
- transition_in: cut
- src: compositions/frames/04-checks.html
- status: animated
- voiceover: "Now watch the gate work. Fresh. Bound to the exact commit. Hash intact. Signed by CI's own key."
- type: feature_showcase
- blueprint: agent-progress-theater (Reproduce)
- focal: the decision object card
- roles: decision card = cutout hero, dim canvas = background, BGM riser under = audio
- sfx: none (riser is in the bed)

Signature: rows arrive and CHECK OFF, one per spoken cue.
Scene 1 (0.0–1.4s): decision card seats center (~45%, 3 depth layers); header
types `gate.evaluate(claim: "tests_passed")` token-stream (`code-typing`); one scanning
shimmer passes — machine working.
Scene 2 (1.4–5.8s): four rows land one per VO cue — "fresh · 12s ≤ 300s" ·
"bound · commit_def456" · "content_hash · 7f3a…" · "signed · ci-key-1" — each
glyph flips to ✓ (badge-flip, blue → green tick); two
reveals in the back half.
Scene 3 (5.8–7.1s): rows hold; card edge brightens (keyword-glow register);
riser crests; hold to cut.

## Frame 6 — ADMIT

- scene: The decision flips to ADMIT in green; the attested hash chain links the event and extends; impact moment
- duration: 4.245s
- transition_in: cut
- src: compositions/frames/05-admit.html
- status: animated
- voiceover: "Admit. The decision itself is signed into a tamper-evident chain."
- type: benefit_highlight
- blueprint: agent-progress-theater (Adapt)
- focal: ADMIT badge + chain
- roles: ADMIT badge = cutout hero, hash chain = supporting, canvas = background
- sfx: none (sub-drop impact in the bed at this beat)

Adapt: receipt-completion signature — the badge flip IS the final check-off;
extended by the chain (`constellation-hub` connectors). Impact moment → STILL.
Scene 1 (0.0–1.0s): verdict flips HALT→**ADMIT** (badge flip) in green — first green in the film; sub-drop under it; card centered.
Scene 2 (1.0–2.6s): content hash shrinks + docks into mono chain blocks
beneath (self-drawing connectors); chain extends one block on "signed into".
Scene 3 (2.6–4.3s): everything holds STILL — no jitter; stillness reads
against the riser's release; hold to cut.

## Frame 7 — Crash, resume

- scene: The process dies mid-run (red X, session card flickers out), relaunches, and restores from checkpoint — "resumed at step 7 · meter intact"
- duration: 8.64s
- transition_in: cut
- src: compositions/frames/05b-resume.html
- status: animated
- voiceover: "When the process dies mid-run, the session resumes at the exact step it stopped. State intact, meter intact — no re-payment."
- type: benefit_highlight
- blueprint: agent-progress-theater (Adapt)
- focal: the session card dying and restoring
- roles: session card = cutout hero, step rail = supporting, canvas = background
- sfx: none

Adapt: working theater, but the machine RECOVERS instead of completes — the
receipt is the restored state. Signature kept: state mutation IS the demo.
Scene 1 (0.0–2.2s): a session card (console-style, step rail of 9 ticks,
~6 lit) mid-work; subtle progress shimmer; meter chip reads $1.42 / $2.00.
Scene 2 (2.2–4.0s): on "dies": the card flickers once and drops to 20%
opacity with a critical-red X stamp — hard stop, one frame of stillness.
Scene 3 (4.0–6.5s): on "resumes": the card relights from the checkpoint —
ticks 7-9 re-arm, a restore bar sweeps, "resumed at step 7 · meter intact"
types in mono; the meter chip still reads $1.42 (unchanged — the point).
Scene 4 (6.5–8.5s): hold, subtle jitter; the completed card reads on.

## Frame 8 — The meter was always running

- scene: A budget gauge drains toward the line; the model-route chip flips flagship→fast; at the line, a clean hard-stop card
- duration: 9.6s
- transition_in: cut
- src: compositions/frames/05c-cost.html
- status: animated
- voiceover: "Budgets are enforced, not suggested. Tokens, dollars, wall-clock. Irreversible work earns the flagship model — everything else routes cheap."
- type: benefit_highlight
- blueprint: dataviz-countup (Reproduce)
- focal: the budget gauge
- roles: gauge = cutout hero, route chip = supporting, canvas = background
- sfx: none

Signature: numbers are the hero; the camera pushes through them.
Scene 1 (0.0–2.5s): a big horizontal gauge (hairline track, blue fill)
counts up 62% → 79% on the VO's "enforced"; a mono chip reads
"flagship · $3.00/M in".
Scene 2 (2.5–5.0s): the route chip flips to "fast · $0.15/M" (badge flip)
as the gauge passes 80%; tiny sparkline of token spend ticks beneath.
Scene 3 (5.0–8.0s): gauge hits the line at 100%; a clean stop card slides
up: "BUDGET_EXCEEDED — session stopped" in amber; hold; the numbers read.

## Frame 9 — Who is really asking

- scene: A signed identity envelope (principal, permissions, expiry) slides into a tool call's _meta; the audit query answers below — every action, per user
- duration: 8.363s
- transition_in: cut
- src: compositions/frames/05d-identity.html
- status: animated
- voiceover: "Every call carries signed identity — who is really asking, and what they may do. Later, the audit trail answers for all of it."
- type: benefit_highlight
- blueprint: comparison-split (Reproduce)
- focal: envelope card ↔ audit rows
- roles: envelope = left panel, audit table = right panel, canvas = background
- sfx: none

Signature: two paired panels from opposite wings, mirrored tilts.
Scene 1 (0.0–2.5s): left panel enters: the identity envelope card — mono
fields principal: alice@co · perms: [read:repo, run:tests] · exp — with a
blue signature seal ring drawing closed.
Scene 2 (2.5–5.0s): right panel enters mirrored: a tool-call card whose
_meta line receives the envelope token (a highlighted slot fills); an
accent pill pops: "verified".
Scene 3 (5.0–8.5s): the right panel grows an audit table beneath — rows
land one per beat (agent-1 · run_tests · ADMIT / agent-2 · deploy · HALT);
hold; the two panels read as cause and record.

## Frame 10 — Tamper with it

- scene: Someone edits one row of history in the sqlite store — the chain verification names the exact broken entry: "entry 3: hash mismatch"
- duration: 5.12s
- transition_in: cut
- src: compositions/frames/06-tamper.html
- status: animated
- voiceover: "Edit one row of history — verification names the exact entry that broke."
- type: feature_showcase
- blueprint: typewriter-reveal (Adapt)
- focal: terminal-simulator running the SQL edit + verify output
- roles: terminal = cutout hero, dim canvas = background
- sfx: none

Adapt: type-and-edit signature — the EDIT is the tamper; payoff is the
verification's typed answer.
Scene 1 (0.0–1.8s): dark terminal (F2 continuity); SQL types with caret:
`UPDATE events SET principal='mallory' WHERE seq=3;`
Scene 2 (1.8–3.4s): one shimmer beat; chain row above shows five linked
blocks; third link desaturates + snaps — hairline crack in critical red.
Scene 3 (3.4–5.1s): verification types back fast, token-streamed: `verify:
entry 3 — hash mismatch (event modified or entries removed)` in red; entry
number reads big; hold to cut.

## Frame 11 — Bookend

- scene: Hook restated: "Your agent says done." → "Now it proves it." → var-runtime ◈ · open source · Proof-or-Stop
- duration: 5.696s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "Your agent says done. Now it proves it. var-runtime — open source. Proof-or-Stop."
- type: cta
- blueprint: titlecard-reveal (Reproduce — card chain)
- focal: the final lockup
- roles: lockup = hero, canvas = background
- sfx: none

Signature: near-still cards, one restrained move each; hard-cut seams; ends
on the logo held to the final frame.
Scene 1 (0.0–1.6s): card 1 "Your agent says done." — slide-up crossfade,
center, display ramp; near-still hold.
Scene 2 (1.6–3.2s): hard cut; card 2 "Now it proves it." — same seat, one
slide-up; "proves" carries the single green tick.
Scene 3 (3.2–5.7s): hard cut; card 3 the lockup: ◈ var-runtime ·
github.com/your-org/var-runtime · "Proof-or-Stop." — settles once, holds
absolutely still to final frame; BGM fades.
