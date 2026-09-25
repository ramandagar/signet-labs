"""varclient — Python SDK for the VAR hosted API. Zero dependencies.

    from varclient import VarClient
    var = VarClient("http://localhost:8788", "var_live_…")
    s = var.create_session(permissions=["run:tests"], max_usd=2.0)
    d = var.gate_claim(s.session_id, "tests_passed", {"commit_sha": sha})
    if d.admitted: ...
    else: print(d.error["recovery"])
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class VarApiError(Exception):
    def __init__(self, status: int, body: dict):
        self.status, self.body = status, body
        super().__init__(f"{status}: {body.get('error', {}).get('message', body)}")


class VarClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None,
                 timeout: int = 30):
        self.base = (base_url or os.environ.get("VAR_URL", "http://localhost:8788")).rstrip("/")
        self.key = api_key or os.environ.get("VAR_API_KEY", "")
        self.timeout = timeout

    def _req(self, method: str, path: str, body: dict | None = None) -> Any:
        req = urllib.request.Request(
            self.base + path, method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": f"Bearer {self.key}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            raise VarApiError(e.code, json.loads(e.read() or b"{}")) from None

    # -- sessions -----------------------------------------------------------------

    def create_session(self, permissions: list[str], *, agent_id: str = "agent",
                       max_usd: float | None = None, max_tokens: int | None = None,
                       max_wall_clock_seconds: int | None = None) -> dict:
        budget = {k: v for k, v in dict(max_usd=max_usd, max_tokens=max_tokens,
                max_wall_clock_seconds=max_wall_clock_seconds).items() if v is not None}
        return self._req("POST", "/v1/sessions",
                         {"agent_id": agent_id, "permissions": permissions,
                          **({"budget": budget} if budget else {})})

    def sessions(self) -> list[dict]:
        return self._req("GET", "/v1/sessions")["sessions"]

    def session_state(self, session_id: str) -> dict:
        return self._req("GET", f"/v1/sessions/{session_id}")

    def resume(self, session_id: str) -> dict:
        return self._req("POST", f"/v1/sessions/{session_id}/resume")

    def checkpoint(self, session_id: str, *, memory: dict | None = None,
                   messages: list | None = None) -> dict:
        return self._req("POST", f"/v1/sessions/{session_id}/checkpoint",
                         {"memory": memory or {}, "messages": messages or []})

    # -- Proof-or-Stop --------------------------------------------------------------

    def gate_claim(self, session_id: str, claim: str, target: dict,
                   confidence: float = 1.0) -> "GateResult":
        return GateResult(self._req("POST", f"/v1/sessions/{session_id}/gate",
                                    {"claim": claim, "target": target,
                                     "confidence": confidence}))

    def record_approval(self, session_id: str, approver: str, role: str,
                        claim: str, target: dict) -> dict:
        return self._req("POST", f"/v1/sessions/{session_id}/approvals",
                         {"approver": approver, "role": role, "claim": claim,
                          "target": target})

    # -- metering / attestation -------------------------------------------------------

    def meter_llm(self, session_id: str, stakes: str, input_tokens: int,
                  output_tokens: int) -> dict:
        return self._req("POST", f"/v1/sessions/{session_id}/meter",
                         {"kind": "llm", "stakes": stakes,
                          "input_tokens": input_tokens,
                          "output_tokens": output_tokens})

    def usage(self, session_id: str) -> dict:
        return self._req("GET", f"/v1/sessions/{session_id}/usage")

    def verify(self, session_id: str) -> dict:
        return self._req("GET", f"/v1/sessions/{session_id}/verify")

    def audit(self, session_id: str, *, principal: str | None = None,
              event_type: str | None = None) -> list[dict]:
        q = "?" + "&".join(f"{k}={v}" for k, v in
                           dict(principal=principal, type=event_type).items() if v)
        return self._req("GET", f"/v1/sessions/{session_id}/audit{q}")["events"]

    def perf(self) -> dict:
        return self._req("GET", "/v1/perf")["tools"]

    def proofs(self) -> list[str]:
        return self._req("GET", "/v1/proofs")["claims"]

    def billing_checkout(self, plan: str) -> dict:
        return self._req("POST", "/v1/billing/checkout", {"plan": plan})


class GateResult(dict):
    def __getattr__(self, k: str) -> Any:
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k) from None

    @property
    def admitted(self) -> bool:
        return self.get("decision") == "ADMIT"

    @property
    def error(self) -> dict:
        return self.get("error", {})

    @property
    def recovery(self) -> str:
        return self.error.get("recovery", {}).get("strategy", "")
