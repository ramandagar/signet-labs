# Launch Video Research → Creative Rules (all 10 videos)

Sources studied: videngineer.com teardown of the Railway "vibe coding" ad
(0:45, ~8.7M impressions), Arcade's 2026 launch-video analysis, Raycast launch
week format, Linear/Stripe/Vercel launch genre conventions.

## What the pros do (evidence)

**Railway ad anatomy (13 cuts / 21 scenes, 45s):**
- 4 script beats: Hook (0:00) → Authority (0:13) → Proof (0:19) → CTA (0:41)
- ~22.6 cuts/min, avg shot 3.5s — fast montage over calm delivery
- Voice: calm, slow, ~120 WPM, meditative; contrast = memorability
- Sound: ambient pad ~70 BPM + ethereal synth accents at scene turns (0.8–1.1s),
  one tonal riser (~2.4s) into a sub-drop impact at the proof moment
- Bookend: opening promise returns as closing CTA
- Color: restrained 6-color palette, one dominant mood

**2026 launch-video traits (Arcade analysis):**
- ONE sharp value promise in the first 8 seconds (73% of viewers drop early)
- Real product usage beats abstract claims — show the actual UI doing the thing
- Benefits as outcomes, not specs; no jargon

**Dev-tool genre conventions:**
- Raycast: speed-cut real UI, cursor-driven focus, feature-per-second montage
- Linear: dark canvas, big confident type, slow reveals, almost no color
- Stripe/Vercel: one signature visual system (gradient / blueprint grid) held
  for the whole video; typography carries the narrative between UI beats

## House rules for VAR videos

1. **Hook ≤ 8s**: the one-liner. Ours: "Your agent says done. Prove it."
2. **4 beats**: Hook → Tension (what breaks without proof) → Proof (real
   runtime: gate HALT→ADMIT, tamper detection) → CTA bookend.
3. **Real product footage**: only the actual dashboard/CLI/runtime output,
   rendered at 60fps equivalent motion — no stock, no mockups.
4. **Pacing**: 30–60s; shot changes every 2.5–4s; calm VO ~120 WPM over
   precise motion (contrast principle from Railway).
5. **Sound**: ambient pad + synth accents at beat turns; one riser into an
   impact at the Proof moment. (HyperFrames BGM/SFX pipeline.)
6. **One visual system**: dark canvas (#0B0E14 family), one accent (verdict
   green #2BD576 / halt amber #F5A623), mono for machine output, sans for
   narrative. Accent color = meaning: green ADMIT, amber HALT. Never decor.
7. **CTA bookend**: close by restating the hook line + repo URL.

## The 10-video slate (order; each 30–60s)

1. **Hero launch** — "Your agent says done. Prove it." Full arc: agent claims
   done → gate HALT (stale evidence) → agent re-runs → ADMIT → attestation
   chain verified. *Ship first, user reviews before 2–10.*
2. The 60-second install (pip → 5 lines → first gated claim)
3. Evidence Gate deep dive (freshness/binding/hash/signature checks animating)
4. Identity envelopes in MCP `_meta` (per-user authorization, live audit)
5. Crash → resume (durable execution, meter intact, no re-payment)
6. Tamper-evidence (edit one event in sqlite → chain breaks at that entry)
7. Cost Governor (budget bar draining, model routing flip, hard stop)
8. SERF self-correction (503 → taxonomy → backoff → success, agent decides)
9. Human-in-the-loop (deploy blocked → Slack approval → envelope chained → ADMIT)
10. "Proof-or-Stop" manifesto (typographic, manifesto style, bookends the slate)

Every video ends: `github.com/your-org/var-runtime — Proof-or-Stop.`
