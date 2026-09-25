"""Assert-based checks for every feature. Run: python3 test_runtime.py"""

from __future__ import annotations

import json
import sqlite3
import time

from var_runtime import (Budget, GateEngine, IdentityEnvelope, Meter, ModelRouter,
                         ProofRegistry, TrustAnchor, VerifiableRuntime)
from var_runtime.attestation import TamperError, EventChain, export_bundle, verify_bundle
from var_runtime.cost import BudgetExceeded, percentile
from var_runtime.errors import Category, classify
from var_runtime.identity import IdentityError, META_KEY, inject_meta, issue, verify
from var_runtime.evidence import make_signed_artifact


def test_identity() -> None:
    anchor = TrustAnchor.generate()
    env = IdentityEnvelope("alice", "agent-1", "s1", ["read:repo", "write:pr"],
                           issued_at=1000, expiry=2000)
    tok = issue(env, anchor)
    got = verify(tok, anchor, now=1500)
    assert got.principal_id == "alice" and got.has_permission("read:repo")
    assert not got.has_permission("run:tests")
    try:
        got.require("run:tests"); assert False, "permission should fail"
    except IdentityError:
        pass
    # tamper: alter the payload segment (signature no longer covers it)
    h, _, s = tok.split(".")
    bad = f"{h}." + tok.split(".")[1][:-2] + "AA." + s
    try:
        verify(bad, anchor, now=1500); assert False, "tampered envelope verified"
    except IdentityError:
        pass
    assert verify(tok, anchor, now=1500, require_permission="write:pr")
    try:
        verify(tok, anchor, now=2500); assert False, "expired envelope verified"
    except IdentityError as e:
        assert "expired" in str(e)
    try:
        verify(tok, TrustAnchor.generate(), now=1500); assert False
    except IdentityError:
        pass
    assert META_KEY in inject_meta(tok)


def _pad(s: str) -> str:
    return s + "=" * (-len(s) % 4)


def test_serf() -> None:
    e = classify({"status": 503, "error": "upstream down"})
    assert e.category is Category.DEPENDENCY and e.should_retry
    assert classify("HTTP 429 too many requests").category is Category.RATE_LIMIT
    assert classify(RuntimeError("permission denied for user")).category is Category.AUTHENTICATION
    assert classify("invalid input: schema mismatch").category is Category.VALIDATION
    assert classify("NoSuchToolError: not found").category is Category.PERMANENT
    assert not classify("not found").should_retry
    e2 = classify("gateway timeout", tool_name="github_api")
    assert e2.to_dict()["tool_name"] == "github_api"
    assert e2.next_backoff(0) in (1, 5, 15, 30, 60, 120, 300, 600)
    d = e2.to_dict()
    assert d["category"] == "TRANSIENT" and "recovery" in d


def test_attestation() -> None:
    anchor = TrustAnchor.generate()
    chain = EventChain(anchor=anchor)
    for i in range(5):
        chain.append({"type": "step", "i": i})
    assert chain.verify()["chain_valid"] and chain.verify()["length"] == 5

    rebuilt = EventChain.from_dict(chain.to_dict(), anchor)
    assert rebuilt.verify()["head_hash"] == chain.verify()["head_hash"]

    # tamper: edit an event payload in the middle
    tampered = EventChain.from_dict(chain.to_dict(), anchor)
    tampered.entries[2].event["i"] = 999
    try:
        tampered.verify(); assert False, "tampered chain verified"
    except TamperError as t:
        assert "modified" in str(t)

    # tamper: delete an entry -> hash mismatch downstream
    deleted = EventChain.from_dict(chain.to_dict(), anchor)
    del deleted.entries[3]
    try:
        deleted.verify(); assert False, "shortened chain verified"
    except TamperError as t:
        assert "mismatch" in str(t) or "prev_hash" in str(t)

    # offline bundle verification
    bundle = export_bundle("s_x", chain)
    report = verify_bundle(bundle, anchor)
    assert report["events"]["chain_valid"]
    bundle["chain"][1]["event"]["i"] = 42
    assert not verify_bundle(bundle, anchor)["events"]["chain_valid"]


