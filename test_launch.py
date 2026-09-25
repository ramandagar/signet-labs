"""Launch-stack checks: API server, billing, waitlist, MCP server, SDKs,
integrations. Run: python3 test_launch.py  (boots real HTTP + MCP processes)"""

from __future__ import annotations

import hashlib
import hmac
import io
import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.request
from http.server import HTTPServer

sys.path.insert(0, "sdk/python")
from varclient import VarClient, VarApiError  # noqa: E402

import var_runtime.server as srv  # noqa: E402
from var_runtime.billing import verify_webhook_signature  # noqa: E402
from var_runtime import TrustAnchor, VerifiableRuntime  # noqa: E402

DB = "/tmp/test_launch.db"
PORT = 8793
BASE = f"http://127.0.0.1:{PORT}"


def _fresh_api():
    if os.path.exists(DB):
        os.remove(DB)
    return srv.Api(store_path=DB, static_dir="frontend", proofs="proofs.json")


def test_webhook_signatures() -> None:
    secret = "whsec_x"
    payload = json.dumps({"type": "checkout.session.completed"}).encode()
    t = str(int(time.time()))
    sig = f"t={t},v1=" + hmac.new(secret.encode(), f"{t}.".encode() + payload,
                                  hashlib.sha256).hexdigest()
    assert verify_webhook_signature(payload, sig, secret)
    assert not verify_webhook_signature(payload + b"x", sig, secret)
    assert not verify_webhook_signature(payload, "t=1,v1=deadbeef", secret)  # stale
    assert not verify_webhook_signature(payload, "garbage", secret)


def test_api_end_to_end() -> None:
    api = _fresh_api()

    def call(method, path, body=None, key=None, sig=None, query=None):
        st, out = api.dispatch(method, path, query or {},
                               json.dumps(body).encode() if body else b"",
                               f"Bearer {key}" if key else None, sig)
        return st, out

    key, kid = api.create_key(tenant="acme", plan="team", role="admin")
    st, out = call("GET", "/healthz")
    assert st == 200 and out["ok"]

    # session + gate + approval lifecycle
    st, s = call("POST", "/v1/sessions", {"permissions": ["run:tests"],
                                          "budget": {"max_usd": 5.0}}, key)
    sid = s["session_id"]
    assert st == 201 and s["identity_envelope"].count(".") == 2
    st, d = call("POST", f"/v1/sessions/{sid}/gate",
                 {"claim": "code_reviewed", "target": {"pr_number": 7}}, key)
    assert d["decision"] == "HALT" and d["error"]["error_code"] == "EVIDENCE_MISSING"
    call("POST", f"/v1/sessions/{sid}/approvals",
         {"approver": "rev", "role": "reviewer", "claim": "code_reviewed",
          "target": {"pr_number": 7}}, key)
    st, d = call("POST", f"/v1/sessions/{sid}/gate",
                 {"claim": "code_reviewed", "target": {"pr_number": 7}}, key)
    assert d["decision"] == "ADMIT" and d["checks"]["signed"]

    # metering + verification + audit + resume
    st, m = call("POST", f"/v1/sessions/{sid}/meter",
                 {"kind": "llm", "stakes": "high", "input_tokens": 10, "output_tokens": 1}, key)
    assert m["routing"]["model"] == "flagship"
    assert call("GET", f"/v1/sessions/{sid}/verify", None, key)[1]["chain_valid"]
    assert len(call("GET", f"/v1/sessions/{sid}/audit", None, key)[1]["events"]) >= 5
    st, r = call("POST", f"/v1/sessions/{sid}/resume", None, key)
    assert r["resumed"]  # hosted sessions advance step client-side; resume must not lose state

    # auth: bad key, cross-tenant
    assert call("GET", f"/v1/sessions/{sid}/verify", None, "var_live_bad_key")[0] == 401
    other, _ = api.create_key(tenant="evil")
    assert call("GET", f"/v1/sessions/{sid}/verify", None, other)[0] == 403

    # listing + perf + proofs
    lst = call("GET", "/v1/sessions", None, key)[1]["sessions"]
    assert lst and lst[0]["admits"] >= 1 and lst[0]["halts"] >= 1
    assert "claims" in call("GET", "/v1/proofs", None, key)[1]

    # waitlist double opt-in
    st, w = call("POST", "/v1/waitlist", {"email": "a@b.co"})
    assert st == 202 and w["status"] == "pending_confirmation"
    assert call("GET", "/waitlist/confirm", query={"token": ["zz"]})[0] == 404
    st, c = call("GET", "/waitlist/confirm",
                 query={"token": [w["confirm_url_dev"].split("token=")[1]]})
    assert c["status"] == "confirmed"

    # billing: webhook upgrades the tenant's keys
    os.environ["STRIPE_WEBHOOK_SECRET"] = "whsec_t"
    pl = json.dumps({"type": "checkout.session.completed", "data": {"object": {
        "client_reference_id": "acme", "metadata": {"plan": "pro"},
        "customer": "cus_9", "subscription": "sub_9"}}}).encode()
    t = str(int(time.time()))
    sig = f"t={t},v1=" + hmac.new(b"whsec_t", f"{t}.".encode() + pl,
                                  hashlib.sha256).hexdigest()
    st, out = call("POST", "/v1/stripe/webhook", json.loads(pl), sig=sig)
    assert st == 200 and out["plan"] == "pro"
    assert api.db.execute("SELECT plan FROM api_keys WHERE key_id=?",
                          (kid,)).fetchone()[0] == "pro"
    assert call("POST", "/v1/stripe/webhook", json.loads(pl),
                sig="t=1,v1=bad")[0] == 400

    # quota: free plan key exhausts its monthly gate decisions (counter tested
    # directly — over HTTP the 60/min rate limit fires first, by design)
    fk, _ = api.create_key(tenant="quota", plan="free")
    auth = {"key_id": fk, "tenant": "quota", "plan": "free", "role": "member"}
    quota_hit = False
    for _ in range(1001):
        try:
            api._count_gate_decision(auth)
        except srv.ApiError as e:
            assert e.code == "QUOTA_EXCEEDED" and e.status == 402
            quota_hit = True
            break
    assert quota_hit

    # api records captured everything
    recs = call("GET", "/v1/records", None, key)[1]["records"]
    assert len(recs) >= 15 and all("latency_ms" in r for r in recs[:5])


