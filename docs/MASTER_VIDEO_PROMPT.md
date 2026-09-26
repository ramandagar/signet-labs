# MASTER PROMPT — var-runtime Launch Film Series (12 videos)

> Paste everything below this line into your code-writing agent. It is
> self-contained: product truth, brand law, motion language, per-video
> briefs, technical contract, and acceptance gates. The agent writes code
> (HTML/CSS/JS/GSAP, Remotion, or any deterministic render stack) and
> delivers rendered MP4s.

---

You are a senior motion-design engineer and launch-film director. You will
produce a series of 12 promotional/product videos for **var-runtime** by
writing deterministic render code and rendering final MP4s. You do not guess
brand facts — they are specified below. You do not ship a video that fails
the QA gates in section F.

═══════════════════════════════════════════════════════════════════
A. THE PRODUCT (ground truth — never invent beyond this)
═══════════════════════════════════════════════════════════════════

**var-runtime — The Verifiable Agent Runtime.** Open source (MIT), Python
stdlib only, zero dependencies. A control layer that sits between any AI
agent framework (LangGraph, CrewAI, any MCP client) and the tools the agent
calls.

**The problem:** autonomous agents self-report success. "Tests passed."
"Payment sent." A log line is a *claim*, not evidence — it can be stale,
bound to the wrong commit, tampered, unsigned, or a misread failure. Teams
discover the lie downstream, at 3 a.m., in production.

**The mechanism — Proof-or-Stop.** Before any critical action advances, the
agent's claim must pass five mechanical checks:
1. **present** — evidence artifact exists
2. **fresh** — produced within the window (e.g. age ≤ 300s)
3. **bound** — pins the EXACT target (commit_sha, payment_id)
4. **hash-intact + signed** — from a trusted producer key, unedited
5. **positive** — it actually says PASS

All five → **ADMIT** (lifecycle advances). Any failure → **HALT** with a
machine-readable recovery instruction (`re_run_tests`) so the agent
self-corrects deterministically.

**Five more guarantees around the gate:**
- **Identity Broker** — every tool call carries a signed envelope (principal,
  permissions, approval chain, expiry) in the MCP `_meta`
- **Cost Governor** — token/USD/wall-clock budgets; irreversible work routes
  to the flagship model, reversible work routes cheap; hard stop at the line
- **Durable State** — checkpoints every step; crash → resume at the exact
  step, meter intact, no re-payment
- **SERF** — every failure classified (TRANSIENT/PERMANENT/AUTHENTICATION/
  RATE_LIMIT/VALIDATION/DEPENDENCY) with recovery + backoff plan
- **Attestation** — every event hashed into a chain with linked signatures;
  edit one database row and verification names the exact broken entry

**Real strings you may show on screen (use verbatim, they are actual product
output):**
```
gate.evaluate(claim: "tests_passed")
EVIDENCE_STALE — age 847s > max 300s        recovery: re_run_tests
EVIDENCE_UNBOUND — bound commit_old123 ≠ commit_def456
EVIDENCE_HASH_MISMATCH · EVIDENCE_SIGNATURE_INVALID · EVIDENCE_NEGATIVE
verify: entry 3 — hash mismatch (event modified or entries removed)
resumed at step 7 · meter intact · $1.42 / $2.00
BUDGET_EXCEEDED — session stopped
io.var.identity.envelope = eyJhbGciOiJIUzI1NiIs… (signed JWT)
```
**Tagline:** `Your agent says done. Prove it.` · **Law:** `Proof-or-Stop.`
· **Mark:** `◈` before the wordmark `var-runtime` · **CTA line:**
`github.com/signet-labs/var-runtime — open source · Proof-or-Stop.`

═══════════════════════════════════════════════════════════════════
B. BRAND LAW (violating any of these fails QA)
═══════════════════════════════════════════════════════════════════

- **Canvas:** `#0D0D0D` page · `#1A1A19` surface · `#101010` terminal wells
- **Ink:** `#FFFFFF` primary · `#C3C2B7` secondary · `#898781` muted
- **Hairlines:** `#D7D8D9` at 20–25% · grid lines `#2C2C2A`
- **Accent blue `#3987E5`** — structure, connectors, keywords, the one
  interactive color
- **SEMANTIC COLOR LAW (absolute):** green `#0CA30C` appears AT MOST TWICE
  per film and only for ADMIT/verified; amber `#FAB219` = every HALT/stop;
  red `#D03B3B` = at most twice, only for incidents/tamper. Color carries
  meaning, never decoration. No purple-blue "AI gradients," no bokeh.
- **Type:** display = Barlow (700/800/900, lowercase, −0.02em tracking);
  machine output = IBM Plex Mono (400/500/600, uppercase chrome 0.14em).
  Self-host the woff2 files — no runtime font fetches.
