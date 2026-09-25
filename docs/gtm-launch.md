# GTM Launch Kit — var-runtime

Compliant growth only. We do NOT scrape emails: CAN-SPAM fines run to
$53k/violation, GDPR up to 4% of global turnover, and cold-mail off scraped
lists gets domains blacklisted (Google Postmaster / Spamhaus) — which kills
the double-opt-in list we actually want. Every channel below is permissioned
or organic.

## 1. Positioning

**One line:** Your agent says done. Prove it.

**Category:** runtime infrastructure for autonomous agents (the admissibility
layer above durable execution — what Dapr/Catalyst attest, VAR decides).

**Enemy:** the self-report. "A log line saying 'All tests passed' is not
evidence."

**Proof assets:** 10 demo videos, live dashboard, tamper-detection clip,
`demo.py` in 2 seconds, 25 passing checks (13 gate evals + 7 core + 5 launch).

## 2. Launch-week channels (in order)

### Day 1 — Hacker News (Show HN)
Title: `Show HN: var-runtime – an open-source runtime that gates AI agents on verifiable proof`
First comment by founder: the trust-gap story, the demo.py GIF, honest
"what's MIT vs paid" split. Reply to every comment for 48h.

### Day 1 — Reddit (respect each sub's rules; post as discussion, not ad)
- r/LocalLLaMA, r/MachineLearning (Discussion flair), r/ExperiencedDevs,
  r/selfhosted, r/LangChain. Lead with the gate HALT→ADMIT clip, not the logo.

### Day 1–2 — X/Twitter launch thread (10 posts = the 10 videos)
Hook post: the 30s hero video + "Your agent says done. Prove it."
One feature per post: evidence gate, identity envelopes, cost governor,
crash-resume, SERF, attestation. Tag no one cold; let it spread.

### Day 2 — Communities (be a member first, not a drive-by)
LangChain + MCP + CrewAI Discords (#showcase), Temporal community (we
complement them), r/MCP. Answer agent-reliability questions for a week
before pitching anything.

### Day 3 — Directories & registries
- awesome-mcp-servers PR (we ARE an MCP server)
- MCP registry listing
- GitHub topics: ai-agents, mcp, llm, observability, verification
- Product Hunt prep for week 2 (needs hunter + gallery; the hero video is the
  40s demo)

### Week 2 — Content flywheel (2 posts/wk, each embeds a video)
1. "Why Your Agent Needs a Trust Layer: the Proof-or-Stop Manifesto"
2. "Identity Propagation in MCP: the Missing Primitive"
3. "We Tested Our Evidence Gate With 13 Adversarial Scenarios" (evals/gate_evals.py)
4. "Durable Execution vs Verifiable Execution"
5. "Building a Verifiable Agent Runtime With Zero Dependencies"

## 3. Permissioned email (the compliant list)

The only list is the waitlist (double opt-in, `POST /v1/waitlist` → confirm
click). Sequences fire ONLY on confirmed addresses:

1. **Confirm** — double opt-in click (already live)
2. **Welcome (on confirm)** — the manifesto + hero video. Unsubscribe in footer.
3. **D+2** — the tamper-detection clip + "run demo.py in 2 seconds"
4. **D+5** — the 13-scenario eval post + GitHub link
5. **Launch week** — "VAR is live" + Pro/Team tiers
6. **Monthly** — changelog + best community integration

Every email: single opt-out link, physical sender identity, no purchased or
scraped addresses ever. Newsletter tools (Listmonk self-hosted keeps the
zero-dependency story) or the built-in SMTP path.

## 4. Design partners (month 1–2)

5 teams from the waitlist/Discord who run agents in production. Offer: white-
glove setup + their claim types added to proofs.json upstream. Ask: the SOC 2
conversation + a case study.

## 5. Metrics that matter

- GitHub stars → clones ratio (real interest)
- `demo.py` completion (the aha moment) — instrument later
- waitlist confirm rate (target >60% = hook works)
- gate decisions on the hosted free tier (activation)

## 6. Launch-day runbook

1. Repo public, README GIF up front, MIT license, CONTRIBUTING + issue
   templates, `good first issue` labels
2. Pin the hero video to the repo README + X profile
3. Show HN at 7–9am ET (Tue–Thu best)
4. Founder in comment threads for 48h straight
5. Discord invite in every README footer
6. Waitlist email #6 goes out only after HN settles (don't bury the launch)
