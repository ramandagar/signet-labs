# var-runtime — The Verifiable Agent Runtime

**Proof-or-Stop.** A control layer that sits between any agent framework and
the tools it invokes. Autonomous agents make claims — "tests passed", "payment
sent", "identity verified". The runtime intercepts every critical action,
demands mechanically verifiable evidence, and only then lets the lifecycle
advance. No evidence, no advance.

Model-agnostic, host-neutral, **zero dependencies** (Python ≥ 3.11, stdlib
only: sqlite3, hmac, hashlib, argparse, http.server).

```
┌─────────────────────────────────────────────────────────────┐
│                AGENT FRAMEWORK (any: LangGraph, …)          │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 VERIFIABLE AGENT RUNTIME                    │
│                                                             │
│  Evidence Gate · Identity Broker · Cost Governor            │
│  Durable State Store · Structured Errors (SERF)             │
│  Attestation & Provenance (hash chain + signatures)         │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│            TOOLS / MCP SERVERS / APIS / DATABASES           │
└─────────────────────────────────────────────────────────────┘
```

## The six features

| # | Feature | Where | What it enforces |
|---|---------|-------|------------------|
| 1 | **Evidence Gate** | `evidence.py` | A claim is ADMITted only with evidence that is present, right-typed, fresh (`max_age_seconds`), bound to the exact target (`must_bind_to`), hash-intact, signature-valid, and semantically positive. Otherwise HALT + machine-readable recovery instructions. |
| 2 | **Identity Broker** | `identity.py` | JWT-shaped signed envelope (principal, agent, scoped permissions, approval chain, expiry) injected into every tool call's MCP `_meta` as `io.var.identity.envelope`. Servers verify + enforce per-user authorization. |
| 3 | **Cost Governor** | `cost.py` | Per-session budgets (tokens / USD / wall-clock), metering of every LLM + tool call, stakes-based model routing (irreversible → flagship, reversible → fast), degrade/escalate/hard-stop on breach, rolling tool latency percentiles + failure rates. |
| 4 | **Durable State Store** | `state.py` | Checkpoint after every tool call and LLM response. Crash → `resume()` reloads the last checkpoint (messages, tool results, meter totals, approvals). No re-execution, no re-payment. |
| 5 | **Structured Error Semantics** | `errors.py` | Raw failures → taxonomy (TRANSIENT / PERMANENT / AUTHENTICATION / RATE_LIMIT / VALIDATION / DEPENDENCY) with recovery strategy, backoff plan, and retry context. Agents self-correct instead of parsing strings. |
| 6 | **Attestation & Provenance** | `attestation.py` | Dapr-style SHA-256 hash chain over every event, batch signatures linked to the previous signature, offline-verifiable export bundles. Tampering any event (or deleting one) breaks the chain at that point. |

## Quickstart

```bash
python3 demo.py            # the full 8-step lifecycle (Part 3 scenario), ~2s
python3 test_runtime.py    # 7/7 core feature checks
python3 test_launch.py     # 5/5 launch-stack checks (API, billing, MCP, SDK)
python3 evals/gate_evals.py  # 13/13 gate evaluation scenarios (CI-able)

python3 -m var_runtime.server --db var.db --port 8788   # hosted API + console (+ /architecture map)
python3 -m var_runtime.mcp_server --db var.db           # VAR as an MCP server
```

## The launch stack

| Piece | Where | What |
|---|---|---|
| **Hosted API** | `var_runtime/server.py` | REST over stdlib http: API-key auth (sha256 at rest, constant-time), per-plan rate limits, per-request `api_records`, session/gate/approval/meter/verify/audit endpoints, monthly gate-decision quotas, static hosting for the console + landing. `python3 -m var_runtime.server` |
| **Console + landing** | `frontend/` | Dark observability console (stat tiles, budget gauge, p50/p99 latency bars, gate feed, chain status — palette validated for the dark surface) + landing with double-opt-in waitlist and pricing. Served at `/` and `/app` by the API. |
| **Payments** | `var_runtime/billing.py` | Stripe Checkout (REST, no SDK) + webhook signature verification (HMAC-SHA256, 5-min replay window). `checkout.session.completed` upgrades the tenant's keys; failed payment / cancellation downgrades. Env: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_PRO`, `STRIPE_PRICE_TEAM`. |
| **MCP server** | `var_runtime/mcp_server.py` | VAR as an MCP server (stdio, JSON-RPC 2.0, spec 2025-11-25): 7 tools incl. `var_gate_claim`, `var_submit_evidence`, `var_record_approval`. Identity envelopes ride `tools/call` `_meta`. Claude Desktop config snippet in the module docstring. |
| **SDKs** | `sdk/python/`, `sdk/js/` | `VarClient` for Python (stdlib) and JS (fetch, browser + Node 18+). Same surface: sessions, gate claims, approvals, metering, verification, audit, billing. |
| **Integrations** | `var_runtime/integrations.py` | `github_actions_fetcher` (real Checks-API evidence, binding to head_sha, mocked tests) and the LangGraph adapter (`gated_node` raises `GateHalted` on HALT; `attach_checkpointer` bridges durable state, lazy import). |
| **Evals** | `evals/gate_evals.py` | Declarative scenario suite (DeepEval/promptfoo shape, zero deps): every ADMIT path, every HALT code, HITL role checks, tamper detection. Exit 1 on failure — wire into CI. |