def test_state_store() -> None:
    rt = VerifiableRuntime()
    rt.store.save_checkpoint("s", 1, {"messages": ["a"]})
    rt.store.save_checkpoint("s", 2, {"messages": ["a", "b"]})
    assert rt.store.latest_checkpoint("s")[0] == 2
    assert len(rt.store.checkpoints("s")) == 2
    assert rt.store.sessions() == ["s"]
    rt.store.close()


def test_cost() -> None:
    m = Meter(budget=Budget(max_usd=1.0))
    m.meter_llm("flagship", 100_000, 0)   # $0.30
    assert abs(m.usage()["usd"] - 0.30) < 1e-9
    assert m.check()["status"] == "ok"
    m.meter_llm("flagship", 300_000, 0)   # total $1.20 > $1.00
    try:
        m.check(); assert False, "budget not enforced"
    except BudgetExceeded as e:
        assert "usd" in str(e)

    m2 = Meter(budget=Budget(max_usd=1.0, on_breach="degrade"))
    m2.meter_llm("flagship", 300_000, 0)
    assert m2.check()["status"] == "degrade"

    r = ModelRouter()
    assert r.route("high") == "flagship" and r.route("low") == "fast"
    assert r.route("high", budget_used_fraction=0.9) == "standard"
    assert percentile([1, 2, 3, 4, 100], 99) == 100
    assert percentile([5], 50) == 5 and percentile([], 99) == 0.0


REQS = {"claims": {"tests_passed": {"evidence_type": "ci_test_result",
                                    "source": "ci", "max_age_seconds": 300,
                                    "must_bind_to": ["commit_sha"],
                                    "recovery": "re_run_tests"}}}


def _mk_artifact(anchor, *, sha="c1", age=0.0, passed=True, payload=None):
    return make_signed_artifact("ci_test_result", "ci",
                                payload or {"passed": passed, "tests": 10},
                                bindings={"commit_sha": sha}, anchor=anchor,
                                produced_at=time.time() - age)


def test_evidence_gate() -> None:
    anchor = TrustAnchor.generate()
    other = TrustAnchor.generate("other-key")
    artifacts: dict[str, dict] = {}
    gate = GateEngine(ProofRegistry(REQS["claims"]), {"ci": lambda r, c: artifacts.get(
        c["target"]["commit_sha"])}, anchor=anchor)

    claim = {"claim": "tests_passed", "target": {"commit_sha": "c1"}, "confidence": 0.9}
    artifacts["c1"] = _mk_artifact(anchor)
    assert gate.evaluate(claim).admitted  # happy path

    cases = []
    artifacts["c1"] = _mk_artifact(anchor, age=400)
    cases.append(("EVIDENCE_STALE", gate.evaluate(claim)))
    artifacts["c1"] = _mk_artifact(anchor, sha="wrong_sha")
    cases.append(("EVIDENCE_UNBOUND", gate.evaluate(claim)))
    cases.append(("EVIDENCE_MISSING", gate.evaluate(
        {"claim": "tests_passed", "target": {"commit_sha": "nope"}})))
    a = _mk_artifact(anchor, sha="c1"); a["payload"]["tests"] = 999  # hash break
    artifacts["c1"] = a
    cases.append(("EVIDENCE_HASH_MISMATCH", gate.evaluate(claim)))
    artifacts["c1"] = _mk_artifact(other, sha="c1")  # signed by untrusted key
    cases.append(("EVIDENCE_SIGNATURE_INVALID", gate.evaluate(claim)))
    artifacts["c1"] = _mk_artifact(anchor, sha="c1", passed=False)
    cases.append(("EVIDENCE_NEGATIVE", gate.evaluate(claim)))
    for want_code, d in cases:
        assert not d.admitted, want_code
        assert d.error.error_code == want_code, (want_code, d.error.error_code)
        assert d.error.recovery["strategy"], want_code

    try:
        gate.evaluate({"claim": "unregistered", "target": {}})
        assert False
    except Exception as e:
        assert getattr(e, "error_code", "") == "CLAIM_UNKNOWN"