def test_http_server_and_sdk() -> None:
    _fresh_api()
    os.environ["VAR_SIGNING_KEY"] = "cd" * 32
    import importlib
    proc_srv = srv.serve  # noqa: F841 — reference
    from var_runtime.server import Api
    api = Api(store_path=DB, static_dir="frontend", proofs="proofs.json")
    key, _ = api.create_key(tenant="sdk", plan="pro")

    handler = srv.serve.__globals__  # build handler exactly like serve()
    from http.server import BaseHTTPRequestHandler

    class Handler(BaseHTTPRequestHandler):
        def _run(self, method):
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            import urllib.parse
            u = urllib.parse.urlparse(self.path)
            from http import HTTPStatus
            status, out = api.dispatch(method, u.path, urllib.parse.parse_qs(u.query),
                                       body, self.headers.get("Authorization"),
                                       self.headers.get("Stripe-Signature"))
            data = json.dumps(out, default=str).encode()
            self.send_response(status if not isinstance(out, tuple) else HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            if method != "HEAD":
                self.wfile.write(data)
        def do_GET(self): self._run("GET")
        def do_POST(self): self._run("POST")
        def log_message(self, *a): pass

    httpd = HTTPServer(("127.0.0.1", PORT), Handler)

    def client_flow():  # runs in a thread; server stays on the main thread
        c = VarClient(BASE, key)
        s = c.create_session(["run:tests"], max_usd=1.0)
        d = c.gate_claim(s["session_id"], "code_reviewed", {"pr_number": 3})
        assert not d.admitted and d.error["error_code"] == "EVIDENCE_MISSING"
        c.record_approval(s["session_id"], "r", "reviewer", "code_reviewed", {"pr_number": 3})
        d = c.gate_claim(s["session_id"], "code_reviewed", {"pr_number": 3})
        assert d.admitted and d.decision == "ADMIT"
        assert c.verify(s["session_id"])["chain_valid"]
        assert c.usage(s["session_id"])["usage"]["tokens"] == 0
        assert len(c.sessions()) >= 1 and len(c.proofs()) == 5
        try:
            c.billing_checkout("pro")
        except VarApiError as e:
            assert e.status == 503 and e.body["error"]["code"] == "BILLING_UNCONFIGURED"
        httpd.shutdown()

    t = threading.Thread(target=client_flow)
    t.start()
    httpd.serve_forever()        # serve on THIS thread — sqlite is thread-bound
    t.join()


def test_mcp_stdio() -> None:
    db = "/tmp/test_mcp.db"
    if os.path.exists(db):
        os.remove(db)
    p = subprocess.Popen([sys.executable, "-m", "var_runtime.mcp_server", "--db", db],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    def send(obj):
        p.stdin.write(json.dumps(obj) + "\n"); p.stdin.flush()
        return json.loads(p.stdout.readline())

    def tool(i, name, args):
        r = send({"jsonrpc": "2.0", "id": i, "method": "tools/call",
                  "params": {"name": name, "arguments": args}})["result"]
        assert not r["isError"]
        return json.loads(r["content"][0]["text"])

    init = send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    assert init["result"]["serverInfo"]["name"] == "var-runtime"
    assert len(send({"jsonrpc": "2.0", "id": 2, "method": "tools/list",
                     "params": {}})["result"]["tools"]) == 7
    s = tool(3, "var_start_session", {"principal_id": "mcp@co",
                                      "permissions": ["run:tests"], "max_usd": 1})
    sid = s["session_id"]
    assert tool(4, "var_gate_claim", {"session_id": sid, "claim": "tests_passed",
                                      "target": {"commit_sha": "c9"}})["decision"] == "HALT"
    tool(5, "var_submit_evidence", {"evidence_type": "ci_test_result",
                                    "payload": {"passed": True}, "bindings": {"commit_sha": "c9"}})
    assert tool(6, "var_gate_claim", {"session_id": sid, "claim": "tests_passed",
                                      "target": {"commit_sha": "c9"}})["decision"] == "ADMIT"
    assert tool(7, "var_verify_session", {"session_id": sid})["chain_valid"]
    assert "gate_decision" in {e["type"] for e in
                               tool(8, "var_audit_session", {"session_id": sid})["events"]}
    err = send({"jsonrpc": "2.0", "id": 9, "method": "bogus/method", "params": {}})
    assert err["error"]["code"] == -32603
    p.terminate()


def test_integrations() -> None:
    import urllib.request as ur
    from var_runtime.integrations import github_actions_fetcher, gated_node

    class Fake(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *a): return False

    anchor = TrustAnchor.generate()
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    orig = ur.urlopen
    ur.urlopen = lambda req, timeout=None: Fake(json.dumps({"check_runs": [
        {"name": "pytest", "status": "completed", "conclusion": "success",
         "completed_at": now}]}).encode())
    rt = VerifiableRuntime(":memory:", anchor=anchor, proofs="proofs.json")
    rt.gate.register("ci_pipeline", github_actions_fetcher("acme/app", anchor=anchor))
    s = rt.start_session(principal_id="ci", agent_id="ag", permissions=["run:tests"])
    d = rt.gate_claim(s, {"claim": "tests_passed", "target": {"commit_sha": "c1"}})
    assert d.admitted and d.checks["bound:commit_sha"]
    ur.urlopen = lambda req, timeout=None: Fake(json.dumps({"check_runs": [
        {"name": "pytest", "status": "completed", "conclusion": "failure",
         "completed_at": now}]}).encode())
    d = rt.gate_claim(s, {"claim": "tests_passed", "target": {"commit_sha": "c1"}})
    assert not d.admitted and d.error.error_code == "EVIDENCE_NEGATIVE"
    ur.urlopen = orig

    wrapped, GateHalted = gated_node(rt, s, "code_reviewed",
                                     lambda st: {"pr_number": st["pr"]})
    try:
        wrapped({"pr": 1}); assert False
    except GateHalted as e:
        assert e.error_code == "GATE_EVIDENCE_MISSING"


def main() -> None:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} launch checks passed")


if __name__ == "__main__":
    main()
