---
workflow: product-launch-video
flow: automation
storyboard: no
message: "MCP doesn't say who's calling. We do."
destination: youtube
aspect: 1920x1080
language: en
length: 55s
angle: feature-deep-dive
audience: platform/agent engineers wiring MCP tools
style_preset: broadside
voice: am_michael
---

## Intent

Film 4 of the var-runtime launch series (docs/MASTER_VIDEO_PROMPT.md, slate
V4 · IDENTITY IN `_meta`). The envelope card (principal / agent / perms /
expiry, seal ring draws closed) slides into a tool call's `_meta` slot →
"verified" pill → the audit query answers with rows landing per beat. Hook:
"MCP doesn't say who's calling. We do."

## Assets

- No site capture — no-capture path; brand tokens carried from var-hero.
- Verbatim strings from the product: `io.var.identity.envelope = eyJhbGciOiJIUzI1NiIs…`,
  `{'path': 'src/auth.py', … 'read_as': 'alice@company.com'}` (also
  written_as / initiated_as), `audit query : 8 events acted on behalf of alice@…`,
  envelope fields principal/agent/permissions/approval_chain/expiry from
  var_runtime/identity.py.
- Design system: frame.md + caption skin + fonts carried from var-hero.

## Customizations

- Envelope card assembles field-by-field as the VO names them; the seal ring
  (blue, one draw-on) closes it.
- The `_meta` slot is the focal: the envelope docks INTO the tool call; the
  JWT line prints verbatim.
- Verified pill = green use #1; end-card tick = green use #2. No amber, no
  red in this film.
- End card: `◈ var-runtime · github.com/signet-labs/var-runtime ·
  Proof-or-Stop.` dead still ≥1.5s.

## Notes

- Autonomous run; signed out → local engines (Kokoro am_michael,
  HYPERFRAMES_PYTHON=/Users/raman/.venvs/hf-tts/bin/python).