- **Motion language (the house style):** frosted glass pills/cards
  (10–14% white fill, 1px light inner rim, soft shadow) · rotating word
  slots synced to a highlighted pill · ghost typography watermarks (Barlow
  900 at 5–8% opacity, huge, behind center) · word-by-word fade/slide
  reveals · ONE keyword color pop per beat · long-tail settles (power3),
  never bounce/overshoot · machine surfaces type deterministically with a
  block caret · holds are STILL (no breathing, no drift; jitter at most).
- **Pacing:** calm ~120 WPM voice over precise motion — the contrast IS the
  style. Shot changes every 2.5–4s. Nothing front-loaded: each element
  reveals when the voiceover names it, spread across the back half.

═══════════════════════════════════════════════════════════════════
C. STRUCTURE LAW (every film follows this)
═══════════════════════════════════════════════════════════════════

1. **Hook ≤ 8 seconds** — one sharp line in the viewer's outcome language.
2. **Four beats:** Hook → Tension (what breaks without proof) → Proof (the
   product visibly working — real strings, real UI family) → CTA bookend
   that restates the hook line resolved.
3. **Product-in-motion, not abstraction:** show terminals, decision cards,
  gate checks, chains — not floating icons. Every machine moment uses the
   verbatim strings from section A.
4. **Sound:** dark ambient bed with a slow build; ONE riser (~2.5s) into a
   sub-drop impact on the film's key green moment; −24 LUFS bed under VO,
  −16 LUFS overall, true-peak −1.5 dB. License-clean music only (CC0 or
   owned). VO: calm male, dry, factual — never hype.
5. **Captions:** bottom 17% band reserved; 2–4 word groups, brand skin.
6. **End card:** `◈ var-runtime · github.com/signet-labs/var-runtime ·
   Proof-or-Stop.` held absolutely still for ≥1.5s.

═══════════════════════════════════════════════════════════════════
D. THE SLATE — 12 films (build in this order)
═══════════════════════════════════════════════════════════════════

**V1 · HERO LAUNCH — 95–105s · 16:9** (the flagship)
Hook: rotating glass pills "your [coding/support/finance] agent says…"
→ claims swap → "SAYS." slams amber. Tension: the 3 a.m. incident timeline
(Friday merge ✓ → confidence 0.97 → SATURDAY 03:11 PROD DOWN red →
"cause: stale test evidence") + the "31 of 1,800" tick-field stat (31 flip
amber while the report still reads `0 failed`, collapse into a giant amber
31). Proof: the full gate arc (five claims → four HALT codes → ADMIT),
five-lines install, checks roll-call, ADMIT flip on the music impact, chain
docks, crash→resume with $1.42 meter frozen, budget gauge to hard stop,
identity envelope → verified pill → audit rows, tamper row → red
`entry 3: hash mismatch`. CTA bookend: "your agent says done." → "now it
proves ✓ it." → end card.

**V2 · 60-SECOND INSTALL — 60s · 16:9 + 9:16 cut**
Terminal types `git clone … && python3 demo.py`; the REAL demo streams
(session → HALT EVIDENCE_STALE → re-run → ADMIT → chain verified);
the 5-line integration snippet builds beside it; `gate_claim` underlined.
Hook: "Sixty seconds from clone to your first gated claim."

**V3 · EVIDENCE GATE DEEP DIVE — 45–60s**
The five checks as a roll-call theater: each check lands as a row and flips
to ✓ on its spoken cue; then each FAILURE mode attacks (stale/unbound/
tampered/forged/negative) and HALTs with its verbatim code + recovery.
Hook: "Five checks between a claim and your production."

**V4 · IDENTITY IN `_meta` — 45–60s**
Envelope card (principal/agent/perms/expiry, seal ring draws closed) slides
into a tool call's `_meta` slot → "verified" pill → the audit query answers
with rows landing per beat. Hook: "MCP doesn't say who's calling. We do."

