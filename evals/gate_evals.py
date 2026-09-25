"""Gate evaluation suite — scenario-based evals for the Evidence Gate.

Shape borrowed from the pytest-native LLM eval frameworks (DeepEval/promptfoo
pattern: declarative cases, one metric each, exit-code CI gate) but with zero
dependencies and deterministic assertions — the gate is pure machinery, so
every case has exactly one correct verdict.

Each case: name, setup (evidence state), claim, expect (decision + code).
Run: python3 evals/gate_evals.py    (exit 1 on any failure — CI-able)
"""

from __future__ import annotations

import json
import sqlite3
import sys
import time

sys.path.insert(0, ".")
from var_runtime import Budget, TrustAnchor, VerifiableRuntime  # noqa: E402
from var_runtime.evidence import make_signed_artifact  # noqa: E402

REQS = {"claims": {
    "tests_passed": {"evidence_type": "ci_test_result", "source": "ci",
                     "max_age_seconds": 300, "must_bind_to": ["commit_sha"],
                     "recovery": "re_run_tests"},
    "deploy_to_production": {"evidence_type": "human_approval",
                             "source": "approval_log", "approver_role": "senior_engineer",
                             "max_age_seconds": 3600, "must_bind_to": ["deployment_id"],
                             "min_confidence": 0.9},
}}


def art(anchor, *, sha="c1", age=0.0, passed=True, payload=None):
    return make_signed_artifact("ci_test_result", "ci", payload or {"passed": passed},
                                {"commit_sha": sha}, anchor, time.time() - age)


def runtime_with() -> VerifiableRuntime:
    anchor = TrustAnchor.generate()
    ci_anchor = TrustAnchor.generate("ci-key")
    anchor.keys["ci-key"] = ci_anchor.keys["ci-key"]
    rt = VerifiableRuntime(":memory:", anchor=anchor, proofs=REQS)
    rt.ci, rt.ci_anchor = {}, ci_anchor   # the fetcher closes over rt.ci
    rt.gate.register("ci", lambda r, c: rt.ci.get(c["target"].get("commit_sha")))
    return rt


CASES = []


def case(name, setup, claim, expect_decision, expect_code=None):
    CASES.append(dict(name=name, setup=setup, claim=claim,
                      decision=expect_decision, code=expect_code))


# --- ADMIT paths ---------------------------------------------------------------
case("fresh signed evidence admits",
     lambda rt: rt.ci.__setitem__("c1", art(rt.ci_anchor, sha="c1")),
     {"claim": "tests_passed", "target": {"commit_sha": "c1"}, "confidence": 0.9},
     "ADMIT")
case("evidence exactly at freshness boundary still admits",
     lambda rt: rt.ci.__setitem__("c1", art(rt.ci_anchor, sha="c1", age=299)),
     {"claim": "tests_passed", "target": {"commit_sha": "c1"}, "confidence": 0.9},
     "ADMIT")

# --- HALT paths: every rejection code ------------------------------------------
case("no evidence at all",
     lambda rt: None,
     {"claim": "tests_passed", "target": {"commit_sha": "nope"}, "confidence": 0.9},
     "HALT", "EVIDENCE_MISSING")
case("stale evidence (847s > 300s)",
     lambda rt: rt.ci.__setitem__("c1", art(rt.ci_anchor, sha="c1", age=847)),
     {"claim": "tests_passed", "target": {"commit_sha": "c1"}, "confidence": 0.9},
     "HALT", "EVIDENCE_STALE")
case("evidence bound to a different commit (stale checkout)",
     lambda rt: rt.ci.__setitem__("c1", art(rt.ci_anchor, sha="old_sha")),
     {"claim": "tests_passed", "target": {"commit_sha": "c1"}, "confidence": 0.9},
     "HALT", "EVIDENCE_UNBOUND")
