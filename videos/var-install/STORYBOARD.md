---
format: 1920x1080
duration: 60s
message: "Sixty seconds from clone to your first gated claim."
arc: demo-led (show the product being installed and gate its first claim live)
audience: engineers evaluating agent guardrails; want to touch the product now
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the ADMIT moment (~34s)
---

## Video direction

- **Palette** — page #0d0d0d, surface #1a1a19, terminal wells #101010, ink
  #ffffff/#c3c2b7, muted #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a.
  Accent blue #3987e5 for structure, keywords, the caret, the `gate_claim`
  underline. SEMANTIC LAW: green #0ca30c exactly TWICE (the ADMIT flip, the
  final bookend tick); amber #fab219 for the one HALT; red #d03b3b UNUSED.
- **Type** — Barlow display lowercase 700–900 −0.02em for narrative; IBM Plex
  Mono for every machine surface, uppercase chrome 0.14em for labels/kickers.
  Terminal output is NEVER uppercase-chrome — it renders verbatim, lowercase
  as the product prints it.
- **Motion** — fromTo entrances only, long-tail power3 settles, no bounce.
  Terminal text types with a block caret (deterministic index math, no
  randomness). Holds are STILL. Shot changes every 2.5–4s inside frames.
- **Rhythm** — calm ~120 WPM VO; the ADMIT flip (~34s) is the impact: ONE
  riser (~2.5s) into a sub-drop, flip lands on the drop, then DEAD STILL
  hold. Nothing front-loaded; each element appears when the VO names it.
- **Caption band** — bottom ~17% clear of content in every frame.
- **Never** — browser chrome (terminal wells only), AI gradients, bokeh,
  bounce, infinite loops, randomness, invented product strings.

## Frame 1 — Sixty seconds

- scene: Ghost "60" watermark seats behind center; "sixty seconds." builds word-by-word in display ramp; a thin blue connector draws from the word "clone" to a terminal-prompt glyph, then to "gated claim" — the whole promise as one line; hold
- duration: 3.456s
- poster: 4.2s
- transition_in: cut
- src: compositions/frames/01-hook.html
- status: animated
- voiceover: "Sixty seconds from clone to your first gated claim."
- type: hook
- blueprint: kinetic-type-beats (Reproduce)
- focal: the sixty-seconds promise line (typeset, no asset)
- asset_candidates: ghost numeral watermark (typeset); promise line (typeset); prompt glyph (authored SVG, chrome of the terminal family)
- sfx: none (BGM opens)

Scene 1 (0.0–1.2s): canvas #0d0d0d + faint grid; ghost "60" (display ramp,
6% opacity) seats behind center; nothing else.
Scene 2 (1.2–3.4s): "sixty seconds." builds word-by-word (fade/slide, 12px
rise) left-anchored at optical center; "sixty" ink white, "seconds." muted
until the word lands.
Scene 3 (3.4–5.0s): a 1px blue connector draws from the line's start to a
small mono prompt glyph `❯`, then to a second clause "your first gated
claim." in accent blue; settle long-tail; hold still to the cut.

## Frame 2 — Clone and run

