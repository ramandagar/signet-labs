---
format: 1920x1080
duration: 50s
message: "Minute 38 of 40. The process dies. Nothing is lost."
arc: disaster-recovery (kill it in front of them, restore it untouched)
audience: engineers running long unattended agent sessions
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the restored meter (~33s)
---

## Video direction

- **Palette** — page #0d0d0d, surface #1a1a19, terminal wells #101010, ink
  #ffffff/#c3c2b7, muted #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a.
  Accent blue #3987e5 = structure, restore bar, ticks. SEMANTIC LAW: green
  #0ca30c exactly TWICE (resume tick, end-card tick); red #d03b3b ONCE (the
  crash X); NO amber in this film.
- **Type** — Barlow display lowercase 700–900 −0.02em; IBM Plex Mono chrome
  and machine strings verbatim.
- **Motion** — fromTo + long-tail power3; the death beat is ONE still frame
  (0.5s, nothing moves — silence in the bed); the restore bar sweeps once;
  holds STILL.
- **Rhythm** — reveals on cue; the restored meter is the impact (sub-drop);
  bottom 17% clear.
- **Never** — bounce, randomness, invented strings, red anywhere but the X.

## Frame 1 — Minute 38

- scene: A session card mid-work: header `session s_f3c9… · run_tests`, a 9-tick rail with 6 lit, step counter `step 6 / 9`, meter line `$0.1854 / $2.00`; clock chip counts `minute 38` as the VO opens; everything calm and alive
- duration: 3.925s
- poster: 5.0s
- transition_in: cut
- src: compositions/frames/01-midwork.html
- status: animated
- voiceover: "Minute 38 of a 40-minute run. The process dies."
- type: hook
- blueprint: agent-progress-theater (Reproduce)
- focal: the living session card
- asset_candidates: session card (authored HTML); tick rail (authored); meter (mono, tabular)
- sfx: none

Scene 1 (0.0–2.2s): card on from the cut; ticks pulse in sequence (7th
about to fire).
Scene 2 (2.2–4.4s): clock chip `minute 38 / 40` counts in.
Scene 3 (4.4–5.5s): the 7th tick stalls halfway — hold.

## Frame 2 — The death

- scene: The card freezes; a red X stamps the corner; mono line prints `*** agent process crashes mid-PR-creation ***` then `exit 1`; then ONE still beat — the whole frame motionless (0.5s); bed cuts to near-silence
- duration: 5.867s
- poster: 6.0s
- transition_in: cut
- src: compositions/frames/02-death.html
- status: animated
- voiceover: "Normally that means re-run, re-pay, re-explain. Here, everything is already saved."
- type: problem
- blueprint: agent-progress-theater (Adapt — the anti-theater beat)
- focal: the crash line
- asset_candidates: red X stamp (authored SVG, red 1×); crash lines (verbatim); frozen card (continuity)
- sfx: bed drops out for the still beat

Scene 1 (0.0–1.4s): X stamps (red #d03b3b); rail desaturates.
Scene 2 (1.4–2.8s): crash line types verbatim; `exit 1` prints.
Scene 3 (2.8–6.5s): STILL — nothing moves; the words `re-run · re-pay ·
re-explain` sit muted beside the card; hold.

## Frame 3 — What was saved

- scene: The card's shadow peels into a checkpoint list: `messages` / `tool results ×7` / `approvals` / `meter $0.1854` — four hairline rows land per cue, each with a blue hash chip
- duration: 9.003s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/03-checkpoints.html
- status: animated
- voiceover: "Every step checkpointed — messages, tool results, approvals, the meter."
- type: product_intro
- blueprint: grid-card-assemble (Reproduce)
- focal: the checkpoint list
- asset_candidates: checkpoint rows ×4 (authored); hash chips (mono)
- sfx: none

Scene 1 (0.0–6.0s): rows land one per spoken cue; hash chips type.
Scene 2 (6.0–7.0s): footer chip `checkpointed after every call` types
under the rows; settle; hold.

## Frame 4 — Relaunch

- scene: The well prints `resume(s_f3c9…)`; a blue restore bar sweeps left→right under the card; the 6 dead ticks re-arm in sequence; counter snaps `step 6 / 9`
- duration: 6.208s
- poster: 5.8s
- transition_in: cut
- src: compositions/frames/04-resume.html
- status: animated
- voiceover: "Relaunch. The session resumes at the exact step it stopped."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the restore sweep
- asset_candidates: restore bar (authored); re-arming ticks (authored)
- sfx: none

Scene 1 (0.0–1.6s): `resume(s_f3c9…)` types; bar sweeps.
Scene 2 (1.6–4.6s): ticks re-arm one per beat.
Scene 3 (4.6–6.5s): counter snaps `step 7 / 9` as the 7th tick re-arms;
hold.

## Frame 5 — Nothing lost

- scene: The verbatim receipt prints as three mono lines: `resumed at step 7 — meter restored: {'tokens': 75500, 'usd': 0.1854, 'wall_clock_seconds': 0.0}` and `no re-execution: 7 completed tool results intact`; the meter chip re-renders UNCHANGED ($0.1854 / $2.00) and a green tick draws on it (green #1) exactly on the sub-drop; dead-still hold
- duration: 6.997s
- poster: 9.6s
- transition_in: cut
- src: compositions/frames/05-receipt.html
- status: animated
- voiceover: "State intact. Meter intact. Seven completed tool results — no re-execution, no re-payment."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the unchanged meter with its green tick
- asset_candidates: receipt lines (verbatim, authored well); meter chip (continuity); green tick (authored)
- sfx: riser (~2.4s) into sub-drop aligned to the tick

Scene 1 (0.0–3.4s): receipt lines type verbatim.
Scene 2 (3.4–5.2s): meter chip re-renders; riser; tick draws ON the drop.
Scene 3 (5.2–10.5s): DEAD STILL hold.

## Frame 6 — The point

- scene: "a heartbeat, not the work." builds center in display ramp; the words "heartbeat" muted, "the work." ink
- duration: 4.331s
- poster: 5.4s
- transition_in: cut
- src: compositions/frames/06-point.html
- status: animated
- voiceover: "The crash costs you a heartbeat. Not the work."
- type: benefits
- blueprint: kinetic-type-beats (Reproduce)
- focal: the statement line
- asset_candidates: statement line (typeset)
- sfx: none

Scene 1 (0.0–2.4s): line builds word-by-word.
Scene 2 (2.4–6.0s): second line lands muted: `the meter never blinked.`
beside a tiny frozen `$0.1854` chip; settle; hold STILL.

## Frame 7 — Bookend

- scene: "crash-proof by default." center; green tick draws after "default" (green #2); resolves to end card lockup: ◈ + var-runtime + `OPEN SOURCE · github.com/signet-labs/var-runtime` + `proof-or-stop.`; dead still ≥1.5s
- duration: 3.691s
- poster: 6.3s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "Crash-proof by default. var-runtime. Proof-or-Stop."
- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- focal: the end-card lockup
- asset_candidates: resolve line (typeset); end-card lockup (series family); ◈ mark (authored SVG)
- sfx: none

Scene 1 (0.0–2.4s): line builds; tick draws after "default".
Scene 2 (2.4–4.6s): line clears fully BEFORE the lockup arrives; lockup
assembles.
Scene 3 (4.6–6.5s): DEAD STILL ≥1.5s.