case("payload tampered after signing",
     lambda rt: rt.ci.__setitem__("c1", {**art(rt.ci_anchor, sha="c1"),
                                          "payload": {"passed": True, "tests": 999}}),
     {"claim": "tests_passed", "target": {"commit_sha": "c1"}, "confidence": 0.9},
     "HALT", "EVIDENCE_HASH_MISMATCH")
case("signature from an untrusted key",
     lambda rt: rt.ci.__setitem__("c1", art(TrustAnchor.generate("rogue"), sha="c1")),
     {"claim": "tests_passed", "target": {"commit_sha": "c1"}, "confidence": 0.9},
     "HALT", "EVIDENCE_SIGNATURE_INVALID")
case("fresh signed evidence of FAILURE",
     lambda rt: rt.ci.__setitem__("c1", art(rt.ci_anchor, sha="c1", passed=False)),
     {"claim": "tests_passed", "target": {"commit_sha": "c1"}, "confidence": 0.9},
     "HALT", "EVIDENCE_NEGATIVE")

# --- confidence + HITL -----------------------------------------------------------
case("confidence below floor",
     lambda rt: None,
     {"claim": "deploy_to_production", "target": {"deployment_id": "d1"},
      "confidence": 0.7},
     "HALT", "CONFIDENCE_TOO_LOW")
case("senior approval admits deploy",
     lambda rt: None,  # approval recorded in run()
     {"claim": "deploy_to_production", "target": {"deployment_id": "d1"},
      "confidence": 0.95}, "ADMIT")
case("wrong approver role does not admit",
     lambda rt: None,  # junior approval recorded in run()
     {"claim": "deploy_to_production", "target": {"deployment_id": "d1"},
      "confidence": 0.95}, "HALT", "EVIDENCE_MISSING")

# --- unregistered claim -----------------------------------------------------------
case("claim missing from registry raises SERF validation",
     lambda rt: None,
     {"claim": "alien_claim", "target": {}, "confidence": 1.0},
     "RAISE", "CLAIM_UNKNOWN")


def run() -> int:
    failures = 0
    for c in CASES:
        rt = runtime_with()
        s = rt.start_session(principal_id="eval", agent_id="eval",
                             permissions=["run:tests"])
        if "deploy" in c["name"] and "senior" in c["name"]:
            rt.record_approval(s, approver="senior@co", role="senior_engineer",
                               claim="deploy_to_production", target={"deployment_id": "d1"})
        if "wrong approver" in c["name"]:
            rt.record_approval(s, approver="junior@co", role="junior_dev",
                               claim="deploy_to_production", target={"deployment_id": "d1"})
        c["setup"](rt)
        try:
            d = rt.gate_claim(s, c["claim"])
            ok = d.decision == c["decision"] and (c["code"] is None or
                 (d.error and d.error.error_code == c["code"]))
        except Exception as e:  # CLAIM_UNKNOWN surfaces as a SERF raise
            ok = c["decision"] == "RAISE" and getattr(e, "error_code", "") == c["code"]
            d = e
        print(f"  {'ok  ' if ok else 'FAIL'} {c['name']:55s} -> "
              f"{getattr(d, 'decision', getattr(d, 'error_code', 'RAISE'))}")
        failures += 0 if ok else 1

    # regression: a tampered store must fail verification (the tamper classes)
    rt = runtime_with()
    rt.ci["c1"] = art(rt.ci_anchor, sha="c1")
    s = rt.start_session(principal_id="eval", agent_id="eval", permissions=[])
    rt.gate_claim(s, {"claim": "tests_passed", "target": {"commit_sha": "c1"}})
    rt.store.db.execute("UPDATE events SET entry_json=replace(entry_json,'eval','hacker')")
    rt.store.db.commit()
    ok = not rt.verify_session(s.session_id)["chain_valid"]
    print(f"  {'ok  ' if ok else 'FAIL'} {'tampered history fails verification':55s} -> "
          f"{rt.verify_session(s.session_id)['chain_valid']}")
    failures += 0 if ok else 1

    print(f"\n{len(CASES) + 1 - failures}/{len(CASES) + 1} gate evals passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
