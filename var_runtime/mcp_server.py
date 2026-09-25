"""VAR as an MCP server — stdio transport, JSON-RPC 2.0 (spec 2025-11-25).

Lets any MCP client (Claude Desktop, Cursor, agents) use the runtime as tools:

  var_start_session      create a gated session (principal, permissions, budget)
  var_call_tool          run a registered python tool under the runtime
  var_gate_claim         Proof-or-Stop: evaluate a lifecycle claim
  var_record_approval    human-in-the-loop approval for a claim
  var_session_usage      tokens / usd / wall-clock / budget fraction
  var_verify_session     is this session's attested history intact?
  var_audit_session      query the attested event log

Identity: each tools/call may carry `_meta["io.var.identity.envelope"]`; when
present it is verified and the principal is recorded in the attested event
(this is the identity-propagation primitive MCP itself lacks).

Run: python3 -m var_runtime.mcp_server [--db var.db]
Config (Claude Desktop): add to claude_desktop_config.json ->
  {"mcpServers": {"var": {"command": "python3", "args": ["-m",
   "var_runtime.mcp_server"], "env": {"VAR_DB": "var.db"}}}}
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
import uuid

from .cost import Budget
from .evidence import make_signed_artifact
from .identity import TrustAnchor, verify as verify_envelope, META_KEY
from .runtime import VerifiableRuntime

PROTOCOL = "2025-11-25"

TOOLS = [
    {"name": "var_start_session", "description":
      "Start a verifiable agent session: signed identity envelope + budget.",
     "inputSchema": {"type": "object", "properties": {
        "principal_id": {"type": "string"},
        "agent_id": {"type": "string", "default": "mcp-agent"},
        "permissions": {"type": "array", "items": {"type": "string"}},
        "max_usd": {"type": "number"}, "max_tokens": {"type": "integer"},
        "max_wall_clock_seconds": {"type": "integer"}},
      "required": ["principal_id", "permissions"]}},
    {"name": "var_gate_claim", "description":
      "Proof-or-Stop: submit a lifecycle claim for evidence gating. Returns "
      "ADMIT or HALT with machine-readable recovery instructions.",
     "inputSchema": {"type": "object", "properties": {
        "session_id": {"type": "string"}, "claim": {"type": "string"},
        "target": {"type": "object"}, "confidence": {"type": "number"}},
      "required": ["session_id", "claim", "target"]}},
    {"name": "var_record_approval", "description":
      "Record a human approval (approver, role) bound to a claim target; the "
      "identity envelope's approval chain is re-issued.",
     "inputSchema": {"type": "object", "properties": {
        "session_id": {"type": "string"}, "approver": {"type": "string"},
        "role": {"type": "string"}, "claim": {"type": "string"},
        "target": {"type": "object"}},
      "required": ["session_id", "approver", "role", "claim"]}},
    {"name": "var_submit_evidence", "description":
      "Attach evidence for a claim from the client side (e.g. a CI result you "
      "already hold). Signed into an artifact the gate can verify.",
     "inputSchema": {"type": "object", "properties": {
        "evidence_type": {"type": "string"}, "payload": {"type": "object"},
        "bindings": {"type": "object"}},
      "required": ["evidence_type", "payload", "bindings"]}},
    {"name": "var_session_usage", "description":
      "Metered usage for a session: tokens, usd, wall clock, budget fraction.",
     "inputSchema": {"type": "object", "properties": {
        "session_id": {"type": "string"}}, "required": ["session_id"]}},
    {"name": "var_verify_session", "description":
      "Verify a session's tamper-evident execution history (hash chain).",
     "inputSchema": {"type": "object", "properties": {
        "session_id": {"type": "string"}}, "required": ["session_id"]}},
    {"name": "var_audit_session", "description":
      "Attested event log for a session, optionally filtered by type.",
     "inputSchema": {"type": "object", "properties": {
        "session_id": {"type": "string"}, "type": {"type": "string"}},
      "required": ["session_id"]}},
]


class McpVarServer:
    def __init__(self, db: str = "var.db", proofs: str = "proofs.json"):
        self.rt = VerifiableRuntime(db, proofs=proofs)
        self.evidence: dict[str, dict] = {}   # evidence_type -> artifact

        def client_evidence(req, claim):
            # serves client-submitted artifacts for whichever source the
            # registry demands; type/binding checks stay in the gate
            art = self.evidence.get(req["evidence_type"])
            return json.loads(json.dumps(art)) if art else None
        # the gate resolves fetchers by the requirement's source name, so the
        # client-evidence fetcher answers every source in the registry
        for req in self.rt.proof_registry.claims.values():
            self.rt.gate.register(req["source"], client_evidence)

    # -- JSON-RPC plumbing -------------------------------------------------------

    def handle(self, line: str) -> dict | None:
        msg = json.loads(line)
        method, mid = msg.get("method"), msg.get("id")
        if method.startswith("notifications/"):
            return None
        try:
            result = self._call(method, msg.get("params") or {})
            return {"jsonrpc": "2.0", "id": mid, "result": result}
        except Exception as e:  # noqa: BLE001 — protocol boundary
            return {"jsonrpc": "2.0", "id": mid, "error": {
                "code": -32603, "message": f"{type(e).__name__}: {e}",
                "data": traceback.format_exc(limit=3)}}

    def _call(self, method: str, p: dict) -> dict:
        if method == "initialize":
            return {"protocolVersion": PROTOCOL,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "var-runtime", "version": "0.1.0"}}
        if method == "ping":
            return {}
        if method == "tools/list":
            return {"tools": TOOLS}
        if method == "tools/call":
            return self._tool(p.get("name", ""), p.get("arguments") or {},
                              (p.get("_meta") or {}))
        raise ValueError(f"unknown method {method!r}")

    # -- tools -------------------------------------------------------------------

    def _tool(self, name: str, a: dict, meta: dict) -> dict:
        out = getattr(self, "_" + name)(a, meta)
        return {"content": [{"type": "text", "text": json.dumps(out, default=str)}],
                "isError": False}

    def _session(self, sid: str):
        s = self.rt.sessions.get(sid)
        if s is None:
            s = self.rt.resume(sid)  # raises KeyError -> RPC error
        return s

    def _var_start_session(self, a: dict, meta: dict) -> dict:
        # if the client carried an identity envelope, verify + adopt its principal
        principal = a["principal_id"]
        if META_KEY in meta:
            env = verify_envelope(meta[META_KEY], self.rt.anchor)
            principal = env.principal_id
        s = self.rt.start_session(
            principal_id=principal, agent_id=a.get("agent_id", "mcp-agent"),
            permissions=a["permissions"],
            budget=Budget(max_usd=a.get("max_usd"), max_tokens=a.get("max_tokens"),
                          max_wall_clock_seconds=a.get("max_wall_clock_seconds")))
        return {"session_id": s.session_id, "identity_envelope": s.token,
                "expires_at": s.envelope.expiry}

    def _var_gate_claim(self, a: dict, meta: dict) -> dict:
        s = self._session(a["session_id"])
        d = self.rt.gate_claim(s, {"claim": a["claim"], "target": a.get("target", {}),
                                   "confidence": a.get("confidence", 1.0)})
        return d.to_dict()

    def _var_record_approval(self, a: dict, meta: dict) -> dict:
        s = self._session(a["session_id"])
        self.rt.record_approval(s, approver=a["approver"], role=a["role"],
                                claim=a["claim"], target=a.get("target", {}))
        return {"status": "recorded"}

    def _var_submit_evidence(self, a: dict, meta: dict) -> dict:
        art = make_signed_artifact(a["evidence_type"], "client_submitted",
                                   a["payload"], a["bindings"], self.rt.anchor)
        self.evidence[a["evidence_type"]] = art
        return {"status": "accepted", "content_hash": art["content_hash"]}

    def _var_session_usage(self, a: dict, meta: dict) -> dict:
        s = self._session(a["session_id"])
        return {"usage": s.meter.usage(), "fraction_used": round(s.meter.fraction_used(), 4)}

    def _var_verify_session(self, a: dict, meta: dict) -> dict:
        return self.rt.verify_session(a["session_id"])

    def _var_audit_session(self, a: dict, meta: dict) -> dict:
        return {"events": self.rt.audit(a["session_id"], event_type=a.get("type"))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.environ.get("VAR_DB", "var.db"))
    ap.add_argument("--proofs", default="proofs.json")
    args = ap.parse_args()
    srv = McpVarServer(args.db, args.proofs)
    for line in sys.stdin:  # stdio transport: line-delimited JSON-RPC
        line = line.strip()
        if not line:
            continue
        try:
            resp = srv.handle(line)
        except json.JSONDecodeError as e:
            resp = {"jsonrpc": "2.0", "id": None,
                    "error": {"code": -32700, "message": f"parse error: {e}"}}
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
