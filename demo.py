"""End-to-end demo — the Part 3 scenario.

An autonomous coding agent (Alice's session) fixes a bug and opens a PR under
the full lifecycle: identity propagation, evidence gating, cost governance,
crash recovery, structured error recovery, attestation, human-in-the-loop.

Run: python3 demo.py   (writes demo.db + session_bundle.json, then cleans up)
"""

from __future__ import annotations

import os
import time

from var_runtime import Budget, TrustAnchor, VerifiableRuntime
from var_runtime.evidence import make_signed_artifact
from var_runtime.identity import META_KEY, verify as verify_envelope

DB = "demo.db"
BUNDLE = "session_bundle.json"


def beat(title: str) -> None:
    print(f"\n{'—' * 72}\n{title}\n{'—' * 72}")


# --- fake infrastructure: an MCP-ish filesystem server and a CI pipeline ------

fs: dict[str, str] = {}                        # the "repo"
ci_runs: dict[str, dict] = {}                  # commit_sha -> signed CI artifact


def mcp_read_file(meta: dict, path: str) -> dict:
    # Server-side enforcement SDK: verify the envelope, check permission.
    env = verify_envelope(meta[META_KEY], anchor=runtime.anchor,
                          require_permission="read:repo")
    return {"path": path, "content": fs.get(path, ""), "read_as": env.principal_id}


def mcp_write_file(meta: dict, path: str, content: str) -> dict:
    env = verify_envelope(meta[META_KEY], anchor=runtime.anchor,
                          require_permission="write:repo")
    fs[path] = content
    return {"path": path, "bytes": len(content), "written_as": env.principal_id}


def mcp_run_tests(meta: dict, commit_sha: str, *, passed: bool = True,
                  age_seconds: float = 0.0, built_sha: str | None = None) -> dict:
    env = verify_envelope(meta[META_KEY], anchor=runtime.anchor,
                          require_permission="run:tests")
    # CI signs the result with its OWN key; the runtime's trust anchor
    # registers ci-key-1 so the gate can verify it. `built_sha` models CI
    # silently testing a stale checkout.
    artifact = make_signed_artifact(
        "ci_test_result", "ci_pipeline",
        {"passed": passed, "suite": "pytest", "tests": 214,
         "failures": 0 if passed else 3, "runner": "gh-actions"},
        bindings={"commit_sha": built_sha or commit_sha}, anchor=ci_anchor,
        produced_at=time.time() - age_seconds)
    ci_runs[commit_sha] = artifact
    return {"commit": commit_sha, "passed": passed,
            "initiated_as": env.principal_id}


def flaky_registry_api(meta: dict, query: str, _failures: list[int] = [0]) -> dict:
    # Fails twice with 503 then succeeds — demonstrates SERF retry.
    _failures[0] += 1
    if _failures[0] <= 2:
        raise RuntimeError("registry api unavailable: HTTP 503")
    return {"query": query, "results": ["pkg-a", "pkg-b"]}


def ci_fetcher(req: dict, claim: dict) -> dict | None:
    return ci_runs.get(claim["target"].get("commit_sha"))


# --- Step 0: boot the runtime --------------------------------------------------

anchor = TrustAnchor.generate()                       # runtime signing key
ci_anchor = TrustAnchor.generate("ci-key-1")          # CI's own key
anchor.keys["ci-key-1"] = ci_anchor.keys["ci-key-1"]  # trust-anchor registry
with open("demo.key", "w") as f:                      # so the CLI can verify
    f.write(anchor.keys[anchor.active_key_id].hex())

runtime = VerifiableRuntime(store=DB, anchor=anchor, proofs="proofs.json",
                            retry_backoff_scale=0.0)  # demo: don't really sleep
runtime.gate.register("ci_pipeline", ci_fetcher)

# Step 1 — Session initialization
beat("STEP 1 — Session initialization (identity capture + budget)")
session = runtime.start_session(
    principal_id="alice@company.com", agent_id="agent-coder-01",
    permissions=["read:repo", "write:repo", "run:tests"],
    budget=Budget(max_tokens=500_000, max_usd=2.00, max_wall_clock_seconds=1800))
print(f"session        : {session.session_id}")
print(f"identity envelope (signed, first 60 chars):\n  {session.token[:60]}...")

# Step 2 — Agent work begins (metered planning call)
beat("STEP 2 — Agent plans (high-stakes LLM call routes to the flagship model)")
routed = runtime.llm_call(session, stakes="high", input_tokens=40_000, output_tokens=4_000)
print(f"routed to      : {routed['model']}  cost=${routed['cost_usd']}")

# Step 3 — Tool calls with identity propagation
beat("STEP 3 — Tool calls with identity propagation (envelope in MCP _meta)")
fs["src/auth.py"] = "def login(user, pw): ...  # BUG: no rate limit"
print(runtime.call_tool(session, "read_file", mcp_read_file,
                        permission="read:repo", path="src/auth.py"))
print(runtime.call_tool(session, "write_file", mcp_write_file,
                        permission="write:repo", path="src/auth.py",
                        content="def login(user, pw): ...  # fixed: rate limited"))
COMMIT = "commit_def456"
print(runtime.call_tool(session, "run_tests", mcp_run_tests,
                        permission="run:tests", commit_sha=COMMIT))

# SERF in action: the flaky registry API fails 503 twice, retries, succeeds.
print("\nSERF self-correction on a flaky dependency:")
result = runtime.call_tool(session, "registry_api", flaky_registry_api,
                           query="affected packages")