- scene: Terminal well (#101010, 1px hairline rim) slides up as hero; types `git clone https://github.com/signet-labs/var-runtime` with block caret; hard-cut second command `python3 demo.py`; repo meta chips (MIT · zero deps · python 3.11) land under the well as the VO names them
- duration: 7.019s
- poster: 8.0s
- transition_in: cut
- src: compositions/frames/02-clone.html
- status: animated
- voiceover: "One repo. Python three-eleven, standard library only. Clone it, run the demo — nothing to install."
- type: product_intro
- blueprint: prompt-type-submit-generate (Reproduce)
- focal: the typing terminal well
- asset_candidates: terminal well (authored HTML); meta chips (authored HTML); block caret (authored)
- sfx: none

Scene 1 (0.0–1.6s): terminal well rises 24px + fades in, caret blinking
(index-math blink, 0.53s period); prompt glyph `❯` in blue.
Scene 2 (1.6–4.8s): `git clone https://github.com/signet-labs/var-runtime`
types at ~28 chars/s, caret riding the last glyph.
Scene 3 (4.8–6.4s): line submits (caret holds one beat), hard-cut swap to
`❯ python3 demo.py` typed quickly.
Scene 4 (6.4–8.5s): three mono chips land under the well one per beat —
`MIT` · `ZERO DEPS` · `PYTHON 3.11+` (uppercase chrome, hairline borders) —
long-tail settle; hold.

## Frame 3 — Session opens

- scene: Same terminal continues: demo STEP 1 streams verbatim — `session : s_f3c9148991ac` then the signed envelope line; a slim identity chip (`envelope · signed`) docks right of the stream
- duration: 7.915s
- poster: 5.6s
- transition_in: cut
- src: compositions/frames/03-session.html
- status: animated
- voiceover: "A session opens. Identity is signed. The meter starts."
- type: product_intro
- blueprint: agent-progress-theater (Reproduce)
- focal: the streaming session block
- asset_candidates: terminal continuation (authored HTML); identity chip (authored HTML)
- sfx: none

Scene 1 (0.0–1.8s): STEP 1 header line types (`session : s_f3c9148991ac`);
session id renders in blue.
Scene 2 (1.8–4.2s): envelope line types: `identity envelope (signed):` then
`eyJhbGciOiJIUzI1NiIs…` (truncated with ellipsis, verbatim prefix).
Scene 3 (4.2–6.0s): identity chip docks right of the well (`ENVELOPE ·
SIGNED`, uppercase chrome); a meter chip `$0.00 / $2.00` fades in beneath
it; hold.

## Frame 4 — Halt

- scene: The claim card: `gate_claim("tests_passed")` types in a decision card; evidence row lands, then the verdict band flips AMBER — `HALT · EVIDENCE_STALE`; verbatim stream line prints under it: `evidence age 847s exceeds max_age_seconds=300`; recovery chip types `recovery: re_run_tests`
- duration: 8.213s
- poster: 9.4s
- transition_in: cut
- src: compositions/frames/04-halt.html
- status: animated
- voiceover: "The agent claims tests passed. The gate checks the evidence — and stops it cold. Stale. Eight forty-seven seconds old."
- type: key_feature
- blueprint: agent-progress-theater (Adapt)
- focal: the amber HALT verdict band
- asset_candidates: decision card (authored HTML, same card family as var-hero 04-checks/05-admit); verdict band (authored); recovery chip (authored)
- sfx: none

Scene 1 (0.0–2.4s): decision card enters (surface #1a1a19, 1px hairline);
kicker `EVIDENCE GATE` (blue chrome); the claim types in mono:
`gate_claim("tests_passed")`.
Scene 2 (2.4–4.6s): evidence row lands beneath: `ci_test_result · commit_def456`;
a small age field counts 0 → 847 fast (index-math, tabular numerals).
Scene 3 (4.6–6.4s): verdict band flips amber — `HALT` (display-weight) with
code `EVIDENCE_STALE`; the verbatim line prints under it in the well:
`evidence age 847s exceeds max_age_seconds=300`.
Scene 4 (6.4–10.0s): recovery chip types `recovery: re_run_tests` (blue
border); VO names "stale / eight forty-seven" over the still card; hold
DEAD STILL to the cut.

## Frame 5 — Admit

- scene: The re-run: same card, evidence row swaps to fresh (`age 0s`); checks roll call ticks present / fresh / bound / hash / signed; the verdict band flips GREEN — `ADMIT` — on the music impact; ripple ring; dead-still hold
- duration: 9.0s
- poster: 7.5s
- transition_in: cut
- src: compositions/frames/05-admit.html
- status: animated
- voiceover: "The recovery is machine-readable — re-run the tests. The agent does. Same claim, fresh evidence: admit."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the green ADMIT flip
- asset_candidates: decision card continuation (authored HTML); check roll-call rows (authored); verdict flip (authored)
- sfx: riser (~2.5s) into sub-drop impact aligned to the flip frame

Scene 1 (0.0–2.2s): card persists; recovery chip emits a small `↻ re-run`
pulse; evidence row swaps — `age 0s` (fresh).
Scene 2 (2.2–5.4s): five check rows land one per VO beat, each ticking blue:
`present` / `fresh` / `bound:commit_sha` / `hash-intact` / `signed`; BGM
riser starts ~5.4s.
Scene 3 (5.4–6.2s): 0.5s near-silence bed dip; the verdict band flips GREEN
— `ADMIT` (display weight) exactly on the sub-drop; ripple ring expands once
from the band.
Scene 4 (6.2–9.0s): DEAD STILL hold — no breathing, no drift; the sub line
`(lifecycle advances to 'tests passed')` already printed under the band.

## Frame 6 — Five lines

- scene: Split stage: left, the integration snippet builds line-by-line with a caret; right, a caption card "five lines." in display ramp; `gate_claim` underlines in blue as the VO says it; zero-deps chip rests under the snippet
- duration: 8.469s
- poster: 8.8s
- transition_in: cut
- src: compositions/frames/05b-five-lines.html
- status: animated
- voiceover: "Your whole integration is five lines. Wrap the tool calls. Gate the claim."
- type: benefits
- blueprint: typewriter-reveal (Adapt)
- focal: the snippet with the gate_claim underline
- asset_candidates: snippet card (authored HTML, terminal-family well); caption card (typeset); underline draw (authored)
- sfx: none

Scene 1 (0.0–1.4s): caption card lands left-of-center: "five lines."
(display ramp, lowercase 900); snippet well slides in right, empty with
caret.
Scene 2 (1.4–5.6s): snippet lines type in sequence (fast, ~4 lines/s):
`from var_runtime import VerifiableRuntime, Budget` / `rt = VerifiableRuntime(store="var.db", proofs="proofs.json")` /
`s = rt.start_session(...)` block / `d = rt.gate_claim(s, {...})` block /
`if d.admitted: ...` — keywords (`VerifiableRuntime`, `Budget`) muted blue.
Scene 3 (5.6–7.4s): `gate_claim` underlines — 2px blue line draws left→right;
caret parks at end.
Scene 4 (7.4–9.5s): under the well a mono chip: `ZERO DEPENDENCIES ·
PYTHON STDLIB ONLY`; hold still.

## Frame 7 — Chain verified

- scene: The attestation answer prints verbatim in the well — `chain verified : {'chain_valid': True, 'length': 17, ...}`; four chain blocks dock left→right connected by 1px blue links, the last stamped `signed_by: var-key-1`; all ink/muted/blue — no green here
- duration: 7.957s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/06-chain.html
- status: animated
- voiceover: "Every decision lands in a tamper-evident chain — verifiable offline, forever."
- type: benefits
- blueprint: grid-card-assemble (Reproduce)
- focal: the docking chain blocks
- asset_candidates: verification line (authored HTML in terminal well); chain blocks + connectors (authored, same family as var-hero 05-admit)
- sfx: none

Scene 1 (0.0–2.4s): the verification line types in the well (mono, verbatim
dict as the product prints it).
Scene 2 (2.4–5.2s): four blocks dock one per beat (12px drop + fade, power3),
1px blue connectors draw between as each pair completes.
Scene 3 (5.2–7.0s): `signed_by: var-key-1` stamp types at the chain head;
hold DEAD STILL.

## Frame 8 — Bookend

- scene: "sixty seconds. your first gated claim." resolves center in display ramp; collapses to the end card lockup: ◈ mark + var-runtime wordmark, `github.com/signet-labs/var-runtime — open source · Proof-or-Stop.`; one green tick appears after "gated claim" (green use #2); end card holds dead still ≥1.5s
- duration: 5.867s
- poster: 6.3s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "Sixty seconds. Your first gated claim. var-runtime — open source. Proof-or-Stop."
- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- focal: the end-card lockup
- asset_candidates: resolve line (typeset); end-card lockup (authored, same family as var-hero 07-bookend); ◈ mark (authored SVG)
- sfx: none (BGM resolves)

Scene 1 (0.0–2.2s): "sixty seconds. your first gated claim" builds
word-by-word center; the tick (green, #0ca30c) draws after "claim" as the VO
says it — green use #2 of 2.
Scene 2 (2.2–4.4s): line settles up and fades; lockup assembles: ◈ mark
(draws once, blue) + `var-runtime` wordmark; meta line types beneath:
`OPEN SOURCE · github.com/signet-labs/var-runtime`; statement line
`proof-or-stop.` with `proof` in blue.
Scene 3 (4.4–6.5s): end card holds DEAD STILL ≥1.5s — exact lockup, nothing
clipped, captions clear of the lockup.
