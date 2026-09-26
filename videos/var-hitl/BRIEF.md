---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Some claims need a human. Chain the human to the proof."
destination: youtube
aspect: 1920x1080
language: en
length: 48s
angle: feature-deep-dive
audience: platform owners with compliance or sign-off requirements
style_preset: broadside
voice: am_michael
---

## Intent

Film 9 of the var-runtime launch series (docs/MASTER_VIDEO_PROMPT.md, slate
V9 · HUMAN-IN-THE-LOOP). A deploy claim HALTs (no approval); a Slack-style
approval card slides in; the senior engineer approves; the approval chains
INTO the signed envelope; ADMIT. Hook: "Some claims need a human. Chain the
human to the proof."

## Assets

- No site capture — no-capture path; brand tokens carried from var-hero.
- Verbatim strings from demo step 8 + proofs.json: `no approval -> HALT
  [EVIDENCE_MISSING]` / `after approval -> ADMIT (envelope approval_chain
  now: ['senior_engineer'])` / claim `deploy_to_production` requiring
  `approver_role: senior_engineer`.
- Design system: frame.md + caption skin + fonts carried from var-hero.

## Customizations

- The approval card is the household object: requester, claim
  deploy_to_production, role required senior_engineer, approve/deny.
- On approve, a chain link draws FROM the approval INTO the envelope's
  approval_chain field — the human literally enters the chain.
- HALT band amber; the ADMIT flip green #1; end-card tick green #2; no red.
- End card: series lockup, dead still ≥1.5s.

## Notes

- Autonomous run; local engines (Kokoro am_michael,
  HYPERFRAMES_PYTHON=/Users/raman/.venvs/hf-tts/bin/python).
