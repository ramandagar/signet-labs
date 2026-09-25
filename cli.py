"""var — CLI for the Verifiable Agent Runtime.

Commands:
  var sessions [--db PATH]                      list recorded sessions
  var verify SESSION_ID [--db PATH] [--key HEX] verify a session's hash chain
  var audit SESSION_ID [--principal P] [--type T] [--db]  query the audit trail
  var replay SESSION_ID [--db PATH]             walk checkpoints step by step
  var verify-bundle BUNDLE.json [--key demo.key|--key-hex HEX]
                                                offline attestation verification
  var gate CLAIM [--proofs proofs.json]         show the evidence requirement
  var serve [--db PATH] [--port 8787]           verification API (HTTP)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from var_runtime.attestation import verify_bundle
from var_runtime.identity import TrustAnchor
from var_runtime.evidence import ProofRegistry
from var_runtime.runtime import VerifiableRuntime


def load_anchor(args: argparse.Namespace) -> TrustAnchor:
    hex_key = getattr(args, "key_hex", None) or os.environ.get("VAR_SIGNING_KEY")
    if getattr(args, "key", None):
        hex_key = open(args.key).read().strip()
    if hex_key:
        return TrustAnchor.from_secret_hex(hex_key)
    return TrustAnchor.generate()  # ephemeral: fine for inspecting unsigned data


def open_runtime(args: argparse.Namespace) -> VerifiableRuntime:
    return VerifiableRuntime(store=args.db, anchor=load_anchor(args),
                             proofs=getattr(args, "proofs", None))


def cmd_sessions(a):
    rt = open_runtime(a)
    for sid in rt.store.sessions():
        ck = rt.store.latest_checkpoint(sid)
        print(f"{sid}  last_step={ck[0] if ck else '-'}  "
              f"events={len(rt.store.load_events(sid))}")
    rt.store.close()


def cmd_verify(a):
    rt = open_runtime(a)
    report = rt.verify_session(a.session_id)
    print(json.dumps(report, indent=2))
    rt.store.close()
    sys.exit(0 if report.get("chain_valid") else 1)


def cmd_audit(a):
    rt = open_runtime(a)
    events = rt.audit(a.session_id, principal=a.principal, event_type=a.type)
    print(json.dumps(events, indent=2, default=str))
    rt.store.close()


def cmd_replay(a):
    rt = open_runtime(a)
    for ck in rt.store.checkpoints(a.session_id):
        s = ck["state"]
        print(f"step {ck['step_index']:>3}  tools={len(s.get('tool_results', {}))} "
              f"pending={len(s.get('pending_actions', []))} "
              f"memory_keys={list(s.get('memory', {}))}")
    rt.store.close()


def cmd_verify_bundle(a):
    anchor = load_anchor(a)
    report = verify_bundle(json.load(open(a.bundle)), anchor)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["events"].get("chain_valid") else 1)


def cmd_gate(a):
    reg = ProofRegistry.load(a.proofs)
    print(json.dumps(reg.requirement(a.claim), indent=2))


def cmd_serve(a):
    rt = open_runtime(a)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802 — http.server API
            routes = {
                "/sessions": lambda: {"sessions": rt.store.sessions()},
                "/verify": lambda: rt.verify_session(q["session_id"][0]),
                "/audit": lambda: {"events": rt.audit(
                    q["session_id"][0], principal=(q.get("principal") or [None])[0],
                    event_type=(q.get("type") or [None])[0])},
            }
            import urllib.parse
            u = urllib.parse.urlparse(self.path)
            q = urllib.parse.parse_qs(u.query)
            fn = routes.get(u.path.rstrip("/"))
            body = (fn() if fn else {"error": "not found", "path": u.path})
            data = json.dumps(body, default=str).encode()
            self.send_response(200 if fn else 404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *_):
            pass

    print(f"var verification API on http://localhost:{a.port} "
          f"(/sessions, /verify?session_id=…, /audit?session_id=…&principal=…)")
    HTTPServer(("", a.port), Handler).serve_forever()  # single-threaded: sqlite-safe


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="var")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sessions"); s.set_defaults(fn=cmd_sessions)
    s = sub.add_parser("verify"); s.add_argument("session_id"); s.set_defaults(fn=cmd_verify)
    s = sub.add_parser("audit"); s.add_argument("session_id")
    s.add_argument("--principal"); s.add_argument("--type"); s.set_defaults(fn=cmd_audit)
    s = sub.add_parser("replay"); s.add_argument("session_id"); s.set_defaults(fn=cmd_replay)
    s = sub.add_parser("verify-bundle"); s.add_argument("bundle")
    s.set_defaults(fn=cmd_verify_bundle)
    s = sub.add_parser("gate"); s.add_argument("claim")
    s.add_argument("--proofs", default="proofs.json"); s.set_defaults(fn=cmd_gate)
    s = sub.add_parser("serve"); s.add_argument("--port", type=int, default=8787)
    s.set_defaults(fn=cmd_serve)

    # shared options on every subcommand (usable after the subcommand)
    for sp in sub.choices.values():
        sp.add_argument("--db", default="var.db", help="runtime state store (sqlite)")
        sp.add_argument("--key", help="file containing hex signing key")
        sp.add_argument("--key-hex", help="hex signing key directly")

    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
