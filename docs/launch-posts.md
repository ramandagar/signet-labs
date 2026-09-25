# Launch posts — copy-ready

## Show HN

**Title:** Show HN: var-runtime – an open-source runtime that gates AI agents on verifiable proof

**Body:**

Every autonomous agent makes claims. It says it ran the tests. Says it sent
the payment. Says the migration is done. Those are self-reports — and a log
line that says "All tests passed" is not evidence that the tests correspond
to the code you're about to merge.

var-runtime is a control layer that sits between your agent framework and
its tools. When the agent makes a critical claim, the runtime demands
mechanically verifiable evidence before the lifecycle advances:

- **Evidence Gate (Proof-or-Stop):** a claim like `tests_passed` is only
  ADMITted when the CI artifact is present, fresh (age ≤ max_age_seconds),
  bound to the exact commit SHA, hash-intact, and signed by CI's own key.
  Otherwise: HALT, with a machine-readable recovery instruction the agent can
  act on ("re_run_tests").
- **Identity Broker:** every tool call carries a signed envelope (principal,
  agent, scoped permissions, approval chain, expiry) in the MCP `_meta` — the
  identity-propagation primitive MCP itself lacks.
- **Cost Governor:** token/USD/wall-clock budgets per session, stakes-based
  model routing, hard stop / degrade / escalate.
- **Durable state:** checkpoints after every tool call and LLM response; a
  crashed session resumes at the exact step it died. No re-execution, no
  re-payment.
- **SERF:** every tool failure classified into a six-category taxonomy with
  recovery strategy and backoff plan, so agents self-correct instead of
  parsing error strings.
- **Attestation:** every event hashed into a chain with linked batch
  signatures. Edit one row of the sqlite store and verification names the
  exact entry that broke.

Zero dependencies — Python stdlib only (sqlite3, hmac, hashlib). MIT.

    pip install nothing. python3 demo.py

`demo.py` runs the full lifecycle in ~2 seconds, including a crash-resume,
a stale-evidence HALT, and a tamper-detection pass. `evals/gate_evals.py`
runs 13 adversarial gate scenarios (all green).

There's a hosted tier for teams that want the dashboard, quotas, and RBAC —
the core runtime is and stays MIT. Asking because HN cares about that split:
happy to answer anything about the gate design or the attestation model.

## X launch thread (10 posts — one per video)

1/ Your AI agent says tests passed. Says payments sent. Says shipped.
* Says. *

var-runtime — the open-source runtime that makes agents prove it. 🧵
[hero video]

2/ A log line is not evidence. Fresh matters. Bound-to-the-commit matters.
The gate checks four things mechanically — and HALTs with instructions the
agent can execute. [video 3]

3/ No standard in MCP propagates WHO is calling. We ship signed identity
envelopes — principal, permissions, approval chain — in every tool call's
_meta. Per-user authorization for agents, finally. [video 4]

4/ Your agent crashed at minute 38 of 40. With var-runtime it resumes at the
exact step — state and meter intact. No re-execution. No re-payment.
[video 5]

5/ We tampered with our own database on camera. One row. Verification names
the exact broken entry. That's what "tamper-evident" means. [video 6]

6/ Agent economics: budgets per session, model routing by stakes (irreversible
work earns the flagship model, reversible goes cheap), hard stop at the line.
[video 7]

7/ Agents fail silently because error strings are unparseable. SERF returns
a category, a recovery strategy, and a backoff plan. The agent decides —
deterministically. [video 8]

8/ Deploys need a human when the stakes are high. The gate pauses the
lifecycle, Slack pings your senior engineer, the approval chains into the
signed envelope, then ADMIT. [video 9]

9/ 13 adversarial scenarios against the evidence gate: stale evidence, wrong
binding, tampered payloads, forged signatures, failing runs. 13 correct
verdicts. The suite ships in the repo. [video 2 or eval post]

10/ Everything above is Python stdlib. Zero dependencies. MIT.
github.com/your-org/var-runtime — Proof-or-Stop. [manifesto video]

## Reddit discussion post (r/LocalLLaMA etc.)

**Title:** We built a runtime that blocks AI agents from claiming "done" without verifiable proof — open source, zero deps

Body: short version of the HN post + the HALT→ADMIT clip + "happy to go deep
on the gate design". No link in title; link in body with context. Ask a real
question to start discussion: "What's your current story for trusting agent
self-reports — or do you just re-run everything?"

## Discord #showcase blurb

var-runtime (MIT, zero deps): an evidence gate for agent claims —
tests_passed only ADMITs with fresh, commit-bound, signed CI artifacts;
identity envelopes in MCP _meta; crash-resume; tamper-evident history.
2-second demo: `python3 demo.py`. Would love feedback from anyone running
agents unattended.