Production notes: the API is single-threaded by design (sqlite + zero deps) —
put Caddy/nginx in front for TLS and run N processes on N ports to scale; set
`VAR_SIGNING_KEY` (stable signing), `VAR_SMTP_*` (real waitlist email),
`VAR_BASE_URL` (Stripe redirects). API records land in `api_records`; admin
keys read them via `GET /v1/records`.

### 5-line integration

```python
from var_runtime import VerifiableRuntime, Budget

rt = VerifiableRuntime(store="var.db", proofs="proofs.json")
s = rt.start_session(principal_id="alice@co", agent_id="coder-1",
                     permissions=["read:repo", "run:tests"],
                     budget=Budget(max_usd=2.00))

result = rt.call_tool(s, "read_file", my_mcp_tool, permission="read:repo",
                      path="src/auth.py")          # identity-injected, metered, attested
d = rt.gate_claim(s, {"claim": "tests_passed",
                      "target": {"commit_sha": sha}, "confidence": 0.97})
if d.admitted: ...                                  # else: d.error.recovery tells the agent what to do
```

The tool receives `meta={"io.var.identity.envelope": "<signed JWT>"}` — any
MCP server (or the `identity.verify` helper) can check the signature,
expiry, and permissions and log the acting principal.

### Proof Registry (`proofs.json`)

Claims map declaratively to evidence requirements; extend per domain:

```json
"tests_passed": {
  "evidence_type": "ci_test_result", "source": "ci_pipeline",
  "max_age_seconds": 300, "must_bind_to": ["commit_sha"], "recovery": "re_run_tests"
},
"deploy_to_production": {
  "evidence_type": "human_approval", "source": "approval_log",
  "approver_role": "senior_engineer", "max_age_seconds": 3600,
  "must_bind_to": ["deployment_id"], "min_confidence": 0.9
}
```

Register a fetcher per evidence source (`rt.gate.register("ci_pipeline",
fetch_fn)`); it returns a signed artifact produced by
`make_signed_artifact(...)` — CI signs with its own key, the runtime's trust
anchor registers that key.

## CLI

```
var sessions  [--db var.db]                       list sessions
var verify SESSION [--db] [--key demo.key]        hash-chain verification (exit 1 on tamper)
var audit SESSION [--principal P] [--type T]      queryable audit trail
var replay SESSION [--db]                         walk checkpoints
var verify-bundle bundle.json --key demo.key      offline attestation verification
var gate tests_passed [--proofs proofs.json]      show evidence requirement
var serve [--port 8787]                           HTTP verification API
```

API routes: `GET /sessions`, `GET /verify?session_id=…`,
`GET /audit?session_id=…&principal=…&type=…`.

Signing keys: pass `--key <file>` / `--key-hex` or set `VAR_SIGNING_KEY`.
`python3 demo.py` writes `demo.key` + `session_bundle.json` so you can
verify a real bundle immediately.

## What the demo shows

`python3 demo.py` runs the concrete scenario end to end: Alice's coding
agent fixes a bug — identity capture → flagship-routed planning →
envelope-injected tool calls (including a 503 flaky tool retrying via SERF)
→ the gate ADMITting fresh CI evidence, HALTing stale (847s > 300s) and
wrong-bound evidence (CI tested a stale checkout) → cost metering with
cheap-model routing → a crash with full resume (state + meter intact) →
chain verification + offline bundle + audit query → human-in-the-loop
approval gating a production deploy → budget hard stop.

## Design notes / ceilings

- **HMAC-SHA256 signing** (symmetric): anyone who can verify can also sign.
  Fine for a runtime trust anchor; swap `identity.TrustAnchor.sign/verify_sig`
  for Ed25519 (`cryptography` package) to let third parties verify without
  holding the signing key. Envelope format stays identical.
- **SQLite** is the only state backend. Postgres/S3/Redis adapters are the
  same four methods against a different driver — add when needed.
- **No framework adapters yet**: the runtime wraps plain callables, which any
  framework (LangGraph, CrewAI, OpenAI Agents SDK) can call through. A
  LangGraph checkpointer adapter is the natural next step.
- gRPC, dashboard, hosted cloud: not built here. The stdlib HTTP
  verification API covers the audit surface.

## Layout

```
var_runtime/           the runtime package (7 modules, one per feature)
proofs.json            default Proof Registry
demo.py                end-to-end scenario demo
test_runtime.py        assert-based checks (run directly)
cli.py                 `var` CLI + verification API
```

MIT licensed.
