# var-runtime — Run, Understand, and Test Everything

*The complete operator's guide. Every command below was run on 2026-09-26 and
its actual output is quoted. Nothing here is aspirational.*

---

## Part 1 — What problem are we solving? (plain words)

You have an AI agent doing real work: writing code, sending payments, editing
records. At the end it says **"done — tests passed."**

**That sentence is a claim, not a fact.** The log line saying "All tests
passed" proves nothing: the tests might be from 20 minutes ago (stale), from a
different commit than the one you're about to ship (unbound), edited after the
fact (tampered), signed by nobody (unverified), or the tests actually FAILED
and the agent misread it. Pipelines go green anyway. You find out at 3 a.m.
when production breaks — and nobody can say which claim was false.

**var-runtime is the referee that sits between your agent and everything it
touches.** Before any critical action advances, the agent must show
machine-checkable proof. Five checks, every time:

| Check | Question it answers |
|---|---|
| **present** | does any evidence exist at all? |
| **fresh** | was it produced within the time window (e.g. 300s)? |
| **bound** | does it pin the EXACT target (this commit, this payment id)? |
| **hash-intact + signed** | was it produced by a trusted source, unedited? |
| **positive** | does it actually say the thing PASSED? |

All five pass → **ADMIT**, the workflow continues. Any one fails → **HALT**,
and the agent gets a machine-readable recovery instruction
(`re_run_tests`) so it self-corrects instead of hallucinating success.

Around that gate, the runtime also: signs **who** is asking (identity
envelopes in every tool call), meters **what it costs** (budgets, model
routing), survives **crashes** (resume at the exact step), classifies every
**error** (so agents recover deterministically), and writes every event into
a **tamper-evident chain** (edit one database row and verification names the
exact broken entry).

---

## Part 2 — How it works, end to end (the 60-second version)

```
Your agent framework (LangGraph / CrewAI / any MCP client / plain Python)
        │  wraps every tool call + submits every claim
        ▼
┌─ VAR ──────────────────────────────────────────────┐
│ 1 verify identity ──► 2 check budget ──► 3 run tool │
│ 4 classify errors ──► 5 attest event  ──► 6 checkpoint│
│                                                    │
│ THE GATE: claim ──► evidence ──► 5 checks ──► ADMIT/HALT │
└────────────────────────────────────────────────────┘
        │  identity-injected, metered, attested calls
        ▼
Your tools: MCP servers, GitHub Actions, REST APIs, databases, files
```

Full interactive map with diagrams: **run the server and open `/architecture`**.

---

## Part 3 — Run it yourself (3 commands)

```bash
cd /Users/raman/Downloads/Projects/Signet

python3 demo.py          # the whole story in ~2 seconds: claims, HALTs,
                         # crash+resume, tamper detection, approvals, budget stop

python3 -m var_runtime.server --db var.db --port 8788
# → prints a one-time bootstrap admin key. Then open:
#   http://localhost:8788/              landing page
#   http://localhost:8788/app           the console (paste the key to connect)
#   http://localhost:8788/architecture  the full architecture map

python3 -m var_runtime.mcp_server --db var.db   # VAR as an MCP server (stdio)
```

---

## Part 4 — The test suites (run these any time)

```bash
python3 test_runtime.py      #  7/7 — the six core features
python3 test_launch.py       #  5/5 — API, billing, MCP, SDK, integrations
python3 evals/gate_evals.py  # 13/13 — adversarial gate scenarios
```

**Last full run (today): 25/25 green.** CI (`.github/workflows/ci.yml`) runs
all three on Python 3.11/3.12/3.13 on every push.

### What each suite proves

**Suite 1 — core (`test_runtime.py`)**
- Identity envelopes: sign → verify round-trip; tampered payload, expired
  token, and wrong key each rejected; permission scoping enforced.
- SERF: 503→DEPENDENCY, 429→RATE_LIMIT, "permission denied"→AUTHENTICATION,
  timeouts retry, "not found" never retries.
- Attestation: edit any event → chain names it; delete an entry → downstream
  hash mismatch; bundles verify offline.
- State store: checkpoints, latest, replay.
- Cost: exact USD math, hard-stop over budget, degrade at 80%, stakes
  routing (high→flagship, low→fast), percentiles.
- Gate: every rejection code.
- End-to-end: session → permission denial → SERF retries (2) → success →
  gate ADMIT → approval → crash → resume with meter intact → tampered DB
  row fails verification.

**Suite 2 — launch stack (`test_launch.py`)**
- Stripe webhook signatures: valid passes; wrong signature, tampered payload,
  and stale timestamps rejected.
- API end-to-end over dispatch: session create, HALT, approval, ADMIT,
  metering, verify, audit, resume, 401/403 on bad/cross-tenant keys,
  waitlist double opt-in, webhook plan upgrade, quota exhaustion (402),
  request records.
- A real HTTP server on a real port + the Python SDK against it.
- The MCP server as a real subprocess speaking JSON-RPC.
- GitHub fetcher (mocked API): pass, fail, binding; LangGraph gated_node.

**Suite 3 — adversarial evals (`evals/gate_evals.py`)**
The gate's judgment under attack — each row has exactly one correct verdict:

