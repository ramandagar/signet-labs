---
format: 1920x1080
duration: 46s
message: "Agents don't fail. They're classified."
arc: specimen-dissection (raw error in, structured plan out, success receipts)
audience: engineers building resilient agent pipelines
mode: autonomous
music: dark-tech minimal ambient, slow build, one impact at the success retry (~30s)
---

## Video direction

- **Palette** — page #0d0d0d, surface #1a1a19, terminal wells #101010, ink
  #ffffff/#c3c2b7, muted #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a.
  Accent blue #3987e5 = structure, the classification object, ticks.
  SEMANTIC LAW: green #0ca30c TWICE (success row, end-card tick); NO amber;
  NO red (the 503 renders ink/muted — classification removes the drama).
- **Type** — Barlow display lowercase 700–900 −0.02em; IBM Plex Mono chrome
  and error object verbatim.
- **Motion** — strikethrough draw on the raw error; object fields assemble;
  backoff ticks land per beat; retry lands on the sub-drop; holds STILL.
- **Rhythm** — bottom 17% clear; no front-loading.
- **Never** — bounce, randomness, invented strings.

## Frame 1 — Classified

- scene: Ghost watermark "?"; "agents don't fail." builds; second clause "they're classified." in blue; a tiny six-cell taxonomy strip (mono labels) slides in beneath
- duration: 2.795s
- poster: 4.0s
- transition_in: cut
- src: compositions/frames/01-hook.html
- status: animated
- voiceover: "Agents don't fail. They're classified."
- type: hook
- blueprint: kinetic-type-beats (Reproduce)
- focal: the reframe line
- asset_candidates: statement (typeset); taxonomy strip (authored)
- sfx: none

## Frame 2 — The 503

- scene: Terminal well; the raw error types: `503 Service Unavailable` with a muted `flaky_dependency: query_affected()` chrome above; the line strikes through once, muting
- duration: 9.813s
- poster: 5.4s
- transition_in: cut
- src: compositions/frames/02-503.html
- status: animated
- voiceover: "A flaky dependency throws 503 — service unavailable. To an agent, that's just a string."
- type: problem
- blueprint: prompt-type-submit-generate (Adapt)
- focal: the raw error struck through
- asset_candidates: well (authored); raw error (verbatim-ish product line); strike draw
- sfx: none

## Frame 3 — The object

- scene: The structured error object assembles field-by-field (mono, verbatim): `category: "DEPENDENCY"` / `strategy: "fallback_or_retry"` / `max_retries: 3` / `backoff_seconds: [5, 15, 60]`; the taxonomy strip highlights the DEPENDENCY cell
- duration: 9.877s
- poster: 7.9s
- transition_in: cut
- src: compositions/frames/03-object.html
- status: animated
- voiceover: "The runtime classifies it: category — dependency. Strategy — fallback, or retry. Three tries. Backoff at five, fifteen, sixty seconds."
- type: key_feature
- blueprint: grid-card-assemble (Reproduce)
- focal: the structured object
- asset_candidates: object card (authored); fields (verbatim); taxonomy strip continuation
- sfx: none

## Frame 4 — On schedule

- scene: Three backoff ticks land left-to-right: `5s` / `15s` / `60s` (mono chips on a 1px rail); a small wait cursor steps between them; no panic, no hammering — just the clock
- duration: 4.267s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/04-backoff.html
- status: animated
- voiceover: "The agent doesn't panic, and doesn't hammer. It retries on schedule."
- type: key_feature
- blueprint: spatial-pan-stations (Adapt — three stations, seated)
- focal: the backoff rail
- asset_candidates: backoff chips ×3 (authored); rail (authored)
- sfx: none

## Frame 5 — Success

- scene: The retry fires; the well prints verbatim: `-> {'query': 'affected packages', 'results': ['pkg-a', 'pkg-b']} (after structured-error retry)`; a green tick draws on the row (green #1) exactly on the sub-drop; dead-still hold
- duration: 5.355s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/05-success.html
- status: animated
- voiceover: "Same call, next window — the answer comes back, and the run continues."
- type: key_feature
- blueprint: agent-progress-theater (Reproduce)
- focal: the success row
- asset_candidates: well (authored); success line (verbatim); green tick
- sfx: riser (~2.2s) into sub-drop aligned to the tick

## Frame 6 — Six plans

- scene: The taxonomy strip returns full-width: `TRANSIENT / PERMANENT / AUTHENTICATION / RATE_LIMIT / VALIDATION / DEPENDENCY` — six cells land one per beat; caption line under: `six categories · six recovery plans`
- duration: 4.8s
- poster: 6.4s
- transition_in: cut
- src: compositions/frames/06-taxonomy.html
- status: animated
- voiceover: "Six categories. Six recovery plans. No string-parsing, ever again."
- type: benefits
- blueprint: grid-card-assemble (Reproduce)
- focal: the taxonomy strip
- asset_candidates: taxonomy cells ×6 (authored, verbatim labels)
- sfx: none

## Frame 7 — Bookend

- scene: "errors machines can use." center; green tick draws after "use" (green #2); resolves to end card lockup (exact series lockup, URL verbatim); dead still ≥1.5s
- duration: 3.883s
- poster: 5.8s
- transition_in: cut
- src: compositions/frames/07-bookend.html
- status: animated
- voiceover: "Errors machines can use. var-runtime. Proof-or-Stop."
- type: cta
- blueprint: logo-assemble-lockup (Reproduce)
- focal: the end-card lockup
- asset_candidates: resolve line (typeset); end-card lockup (series family)
- sfx: none

Scene 1 (0.0–1.6s): line builds; tick draws. Scene 2 (1.6–3.8s): clears
fully BEFORE lockup; lockup assembles. Scene 3 (3.8–6.0s): DEAD STILL ≥1.5s.