print(f"  -> {result} (after structured-error retry)")

# Step 4 — Evidence Gate: the critical moment
beat("STEP 4 — Evidence Gate (Proof-or-Stop)")
d = runtime.gate_claim(session, {"claim": "tests_passed",
                                 "target": {"commit_sha": COMMIT},
                                 "confidence": 0.97})
print(f"fresh evidence  -> {d.decision}  checks={d.checks}")

# stale evidence: CI ran 847s ago, max_age is 300s
runtime.call_tool(session, "run_tests", mcp_run_tests,
                  permission="run:tests", commit_sha=COMMIT, age_seconds=847)
d = runtime.gate_claim(session, {"claim": "tests_passed",
                                 "target": {"commit_sha": COMMIT},
                                 "confidence": 0.97})
print(f"stale evidence  -> {d.decision}  [{d.error.error_code}] "
      f"{d.error.message}")
print(f"                  recovery: {d.error.recovery['strategy']}")

# CI "tested" the target but actually built a stale checkout: fresh, signed,
# and still not admissible
runtime.call_tool(session, "run_tests", mcp_run_tests,
                  permission="run:tests", commit_sha=COMMIT,
                  built_sha="commit_old123")
d = runtime.gate_claim(session, {"claim": "tests_passed",
                                 "target": {"commit_sha": COMMIT},
                                 "confidence": 0.97})
print(f"wrong binding   -> {d.decision}  [{d.error.error_code}] "
      f"target={d.error.context.get('expected')!r} "
      f"evidence={d.error.context.get('actual')!r}")

# re-run fresh, then admit
runtime.call_tool(session, "run_tests", mcp_run_tests,
                  permission="run:tests", commit_sha=COMMIT)
d = runtime.gate_claim(session, {"claim": "tests_passed",
                                 "target": {"commit_sha": COMMIT},
                                 "confidence": 0.97})
print(f"re-run evidence -> {d.decision}  (lifecycle advances to 'tests passed')")

# Step 5 — Cost governance in action
beat("STEP 5 — Cost Governor (metering + adaptive routing + tool perf)")
routed = runtime.llm_call(session, stakes="low", input_tokens=30_000, output_tokens=1_500)
print(f"PR-description call routed to cheap model: {routed['model']}  "
      f"(${routed['cost_usd']})")
print(f"usage           : {session.meter.usage()}  "
      f"({session.meter.fraction_used():.1%} of budget)")
print(f"run_tests perf  : {runtime.perf.profile('run_tests')}")

# Step 6 — Crash and recovery
beat("STEP 6 — Crash and recovery (resume from last checkpoint)")
print("  *** agent process crashes mid-PR-creation ***")
runtime2 = VerifiableRuntime(store=DB, anchor=anchor, proofs="proofs.json")
runtime2.gate.register("ci_pipeline", ci_fetcher)
session = runtime2.resume(session.session_id)
print(f"resumed at step {session.step} — meter restored: {session.meter.usage()}")
print(f"no re-execution: {len(session.tool_results)} completed tool results intact")

# Step 7 — Attestation and audit
beat("STEP 7 — Attestation & provenance (tamper-evident history)")
report = runtime2.verify_session(session.session_id)
print(f"chain verified  : {report}")
bundle = runtime2.export_session(session.session_id)
with open(BUNDLE, "w") as f:
    import json
    json.dump(bundle, f, indent=2)
print(f"bundle exported : {BUNDLE} ({len(bundle['chain'])} events), "
      f"offline verify: {runtime2.verify_bundle(bundle)['events']['chain_valid']}")
alice_actions = runtime2.audit(session.session_id, principal="alice@company.com")
print(f"audit query     : {len(alice_actions)} events acted on behalf of alice@…")

# Step 8 — Human-in-the-loop
beat("STEP 8 — Human-in-the-loop (deploy requires a senior engineer)")
d = runtime2.gate_claim(session, {"claim": "deploy_to_production",
                                  "target": {"deployment_id": "deploy_77"},
                                  "confidence": 0.95})
print(f"no approval     -> {d.decision}  [{d.error.error_code}]")
runtime2.record_approval(session, approver="bob@company.com", role="senior_engineer",
                         claim="deploy_to_production", target={"deployment_id": "deploy_77"})
d = runtime2.gate_claim(session, {"claim": "deploy_to_production",
                                  "target": {"deployment_id": "deploy_77"},
                                  "confidence": 0.95})
print(f"after approval  -> {d.decision}  (envelope approval_chain now: "
      f"{[a['role'] for a in session.envelope.approval_chain]})")

# Bonus — budget hard stop
beat("BONUS — Budget hard stop (Proof-or-Stop applies to money too)")
tiny = runtime.start_session(principal_id="alice@company.com",
                             agent_id="agent-coder-01", permissions=["read:repo"],
                             budget=Budget(max_usd=0.01))
try:
    runtime.llm_call(tiny, stakes="high", input_tokens=40_000, output_tokens=4_000)
except Exception as e:
    print(f"session stopped : {getattr(e, 'error_code', e)} — {e}")

runtime.store.close()
runtime2.store.close()
if not os.environ.get("VAR_DEMO_KEEP"):
    os.remove(DB)
print(f"\nDone. ({BUNDLE} + demo.key left on disk — inspect with: "
      f"python3 cli.py verify-bundle {BUNDLE} --key demo.key)")