| scenario | verdict |
|---|---|
| fresh signed evidence | ADMIT |
| exactly at freshness boundary | ADMIT |
| no evidence at all | HALT EVIDENCE_MISSING |
| 847s old (>300s window) | HALT EVIDENCE_STALE |
| CI tested the wrong commit | HALT EVIDENCE_UNBOUND |
| payload edited after signing | HALT EVIDENCE_HASH_MISMATCH |
| signature from untrusted key | HALT EVIDENCE_SIGNATURE_INVALID |
| fresh, signed, tests FAILED | HALT EVIDENCE_NEGATIVE |
| confidence below floor | HALT CONFIDENCE_TOO_LOW |
| senior engineer approved deploy | ADMIT |
| junior tried to approve deploy | HALT EVIDENCE_MISSING |
| unregistered claim | raises CLAIM_UNKNOWN |
| history row edited | chain_valid = False |

---

## Part 5 — Live end-to-end walkthrough (what we ran today)

**Every product surface** (all 200):
`/` landing · `/app` console · `/architecture` · `/privacy` · `/terms` ·
`/favicon.svg` · `/healthz`

**The problem→solution arc over real HTTP** with the bootstrap key:
- create session → signed identity envelope issued
- claim `tests_passed` with no CI fetcher → HALT with SERF recovery
  (`FETCHER_MISSING / escalate_to_human`)
- senior-engineer approval recorded → deploy claim → **ADMIT**
- LLM metered: 40k in / 4k out → routed **flagship**, $0.18
- chain verified (`chain_valid: true`), gate decisions in the audit log

**The full gate arc on the local runtime (five claims, five verdicts):**
```
1. claim before CI ran        -> HALT  [EVIDENCE_MISSING]   recovery: re_run_tests
2. CI ran 847s ago (>300s)    -> HALT  [EVIDENCE_STALE]     recovery: re_run_tests
3. CI built the WRONG commit  -> HALT  [EVIDENCE_UNBOUND]   (bound old_sha != c1)
4. fresh, signed, but FAILED  -> HALT  [EVIDENCE_NEGATIVE]
5. fresh + bound + signed     -> ADMIT  [all 8 checks pass]
```
Then a simulated crash: new runtime process → `resume()` → same session,
chain still valid.

**Tamper detection through the CLI:**
```
before tamper: chain_valid = True | events: 2
>>> edited one history row: alice@co -> mallory@evil.io
after tamper:  chain_valid = False | entry 0: hash mismatch
cli.py exit code: 1        (CI-ready)
```

**Payments (signature-enforced, live):**
```
valid signature   -> 200 activated (plan: team -> pro, customer row created)
forged signature  -> 400 INVALID_SIGNATURE  (rejected)
tampered payload  -> 400 INVALID_SIGNATURE  (rejected)
```

**Waitlist double opt-in:** signup → `pending_confirmation` → confirm link →
`confirmed=1` stored. No confirmation click, no list membership.

**Rate limiting:** 61 rapid requests on a free key → the 61st returns **429**.

**Auth:** bad key → **401**; cross-tenant session access → **403** (suite 2).

**MCP server (raw stdio, exactly as Claude Desktop speaks it):**
```
initialize : var-runtime 0.1.0      tools: 7 exposed
gate HALT  : HALT - EVIDENCE_MISSING | recovery: re_run_tests
gate ADMIT : ADMIT                  chain: True
audit types: [gate_decision, session_started]
```

**JS SDK (Node, against the live server):** HALT → approve → ADMIT →
meter (`fast, $0.00021`) → verify true → sessions listed.

**Console in a real browser (Chromium):** key connect → 3 session rows with
live gate chips, detail pane, envelope, chain-intact badges.

**Load:** 300 requests / 50 concurrent threads → **295 req/s sustained,
zero errors**; rate limiter engages exactly at the plan boundary.

---

## Part 6 — Two real bugs this walkthrough found (and fixed)

This is why you run everything:

1. **Unsigned webhooks were accepted when `STRIPE_WEBHOOK_SECRET` was unset**
   (dev convenience = anyone could POST a plan upgrade in a misconfigured
   prod). **Fix:** fail closed — 503 `BILLING_UNCONFIGURED`; unsigned is
   never accepted.
2. **`python -m var_runtime.server` ran the file as `__main__`, creating a
   second module instance** — `ApiError` raised by `billing.py` was a
   different class than the one dispatch caught, turning clean 400s into
   500s over real HTTP (in-process tests never saw it). **Fix:** the
   `__main__` guard re-imports the package module; one class identity.

Both fixes are in, and all 25 checks re-ran green after.

---

## Part 7 — Honest tested/not-tested table

| Area | Status |
|---|---|
| Runtime core (6 features) | ✅ 25 automated checks + live walkthrough |
| Gate under adversarial input | ✅ 13 eval scenarios, all correct verdicts |
| API (auth, rate, quota, records, tenants) | ✅ suite + live HTTP + load (295 r/s) |
| Stripe billing logic | ✅ signatures + plan transitions, **test mode** — live Stripe keys still yours to add |
| Waitlist double opt-in | ✅ live; real SMTP delivery needs your credentials |
| MCP server | ✅ raw stdio protocol tests |
| SDKs | ✅ Python + JS against live HTTP |
| Console/landing/architecture | ✅ real-browser verification |
| Crash/resume, tamper detection | ✅ local + CLI |
| Docker image / CI runners | ⚠ written, runs stdlib-only — first real `docker build`/GitHub runner happens on your repo |
| Production deploy, TLS, domain | ◆ needs your accounts (Railway/domain) |
| HMAC → Ed25519 upgrade path | ◆ documented ceiling, deliberate |

---

## Part 8 — Your 5-minute smoke test (do this after any change)

```bash
python3 test_runtime.py && python3 test_launch.py && python3 evals/gate_evals.py && python3 demo.py | tail -4
```

All green → the product is behaving. Any red → that's a real regression, not
noise: every check asserts an exact verdict or value.
