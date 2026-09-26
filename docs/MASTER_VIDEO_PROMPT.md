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
`github.com/your-org/var-runtime — open source · Proof-or-Stop.`

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
6. **End card:** `◈ var-runtime · github.com/your-org/var-runtime ·
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
F. ACCEPTANCE GATES (all must pass before you say "done" — and you
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
