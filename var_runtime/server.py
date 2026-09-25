"""VAR hosted API — launch-ready REST server (stdlib only).

Auth: API keys (`var_live_<id>_<secret>`, sha256-hashed at rest, constant-time
compare). Every request is recorded (api_records). Rate limits per key.
Sessions can be created/resumed over the API; gate claims run server-side
fetchers (approval_log, http_json). Serves the landing page and dashboard
statically. Billing webhooks live in billing.py.

Run: python3 -m var_runtime.server [--db var.db] [--port 8788]
Production: single-threaded by design (sqlite + zero deps). Put Caddy/nginx in
front for TLS, run N processes on N ports to scale. ponytail: serialize-first,
eventloop/uvicorn port when traffic demands it.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import secrets
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

from . import __version__
from .cost import Budget
from .errors import Category, StructuredError
from .evidence import ProofRegistry
from .identity import TrustAnchor, IdentityError
from .runtime import VerifiableRuntime

RATE_LIMITS = {"free": 60, "pro": 600, "team": 6000}  # req/min per key
PLAN_QUOTA = {"free": 1_000, "pro": 100_000, "team": 1_000_000}  # gate decisions/mo

_EXTRA_SCHEMA = """
CREATE TABLE IF NOT EXISTS api_keys (
    key_id TEXT PRIMARY KEY, key_hash TEXT NOT NULL, tenant TEXT NOT NULL,
    plan TEXT NOT NULL DEFAULT 'free', role TEXT NOT NULL DEFAULT 'member',
    email TEXT, created_at REAL NOT NULL, revoked INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS waitlist (
    email TEXT PRIMARY KEY, token TEXT NOT NULL, confirmed INTEGER NOT NULL DEFAULT 0,
    created_at REAL NOT NULL, confirmed_at REAL);
CREATE TABLE IF NOT EXISTS api_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL NOT NULL, key_id TEXT,
    method TEXT NOT NULL, path TEXT NOT NULL, status INTEGER NOT NULL,
    latency_ms REAL NOT NULL, session_id TEXT);
CREATE TABLE IF NOT EXISTS usage_counters (
    key_id TEXT NOT NULL, month TEXT NOT NULL, gate_decisions INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (key_id, month));
CREATE TABLE IF NOT EXISTS customers (
    tenant TEXT PRIMARY KEY, stripe_customer_id TEXT, stripe_subscription_id TEXT,
    plan TEXT NOT NULL DEFAULT 'free', status TEXT, current_period_end REAL);
