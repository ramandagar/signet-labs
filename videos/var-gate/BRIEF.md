---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Five checks between a claim and your production."
destination: youtube
aspect: 1920x1080
language: en
length: 55s
angle: feature-deep-dive
audience: engineers evaluating agent guardrails; want the gate mechanics
style_preset: broadside
voice: am_michael
---

## Intent

Film 3 of the var-runtime launch series (docs/MASTER_VIDEO_PROMPT.md, slate
V3 · EVIDENCE GATE DEEP DIVE). The five checks as roll-call theater: each
check lands as a row and ticks on its spoken cue (present / fresh / bound /
hash-intact+signed / positive). Then each failure mode attacks — stale,
unbound, tampered, forged, negative — and HALTs with its verbatim code plus
machine-readable recovery. Hook: "Five checks between a claim and your
production." Bookend: "No evidence. No advance."

## Assets

- No site capture — no-capture path; brand tokens carried from videos/var-hero.
- Verbatim codes from var_runtime/evidence.py and proofs.json (the product's
  actual output): EVIDENCE_STALE / EVIDENCE_UNBOUND / EVIDENCE_HASH_MISMATCH /
  EVIDENCE_SIGNATURE_INVALID / EVIDENCE_NEGATIVE; recoveries re_run_tests /
  fix_and_re_run / produce_evidence.
- Design system: frame.md + caption skin + fonts carried from var-hero.

## Customizations

- Roll-call: five rows tick blue one per spoken cue, then the verdict ADMITs
  (green use #1) — the checks are shown working before anything fails.
- Failure theater: one attack per beat, each HALTs amber with its verbatim
  code + recovery chip; tampered bytes get the film's single red glyph.
- End card: `◈ var-runtime · github.com/signet-labs/var-runtime ·
  Proof-or-Stop.` held dead still ≥1.5s; final tick is green use #2.

## Notes

- Brand tokens: page #0d0d0d, surface #1a1a19, ink #ffffff/#c3c2b7, muted
  #898781, hairlines #d7d8d9 at 20–25%, grid #2c2c2a, accent blue #3987e5,
  ADMIT green #0ca30c (exactly 2), HALT amber #fab219 (all stops), red
  #d03b3b (1×, tamper glyph only).
- Autonomous run; signed out of HeyGen → local engines (Kokoro am_michael,
  HYPERFRAMES_PYTHON=/Users/raman/.venvs/hf-tts/bin/python).