def _tool_ok(meta, x=1):
    return {"x": x, "saw_envelope": META_KEY in meta}


def test_runtime_end_to_end() -> None:
    rt = VerifiableRuntime(store=":memory:", anchor=TrustAnchor.generate(),
                           proofs="proofs.json", retry_backoff_scale=0.0)
    ci: dict[str, dict] = {}
    ci_anchor = TrustAnchor.generate("ci-key-1")
    rt.anchor.keys["ci-key-1"] = ci_anchor.keys["ci-key-1"]
    rt.gate.register("ci_pipeline", lambda r, c: ci.get(c["target"]["commit_sha"]))

    s = rt.start_session(principal_id="alice", agent_id="ag",
                         permissions=["read:repo", "run:tests"],
                         budget=Budget(max_usd=10.0))
    # identity propagation + metering + checkpoint
    res = rt.call_tool(s, "read_file", _tool_ok, permission="read:repo")
    assert res["saw_envelope"]
    # permission denial
    try:
        rt.call_tool(s, "write_file", _tool_ok, permission="write:repo")
        assert False, "missing permission allowed"
    except IdentityError:
        pass
    # SERF retry then success
    fails = {"n": 0}
    def flaky(meta):
        fails["n"] += 1
        if fails["n"] < 3:
            raise RuntimeError("HTTP 503 unavailable")
        return "ok"
    assert rt.call_tool(s, "api", flaky) == "ok" and fails["n"] == 3
    assert s.meter.retries == 2

    # evidence flow
    ci["c1"] = _mk_artifact(ci_anchor, sha="c1")
    d = rt.gate_claim(s, {"claim": "tests_passed", "target": {"commit_sha": "c1"}})
    assert d.admitted
    d = rt.gate_claim(s, {"claim": "deploy_to_production",
                          "target": {"deployment_id": "d1"}, "confidence": 0.99})
    assert not d.admitted and d.error.error_code == "EVIDENCE_MISSING"
    rt.record_approval(s, approver="bob", role="senior_engineer",
                       claim="deploy_to_production", target={"deployment_id": "d1"})
    d = rt.gate_claim(s, {"claim": "deploy_to_production",
                          "target": {"deployment_id": "d1"}, "confidence": 0.99})
    assert d.admitted and s.envelope.approval_chain[0]["approver"] == "bob"

    # durable resume: state + meter + approvals survive a "crash"
    rt.llm_call(s, stakes="high", input_tokens=50_000, output_tokens=5_000)
    sid, step, tokens = s.session_id, s.step, s.meter.tokens
    rt2 = VerifiableRuntime(store=":memory:", anchor=rt.anchor, proofs="proofs.json")
    rt2.store.db.close()
    rt2.store = rt.store  # same backing sqlite in-memory db
    rt2.gate.register("ci_pipeline", lambda r, c: ci.get(c["target"]["commit_sha"]))
    s2 = rt2.resume(sid)
    assert s2.step == step and s2.meter.tokens == tokens
    assert s2.tool_results and s2.pending_actions == []
    assert rt2.verify_session(sid)["chain_valid"]
    # approval durability: gate admits on the resumed runtime (in-memory log gone)
    d = rt2.gate_claim(s2, {"claim": "deploy_to_production",
                            "target": {"deployment_id": "d1"}, "confidence": 0.99})
    assert d.admitted

    # audit + export
    assert len(rt2.audit(sid, principal="alice")) >= 1
    assert not any(e for e in rt2.audit(sid, event_type="session_started")
                   if e["type"] != "session_started")
    assert rt2.verify_bundle(rt2.export_session(sid))["events"]["chain_valid"]

    # tamper with persisted history -> verification fails
    rt2.store.db.execute("UPDATE events SET entry_json = replace(entry_json, "
                         "'alice', 'mallory') WHERE session_id=?", (sid,))
    rt2.store.db.commit()
    report = rt2.verify_session(sid)
    assert not report["chain_valid"], report


def main() -> None:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} checks passed")


if __name__ == "__main__":
    main()