"""


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message


class Api:
    def __init__(self, store_path: str = "var.db", static_dir: str = "frontend",
                 anchor: TrustAnchor | None = None, proofs: str = "proofs.json",
                 stripe_secret: str | None = None):
        self.static_dir = Path(static_dir)
        self.docs_dir = Path("docs")
        self.rt = VerifiableRuntime(store_path, anchor=anchor, proofs=proofs)
        self.store, self.db = self.rt.store, self.rt.store.db
        self.db.executescript(_EXTRA_SCHEMA)
        self.db.commit()
        self._rate: dict[str, tuple[float, int]] = {}  # key_id -> (window, count)
        self.lock = threading.Lock()  # api-level state; store access is same-thread
        self.stripe_secret = stripe_secret or os.environ.get("STRIPE_SECRET_KEY")

        # server-side evidence fetchers (hosted mode)
        self.rt.gate.register("http_json", self._fetch_http_json)

        # bootstrap: first admin key printed once if none exist
        if not self.db.execute("SELECT 1 FROM api_keys LIMIT 1").fetchone():
            key, kid = self.create_key(tenant="bootstrap", plan="team", role="admin")
            print(f"[var] bootstrap admin key (save it, shown once): {key}")

    # -- keys & tenants ---------------------------------------------------------

    def create_key(self, tenant: str, plan: str = "free", role: str = "member",
                   email: str | None = None) -> tuple[str, str]:
        key_id = secrets.token_hex(8)
        secret = secrets.token_hex(20)
        key = f"var_live_{key_id}_{secret}"
        self.db.execute(
            "INSERT INTO api_keys VALUES (?,?,?,?,?,?,?,0)",
            (key_id, hashlib.sha256(key.encode()).hexdigest(), tenant, plan, role,
             email, time.time()))
        self.db.commit()
        return key, key_id

    def authenticate(self, header: str | None) -> dict[str, Any]:
        if not header or not header.startswith("Bearer var_live_"):
            raise ApiError(401, "UNAUTHORIZED", "missing or malformed API key")
        key = header.removeprefix("Bearer ").strip()
        parts = key.split("_")  # var, live, id, secret
        if len(parts) != 4:
            raise ApiError(401, "UNAUTHORIZED", "malformed API key")
        row = self.db.execute(
            "SELECT key_id, key_hash, tenant, plan, role, revoked FROM api_keys "
            "WHERE key_id=?", (parts[2],)).fetchone()
        if not row or not hmac.compare_digest(row[1],
                hashlib.sha256(key.encode()).hexdigest()):
            raise ApiError(401, "UNAUTHORIZED", "invalid API key")
        if row[5]:
            raise ApiError(403, "FORBIDDEN", "key revoked")
        self._rate_limit(row[0], row[3])
        return {"key_id": row[0], "tenant": row[2], "plan": row[3], "role": row[4]}

    def _rate_limit(self, key_id: str, plan: str) -> None:
        now, limit = time.time(), RATE_LIMITS.get(plan, 60)
        win, count = self._rate.get(key_id, (now, 0))
        if now - win > 60:
            win, count = now, 0
        count += 1
        self._rate[key_id] = (win, count)
        if count > limit:
            raise ApiError(429, "RATE_LIMIT",
                           f"{limit} req/min limit for plan '{plan}'")

    def _tenant_key(self, auth: dict, session_id: str) -> None:
        s = self.rt.sessions.get(session_id) or self._lazy_resume(session_id)
        if s is None:
            raise ApiError(404, "NOT_FOUND", f"unknown session {session_id}")
        if s.envelope.principal_id != auth["tenant"] and auth["role"] != "admin":
            raise ApiError(403, "FORBIDDEN", "session belongs to another tenant")

    def _lazy_resume(self, session_id: str) -> Any:
        try:
            return self.rt.resume(session_id)
        except KeyError:
            return None

    def _count_gate_decision(self, auth: dict) -> None:
        month = time.strftime("%Y-%m")
        self.db.execute(
            "INSERT INTO usage_counters VALUES (?,?,1) ON CONFLICT(key_id, month) "
            "DO UPDATE SET gate_decisions=gate_decisions+1", (auth["key_id"], month))
        row = self.db.execute("SELECT gate_decisions FROM usage_counters "
                              "WHERE key_id=? AND month=?", (auth["key_id"], month)).fetchone()
        if row[0] > PLAN_QUOTA.get(auth["plan"], 1000):
            raise ApiError(402, "QUOTA_EXCEEDED",
                           f"plan '{auth['plan']}' gate-decision quota exceeded — upgrade")
        self.db.commit()

    # -- evidence fetcher (hosted) ------------------------------------------------

    def _fetch_http_json(self, req: dict, claim: dict) -> dict | None:
        """Generic hosted fetcher: requirement carries a URL template.
        {target_field} placeholders are substituted from the claim target."""
        url = req.get("url", "")
        for k, v in claim.get("target", {}).items():
            url = url.replace("{" + k + "}", str(v))
        if not url.startswith("https://"):
            raise ApiError(400, "FETCHER_CONFIG", "http_json requires https url")
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    url, headers={"Accept": "application/json"}), timeout=10) as r:
                payload = json.loads(r.read())
        except Exception as e:
            raise ApiError(502, "EVIDENCE_SOURCE_UNREACHABLE", str(e))
        from .evidence import make_signed_artifact
        return make_signed_artifact(req["evidence_type"], "http_json", payload,
                                    bindings=claim.get("target", {}),
                                    anchor=self.rt.anchor)

    # -- waitlist (double opt-in; compliant list building) -------------------------

    def waitlist_signup(self, email: str) -> dict[str, Any]:
        email = email.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ApiError(400, "VALIDATION", "invalid email")
        token = secrets.token_urlsafe(24)
        self.db.execute(
            "INSERT INTO waitlist(email, token, created_at) VALUES (?,?,?) "
            "ON CONFLICT(email) DO NOTHING", (email, token, time.time()))
        self.db.commit()
        row = self.db.execute("SELECT token, confirmed FROM waitlist WHERE email=?",
                              (email,)).fetchone()
        confirm_url = f"/waitlist/confirm?token={row[0]}"
        self._send_email(email, "Confirm your VAR waitlist spot",
                         f"Confirm: {confirm_url}\n\nIf you didn't sign up, ignore this.")
        return {"status": "pending_confirmation" if not row[1] else "already_confirmed",
                "confirm_url_dev": confirm_url if self._dev_mode else None}

    _dev_mode = True  # ponytail: dev shows confirm URL inline; set False + SMTP in prod

    def waitlist_confirm(self, token: str) -> dict[str, Any]:
        cur = self.db.execute("UPDATE waitlist SET confirmed=1, confirmed_at=? "
                              "WHERE token=?", (time.time(), token))
        self.db.commit()
        if cur.rowcount == 0:
            raise ApiError(404, "NOT_FOUND", "unknown confirmation token")
        return {"status": "confirmed"}

    def _send_email(self, to: str, subject: str, body: str) -> None:
        host = os.environ.get("VAR_SMTP_HOST")
        if not host:
            print(f"[var] email (dev log) to={to} subject={subject!r}")  # prod: SMTP below
            return
        import smtplib
        from email.message import EmailMessage
        base = os.environ.get("VAR_SMTP_BASE", "https://var-runtime.dev")
        body = body.replace("/waitlist/confirm", base + "/waitlist/confirm")
        msg = EmailMessage()
        msg["To"], msg["Subject"] = to, subject
        msg["From"] = os.environ.get("VAR_SMTP_FROM", "waitlist@var-runtime.dev")
        msg.set_content(body)
        with smtplib.SMTP(host, int(os.environ.get("VAR_SMTP_PORT", "587")), timeout=10) as s:
            s.starttls()
            s.login(os.environ["VAR_SMTP_USER"], os.environ["VAR_SMTP_PASS"])
            s.send_message(msg)

    # -- routes ----------------------------------------------------------------

    def dispatch(self, method: str, path: str, query: dict[str, list[str]],
                 body: bytes, auth_header: str | None,
                 stripe_sig: str | None = None) -> tuple[int, Any]:
        started = time.monotonic()
        auth, status, out = None, 500, None
        session_id = path.split("/")[3] if path.startswith("/v1/sessions/") and \
            len(path.split("/")) > 3 else None
        try:
            public = path in ("/", "/healthz", "/privacy", "/terms", "/favicon.svg", "/architecture") or path.startswith(("/app", "/waitlist/confirm", "/v1/waitlist", "/v1/stripe/webhook"))
            auth = None if public else self.authenticate(auth_header)
            status, out = self._route(method, path, query, body, auth, stripe_sig)
        except ApiError as e:
            status, out = e.status, {"error": {"code": e.code, "message": e.message}}
        except StructuredError as e:
            status = 402 if e.error_code == "BUDGET_EXCEEDED" else 400
            out = {"error": {**e.to_dict(), "serf": True}}
        except IdentityError as e:
            status, out = 401, {"error": {"code": "IDENTITY", "message": str(e)}}
        except Exception as e:  # noqa: BLE001 — API boundary: never leak a stack
            status, out = 500, {"error": {"code": "INTERNAL", "message": str(e)}}
        latency = (time.monotonic() - started) * 1000
        self.db.execute("INSERT INTO api_records(ts,key_id,method,path,status,"
                        "latency_ms,session_id) VALUES (?,?,?,?,?,?,?)",
                        (time.time(), auth and auth["key_id"], method, path,
                         status, round(latency, 2), session_id))
        self.db.commit()
        return status, out

    def _route(self, method: str, path: str, q: dict[str, list[str]],
               body: bytes, auth: dict | None,
               stripe_sig: str | None = None) -> tuple[int, Any]:
        B = json.loads(body) if body else {}
        P = path.rstrip("/")

        if P == "/healthz":
            return 200, {"ok": True, "version": __version__}
        if P == "/architecture":
            f = self.docs_dir / "architecture.html"
            if f.is_file():
                return 200, ("__raw__", f.read_bytes(), "text/html; charset=utf-8")
        if P in ("", "/") or P.startswith("/app") or P in ("/privacy", "/terms", "/favicon.svg"):
            return self._static(P)

        if P == "/v1/waitlist" and method == "POST":
            return 202, self.waitlist_signup(B.get("email", ""))
        if P == "/waitlist/confirm":
            return 200, self.waitlist_confirm((q.get("token") or [""])[0])

        if P == "/v1/stripe/webhook" and method == "POST":
            from .billing import handle_webhook
            return handle_webhook(self, body, stripe_sig)

        if P == "/v1/keys" and method == "POST" and auth and auth["role"] == "admin":
            key, kid = self.create_key(B.get("tenant", auth["tenant"]),
                                       B.get("plan", "free"), B.get("role", "member"),
                                       B.get("email"))
            return 201, {"key": key, "key_id": kid}  # shown once
        if P == "/v1/records" and method == "GET" and auth and auth["role"] == "admin":
            rows = self.db.execute(
                "SELECT ts,key_id,method,path,status,latency_ms,session_id "
                "FROM api_records ORDER BY id DESC LIMIT 500").fetchall()
            return 200, {"records": [dict(zip(("ts", "key_id", "method", "path",
                                               "status", "latency_ms", "session_id"), r)) for r in rows]}

        if P == "/v1/proofs" and method == "GET":
            return 200, {"claims": sorted(self.rt.proof_registry.claims)}

        if P == "/v1/sessions" and method == "GET" and auth:
            out = []
            for sid in self.db.execute(
                    "SELECT DISTINCT session_id FROM checkpoints ORDER BY 1").fetchall():
                sid = sid[0]
                events = self.store.load_events(sid)
                started = next((e["event"] for e in events
                                if e["event"].get("type") == "session_started"), {})
                if started.get("principal") != auth["tenant"] and auth["role"] != "admin":
                    continue
                gates = [e["event"] for e in events
                         if e["event"].get("type") == "gate_decision"]
                ck = self.store.latest_checkpoint(sid)
                out.append({"session_id": sid, "agent": started.get("agent"),
                            "principal": started.get("principal"),
                            "started_at": events[0]["event"].get("ts") if events else None,
                            "steps": ck[0] if ck else 0,
                            "events": len(events),
                            "gate_decisions": len(gates),
                            "admits": sum(1 for g in gates if g.get("decision") == "ADMIT"),
                            "halts": sum(1 for g in gates if g.get("decision") == "HALT")})
            return 200, {"sessions": out}

        if P == "/v1/perf" and method == "GET" and auth:
            tools = [r[0] for r in self.db.execute(
                "SELECT DISTINCT tool FROM tool_stats ORDER BY tool")]
            return 200, {"tools": {t: self.rt.perf.profile(t) for t in tools}}

        if P == "/v1/sessions" and method == "POST":
            s = self.rt.start_session(
                principal_id=auth["tenant"], agent_id=B.get("agent_id", "agent"),
                permissions=B.get("permissions", []), budget=Budget(**B["budget"]) if B.get("budget") else None)
            return 201, {"session_id": s.session_id, "identity_envelope": s.token,
                         "expires_at": s.envelope.expiry}

        m = re.match(r"^/v1/sessions/([\w]+)(?:/(\w+))?$", P)
        if m and auth:
            sid, action = m.group(1), m.group(2)
            self._tenant_key(auth, sid)
            s = self.rt.sessions[sid]
            if action is None and method == "GET":
                return 200, {"session_id": sid, "step": s.step, "state": s.state()}
            if action == "gate" and method == "POST":
                self._count_gate_decision(auth)
                d = self.rt.gate_claim(s, B)
                return 200, d.to_dict()
            if action == "approvals" and method == "POST":
                self.rt.record_approval(s, approver=B["approver"], role=B["role"],
                                        claim=B["claim"], target=B.get("target", {}))
                return 202, {"status": "recorded"}
            if action == "meter" and method == "POST" and B.get("kind") == "llm":
                out = self.rt.llm_call(s, stakes=B.get("stakes", "medium"),
                                       input_tokens=B.get("input_tokens", 0),
                                       output_tokens=B.get("output_tokens", 0))
                return 200, {"routing": out, "usage": s.meter.usage()}
            if action == "usage" and method == "GET":
                return 200, {"usage": s.meter.usage(),
                             "fraction_used": round(s.meter.fraction_used(), 4)}
            if action == "verify" and method == "GET":
                return 200, self.rt.verify_session(sid)
            if action == "audit" and method == "GET":
                return 200, {"events": self.rt.audit(
                    sid, principal=(q.get("principal") or [None])[0],
                    event_type=(q.get("type") or [None])[0])}
            if action == "checkpoint" and method == "POST":
                s.memory.update(B.get("memory", {}))
                s.messages.extend(B.get("messages", []))
                self.rt.checkpoint(s)
                return 202, {"status": "checkpointed", "step": s.step}
            if action == "resume" and method == "POST":
                s = self.rt.resume(sid)
                return 200, {"resumed": True, "step": s.step,
                             "tool_results": len(s.tool_results)}

        if P == "/v1/billing/checkout" and method == "POST":
            from .billing import create_checkout
            return create_checkout(self, auth, B)

        raise ApiError(404, "NOT_FOUND", f"no route {method} {path}")

    # -- static ------------------------------------------------------------------

    def _static(self, path: str) -> tuple[int, Any]:
        # "/" -> landing, "/app" -> dashboard, "/privacy" "/terms" "/favicon.svg" -> legal/brand
        if path in ("", "/"):
            rel = "landing.html"
        elif path == "/app":
            rel = "index.html"
        elif path in ("/privacy", "/terms"):
            rel = path.removeprefix("/") + ".html"
        elif path == "/favicon.svg":
            rel = "favicon.svg"
        else:
            rel = path.removeprefix("/app/")
        f = (self.static_dir / rel).resolve()
        if not str(f).startswith(str(self.static_dir.resolve())) or not f.is_file():
            f = self.static_dir / ("index.html" if rel != "index.html" else "landing.html")
            if not f.is_file():
                return 200, {"status": "frontend/ not built yet — API is live"}
        types = {".html": "text/html; charset=utf-8", ".js": "text/javascript",
                 ".css": "text/css", ".svg": "image/svg+xml", ".png": "image/png"}
        return 200, ("__raw__", f.read_bytes(),
                     types.get(f.suffix, "application/octet-stream"))


def serve(host: str = "0.0.0.0", port: int = 8788, db: str = "var.db",
          static_dir: str = "frontend", key_hex: str | None = None) -> None:
    api = Api(store_path=db, static_dir=static_dir,
              anchor=TrustAnchor.from_secret_hex(key_hex) if key_hex
              else (TrustAnchor.from_secret_hex(os.environ["VAR_SIGNING_KEY"])
                    if os.environ.get("VAR_SIGNING_KEY") else None))
    if not (os.environ.get("VAR_SIGNING_KEY") or key_hex):
        print("[var] WARNING: ephemeral signing key — set VAR_SIGNING_KEY in prod")

    class Handler(BaseHTTPRequestHandler):
        def _run(self, method: str) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            import urllib.parse
            u = urllib.parse.urlparse(self.path)
            from http import HTTPStatus
            status, out = api.dispatch(method, u.path, urllib.parse.parse_qs(u.query),
                                       body, self.headers.get("Authorization"),
                                       self.headers.get("Stripe-Signature"))
            if isinstance(out, tuple) and out and out[0] == "__raw__":
                _, data, ctype = out
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", ctype)
            else:
                data = json.dumps(out, default=str).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            if method != "HEAD":
                self.wfile.write(data)

        def do_GET(self): self._run("GET")       # noqa: N802
        def do_POST(self): self._run("POST")     # noqa: N802
        def do_HEAD(self): self._run("HEAD")     # noqa: N802

        def log_message(self, fmt, *args):
            pass  # api_records is the log

    print(f"[var] API on http://{host}:{port}  (dashboard /app, landing /)")
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="var.db")
    ap.add_argument("--port", type=int, default=8788)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--static", default="frontend")
    ap.add_argument("--key-hex", default=None)
    a = ap.parse_args()
    serve(a.host, a.port, a.db, a.static, a.key_hex)