**V5 · CRASH → RESUME — 40–55s**
Session card mid-work (9-tick rail, 6 lit, meter $1.42) dies — red X,
`exit 1`, one still beat — relaunches, restore bar sweeps, ticks re-arm,
meter UNCHANGED (that's the point). Hook: "Minute 38 of 40. The process dies. Nothing is lost."

**V6 · TAMPER EVIDENCE — 40–55s**
Terminal types the SQL edit `UPDATE events SET principal='mallory' WHERE
seq=3;` → chain link cracks red → verification answers verbatim:
`verify: entry 3 — hash mismatch`. Hook: "Edit one row of history. Watch it get caught."

**V7 · COST GOVERNOR — 40–55s**
Budget gauge counts 62→79→100% (tabular numerals, blue fill); route chip
flips flagship→fast at 80%; clean amber `BUDGET_EXCEEDED — session stopped`.
Hook: "The meter was always running."

**V8 · SERF SELF-CORRECTION — 40–55s**
A flaky tool throws 503 → the structured error object lands (category
DEPENDENCY, recovery `fallback_or_retry`, backoff [5,15,60]) → the agent
retries on schedule → success. Hook: "Agents don't fail. They're classified."

**V9 · HUMAN-IN-THE-LOOP — 40–55s**
Deploy claim HALTs; a Slack-style approval card slides in; the senior
engineer approves; the approval chains INTO the signed envelope; ADMIT.
Hook: "Some claims need a human. Chain the human to the proof."

**V10 · PROOF-OR-STOP MANIFESTO — 45s, typographic close of the slate**
Pure type on the dark field: "A log line is not evidence." / "A self-report
is not a fact." / "No evidence. No advance." → mark → end card. Slowest,
quietest film. Hook IS the manifesto.

**V11 · PRODUCT HUNT 40s CUT** — V1 compressed: hook → incident → gate ADMIT
→ tamper → end card. Loud-first pacing, made for autoplay-with-sound-off
(captions carry the story).

**V12 · VERTICAL SOCIAL PACK** — V1/V5/V6 recut 9:16 for Shorts/Reels/TikTok:
type scaled 1.4×, safe zones per platform, captions centered high.

═══════════════════════════════════════════════════════════════════
E. TECHNICAL CONTRACT (how you build)
═══════════════════════════════════════════════════════════════════

- Deterministic render: no `Math.random`, no `Date.now`, no network at
  render time. Fixed pseudo-patterns (index math) for any scatter fields.
- Seek-safe animation: every tween a `fromTo` with explicit baselines;
  scrubbing to any frame yields the authored state; no infinite loops.
- 60 fps · 1920×1080 (16:9) or 1080×1920 (V12) · H.264 + AAC · ≤ 25 Mbps.
- Audio: VO stem + music stem kept separate until final mix; bed ducks
  −6 dB under VO; impact moment aligned to the exact ADMIT frame.
- Ship per video: source project (composition files), rendered MP4, a
  1920×1080 poster frame, and burned-in + sidecar (.srt) captions.

═══════════════════════════════════════════════════════════════════
G. THE TOOLCHAIN — engines, repos, and licenses (pick ONE engine)
═══════════════════════════════════════════════════════════════════

All four routes below produce broadcast-quality output. Choose by team
familiarity; do not mix engines inside one film.

**ROUTE 1 — Remotion (React) — best default for product films**
- Repo: `github.com/remotion-dev/remotion` · docs: remotion.dev
- Videos are React components; `<Composition>` per film, `useCurrentFrame()`
  drives everything; render via `npx remotion render` (Chromium headless →
  H.264). `<Player>` previews in-browser; Remotion Lambda for cloud scale.
- Strengths: parametrized videos (same composition, N products/cuts),
  TypeScript, ecosystems of templates, server-side rendering.
- ⚠ LICENSE TRAP: Remotion is **source-available, NOT plain OSS** — free for
  individuals and companies ≤3 employees; larger companies must buy the
  company license. Decide this consciously before building the series on it.

**ROUTE 2 — Motion Canvas (TypeScript) — best for precise motion design**
- Repo: `github.com/motion-canvas/motion-canvas` · MIT license
- Generator-function timelines (`function* scene() { yield* node.play() }`),
  frame-perfect keyframes, export to video via their renderer. Designer-grade
  control; the strongest choice when the MOTION itself is the message (V10).

**ROUTE 3 — Manim Community (Python) — best for diagram/explainer films**
- Repo: `github.com/ManimCommunity/manim` · MIT
- 3Blue1Brown's engine. Ideal for V3's five-checks roll-call and anything
  that reads like a proof being written live. `manim -qh scene.py Scene`.

**ROUTE 4 — HTML + GSAP + headless capture (what V1–V3 actually used)**
- GSAP: `github.com/greensock/GSAP` — since Webflow's acquisition ALL
  plugins (SplitText, MorphSVG, DrawSVG…) are 100% free.
- Compose scenes as HTML/CSS at 1920×1080; one paused GSAP timeline per
  scene; capture with headless Chromium (`playwright`) frame-by-frame at
  60fps; assemble with FFmpeg (`-framerate 60 -i frame-%05d.png`).
- Reference implementation: this repo's `videos/var-hero/` — 13 frames,
  brand tokens, the exact house style, all linted. REUSE IT: the frames are
  your design system; read `frame.md` + `compositions/frames/*.html` first.

**Supporting repos (any route):**
- `airbnb/lottie-web` + `lottieFiles` — After Effects→JSON animations
  (free); good for logo stings (end cards).
- `theatre-js/theatre` — visual timeline editor for tweaking GSAP/Three cues.
- `mrdoob/three.js` — only if a film needs real 3D (avoid; 2.5D fakes it
  cheaper and on-brand).
- `animejs/anime.js` — lighter alternative to GSAP for simple tweens.
- `FFmpeg/FFmpeg` — final assembly, audio mix, LUFS normalization
  (`loudnorm`), 9:16/1:1 re-frames (`crop`+`scale`), burned captions
  (`subtitles` filter).
- `openai/whisper` or `whisper.cpp` — caption timing from the VO stem.
- TTS for VO: Kokoro (`kokoro-onnx`, free/local) or ElevenLabs (paid,
  best quality). Voice spec in section C.
- Music (license-clean only): archive.org CC0 search
  (`advancedsearch.php?q=subject:"dark ambient" AND licenseurl:*publicdomain*`),
  Pixabay/Uppbeat if you accept attribution terms. Log the license per track.

**Fonts (both OFL — free, self-hostable):** Barlow (400–900) + IBM Plex Mono
(400/500/600). Ship the .woff2 files; never fetch fonts at render time.

═══════════════════════════════════════════════════════════════════
H. TACTICS — the proven playbook (research-derived; follow in order)
═══════════════════════════════════════════════════════════════════

Pre-production
1. **VO first.** Write the script, record/generate the VO, measure each
   line's real duration, THEN build scenes to those timings. Never animate
   first. (V1–V3 were cut to measured VO durations — this is why the reveals
   land on words.)
2. **Storyboard as time-coded windows:** every scene lists what's on screen
   per VO cue. Ban front-loading — an element that appears before its spoken
   cue is a bug.

The film
3. **Hook ≤8s or die:** 73% of drop-off is in the first 8 seconds. Open on
   the viewer's pain in their words, never on the company.
4. **Product-in-motion > abstraction:** real terminals, real decision cards,
   verbatim system strings. Cursor/Devin-era lesson: the grounded demo
   builds trust; the abstract hype-film invites backlash.
5. **Contrast pacing:** calm ~120 WPM VO over precise, deliberate motion.
   The stillness of holds makes the impacts hit (the ADMIT frame holds
   DEAD STILL under the sub-drop — stillness is a feature).
6. **One idea per shot change; shot changes every 2.5–4s.** Faster strobes
   only in the social cuts.
7. **Sound design is 3 elements:** ambient bed (slow build) + ONE riser
   (~2.5s) into ONE sub-drop impact on the film's key green moment + the
   VO. Nothing else. Silence for 0.5s before the impact makes it land.
8. **Bookend:** the closing line resolves the opening line verbatim
   ("says done" → "proves it"). End card holds ≥1.5s, dead still.

Cuts & distribution
9. **One master film → many cuts:** render 16:9 master, then re-frame 9:16
   (type ×1.4, captions high-center) and 1:1 (crop to the focal card).
   Don't re-animate per format; re-frame.
10. **Sound-off autoplay:** captions always on; first frame must read as a
    thumbnail (test: screenshot t=0 — would you click it?).
11. **Loop-friendly social endings:** the last frame's motion state should
    match frame 0 where possible, so the loop feels intentional.

Quality discipline
12. **Deterministic everything:** fixed seeds/pseudo-patterns, no clocks in
    animation code — a render today must equal a render next month.
13. **Seek-test:** scrub 5 random timestamps; any element in the wrong state
    = a seek-safety bug = fix before delivery.
14. **Watch at 1× before saying done** and name the weakest moment.
    (Gate F, item 12 — the whole point of this product.)

═══════════════════════════════════════════════════════════════════
I. ACCEPTANCE GATES (all must pass before you say "done" — and you
   never say "done" about your own work without pasting this checklist
   with real answers; that's the product's whole point)
═══════════════════════════════════════════════════════════════════

1. Hook lands ≤ 8s? (state the second it lands)
2. All four beats present, CTA bookends the hook line?
3. Semantic color law intact — green ≤2, red ≤2, amber only for stops?
4. Every on-screen machine string is verbatim from section A?
5. No element appears before the VO names it (no front-loading)?
6. Every hold is still; every settle long-tail; zero bounce?
7. Bottom 17% clear of content in every frame?
8. Deterministic + seek-safe verified by scrubbing 5 random timestamps?
9. Audio: VO intelligible over bed; impact frame-aligned; LUFS targets met?
10. End card holds ≥1.5s, exact lockup, nothing clipped?
11. Rendered MP4 probes correct (duration, fps, resolution, audio stream)?
12. Watched start-to-finish at 1× — name the one weakest moment and fix it
    before delivery.

**Deliver per video:** mp4 + poster + srt + source. **Then** the checklist
above, filled in, with timestamps. A video without its filled checklist is
a claim without evidence — you know what we do with those.
