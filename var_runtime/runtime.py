"""VerifiableRuntime — the control layer tying all six features together.

Every tool call passes through: identity verification + permission check ->
budget check -> envelope injection into MCP `_meta` -> execution with timing ->
SERF error classification -> performance recording -> attestation ->
checkpoint. Claims pass through the Evidence Gate before any lifecycle
advances. Crash recovery reloads the latest checkpoint; the attested chain
makes every decision independently re-verifiable.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .attestation import EventChain, export_bundle, verify_bundle
from .cost import Budget, Meter, ModelRouter, ToolPerformanceRegistry
from .evidence import GateEngine, ProofRegistry, make_signed_artifact
from .errors import StructuredError, classify
from .identity import (IdentityEnvelope, TrustAnchor, inject_meta, issue, verify)
from .state import StateStore


@dataclass
class Session:
    session_id: str
    envelope: IdentityEnvelope
    token: str
    meter: Meter
    chain: EventChain
    step: int = 0
    messages: list[dict[str, Any]] = field(default_factory=list)
    tool_results: dict[str, Any] = field(default_factory=dict)
    memory: dict[str, Any] = field(default_factory=dict)
    pending_actions: list[dict[str, Any]] = field(default_factory=list)

    def state(self) -> dict[str, Any]:
        return {"session_id": self.session_id, "step_index": self.step,
                "messages": self.messages, "tool_results": self.tool_results,
                "memory": self.memory, "pending_actions": self.pending_actions,
                "identity_envelope": self.token}


class VerifiableRuntime:
    def __init__(self, store: StateStore | str = ":memory:",
                 anchor: TrustAnchor | None = None,
                 proofs: str | Path | ProofRegistry | None = None,
                 retry_backoff_scale: float = 1.0):
        self.store = store if isinstance(store, StateStore) else StateStore(store)
        self.anchor = anchor or TrustAnchor.generate()
        self.proof_registry = (proofs if isinstance(proofs, ProofRegistry)
                               else ProofRegistry(proofs["claims"]) if isinstance(proofs, dict)
                               else ProofRegistry.load(proofs) if proofs
                               else ProofRegistry(claims={}))
        self.gate = GateEngine(self.proof_registry, anchor=self.anchor)
        self.router = ModelRouter()
        self.perf = ToolPerformanceRegistry(self.store)
        self.retry_backoff_scale = retry_backoff_scale
        self.sessions: dict[str, Session] = {}

        # human approvals recorded this process; keyed for the approval fetcher
        self._approvals: dict[str, list[dict[str, Any]]] = {}
        self.gate.register("approval_log", self._fetch_approval)

    # -- session lifecycle ------------------------------------------------------

    def start_session(self, *, principal_id: str, agent_id: str,
                      permissions: list[str], budget: Budget | None = None,
                      ttl_seconds: int = 3600) -> Session:
        sid = f"s_{uuid.uuid4().hex[:12]}"
        now = int(time.time())
        env = IdentityEnvelope(principal_id=principal_id, agent_id=agent_id,
                               session_id=sid, permissions=permissions,
                               issued_at=now, expiry=now + ttl_seconds)
        session = Session(session_id=sid, envelope=env, token=issue(env, self.anchor),
                          meter=Meter(budget or Budget()),
                          chain=EventChain(anchor=self.anchor))
        self.sessions[sid] = session
        self._attest(session, {"type": "session_started",
                               "principal": principal_id, "agent": agent_id,
                               "permissions": permissions,
                               "budget": vars(budget) if budget else None})
        self.checkpoint(session)
        return session

    def resume(self, session_id: str) -> Session:
        """Crash recovery: reload latest checkpoint + persisted event chain.
        Completed steps are not re-executed (no re-payment)."""
        ck = self.store.latest_checkpoint(session_id)
        if ck is None:
            raise KeyError(f"no checkpoints for session {session_id}")
        _, state = ck
        env = IdentityEnvelope.decode(state["identity_envelope"])
        chain = EventChain.from_dict(self.store.load_events(session_id), self.anchor)
        session = Session(session_id=session_id, envelope=env,
                          token=state["identity_envelope"],
                          meter=Meter(budget=Budget(**state["budget"]),
                                      tokens=state.get("meter", {}).get("tokens", 0),
                                      usd=state.get("meter", {}).get("usd", 0.0)),
                          chain=chain, step=state["step_index"],
                          messages=state.get("messages", []),
                          tool_results=state.get("tool_results", {}),
                          memory=state.get("memory", {}),
                          pending_actions=state.get("pending_actions", []))
        self.sessions[session_id] = session
        self._attest(session, {"type": "session_resumed", "from_step": session.step})
        return session

    # -- tool calls: the intercept path -----------------------------------------

    def call_tool(self, session: Session, tool: str, fn: Callable[..., Any],
                  *, permission: str | None = None, tool_call_id: str | None = None,
                  retry_on_transient: bool = True, **kwargs: Any) -> Any:
        """Identity-verified, metered, SERF-wrapped, attested, checkpointed
        tool invocation. The envelope rides in `meta` (MCP `_meta`)."""
        tc_id = tool_call_id or f"tc_{uuid.uuid4().hex[:8]}"
        session.step += 1

        # identity: full verification on every call — signature, expiry, scope
        env = verify(session.token, self.anchor)
        if permission:
            env.require(permission)

        # budget pre-check
        self._budget_guard(session)

        meta = inject_meta(session.token)
        started = time.monotonic()
        attempt, err = 0, None
        while True:
            try:
                result = fn(meta=meta, **kwargs)
                ok = True
                break
            except Exception as raw:  # noqa: BLE001 — SERF classifies everything
                err = classify(raw, tool_name=tool)
                err.context.update({"tool_call_id": tc_id, "attempt": attempt + 1,
                                    "latency_ms": round((time.monotonic() - started) * 1000, 1)})
                ok = False
                if (retry_on_transient and err.should_retry
                        and attempt < err.recovery.get("max_retries", 0)):
                    self._attest(session, {"type": "tool_retry", "tool": tool,
                                           "attempt": attempt + 1,
                                           "error": err.error_code})
                    session.meter.retries += 1
                    time.sleep(err.next_backoff(attempt) * self.retry_backoff_scale)  # ponytail: fixed backoff, jitter if fleets collide
                    attempt += 1
                    continue
                result = None
                break

        latency_ms = (time.monotonic() - started) * 1000
        session.meter.meter_tool(latency_ms, retry=attempt > 0)
        self.perf.record(tool, latency_ms, ok)
        self.store.commit()

        event = {"type": "tool_call", "tool": tool, "tool_call_id": tc_id,
                 "principal": env.principal_id, "attempt": attempt + 1,
                 "latency_ms": round(latency_ms, 1), "ok": ok}
        if ok:
            session.tool_results[tc_id] = result
            event["result_digest"] = _digest(result)
        else:
            event["error"] = err.to_dict()
        self._attest(session, event)
        if not ok:
            raise err
        self.checkpoint(session)
        return result

    # -- LLM calls: metering + stakes routing ------------------------------------

    def llm_call(self, session: Session, *, stakes: str,
                 input_tokens: int, output_tokens: int) -> dict[str, Any]:
        model = self.router.route(stakes, session.meter.fraction_used())
        cost = session.meter.meter_llm(model, input_tokens, output_tokens)
        self._attest(session, {"type": "llm_call", "model": model, "stakes": stakes,
                               "input_tokens": input_tokens,
                               "output_tokens": output_tokens,
                               "cost_usd": round(cost, 6)})
        self._budget_guard(session)
        self.checkpoint(session)
        return {"model": model, "cost_usd": round(cost, 6)}

    def _budget_guard(self, session: Session) -> None:
        report = session.meter.check()
        if report["status"] != "ok":
            self._attest(session, {"type": "budget_event", **report})

    # -- Proof-or-Stop -----------------------------------------------------------

    def gate_claim(self, session: Session, claim: dict[str, Any]) -> Any:
        """Evaluate a lifecycle claim. ADMIT advances; HALT returns the
        decision carrying structured error semantics (does not raise — the
        caller decides whether to correct, escalate, or abort)."""
        claim = {**claim, "session_id": session.session_id}  # binds approval lookup
        decision = self.gate.evaluate(claim)
        self._attest(session, {"type": "gate_decision", **decision.to_dict()})
        key = (claim["claim"], json.dumps(claim.get("target", {}), sort_keys=True))
        session.pending_actions = [p for p in session.pending_actions
                                   if (p.get("claim"), json.dumps(p.get("target", {}), sort_keys=True)) != key]
        if not decision.admitted:
            session.pending_actions.append(claim)  # blocked claim awaits correction
        self.checkpoint(session)
        return decision

    def record_approval(self, session: Session, *, approver: str, role: str,
                        claim: str, target: dict[str, Any]) -> None:
        """Human-in-the-loop: record an approval; re-issues the envelope with
        the approval chained so downstream calls carry it."""
        entry = {"approver": approver, "role": role, "claim": claim,
                 "target": target, "approved_at": time.time()}
        self._approvals.setdefault(session.session_id, []).append(entry)
        session.token = session.envelope.with_approval(approver, role, claim,
                                                       self.anchor)
        self._attest(session, {"type": "human_approval", **entry})

    def _fetch_approval(self, req: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any] | None:
        """Evidence fetcher for the approval_log source: newest matching
        approval (same claim, required approver role, bound to target).
        Falls back to the attested chain so approvals survive crashes."""
        role = req.get("approver_role")
        candidates = list(self._approvals.get(claim.get("session_id", "")) or [])
        for e in self.store.load_events(claim.get("session_id", "")):
            if e["event"].get("type") == "human_approval":
                candidates.append(e["event"])
        for entry in reversed(candidates):
            if entry["claim"] != claim["claim"]:
                continue
            if role and entry["role"] != role:
                continue
            return make_signed_artifact(
                "human_approval", "approval_log",
                {"passed": True, "approver": entry["approver"], "role": entry["role"]},
                bindings=entry["target"], anchor=self.anchor,
                produced_at=entry["approved_at"])
        return None

    # -- checkpoints / attestation / audit ----------------------------------------

    def checkpoint(self, session: Session) -> None:
        state = session.state()
        state["budget"] = {k: v for k, v in vars(session.meter.budget).items()}
        state["meter"] = {"tokens": session.meter.tokens,
                          "usd": round(session.meter.usd, 6)}
        self.store.save_checkpoint(session.session_id, session.step, state)
        self.store.commit()

    def _attest(self, session: Session, event: dict[str, Any]) -> None:
        entry = session.chain.append(event)
        self.store.append_event(session.session_id, {
            "seq": entry.seq, "prev_hash": entry.prev_hash, "event": entry.event,
            "hash": entry.hash, "batch_signature": entry.batch_signature,
            "key_id": entry.key_id})
        self.store.commit()

    def verify_session(self, session_id: str) -> dict[str, Any]:
        """Verification API: has this session's history been tampered with?"""
        events = self.store.load_events(session_id)
        if not events:
            return {"session_id": session_id, "chain_valid": False,
                    "error": "no events recorded for session"}
        chain = EventChain.from_dict(events, self.anchor)
        try:
            return {"session_id": session_id, **chain.verify()}
        except Exception as e:  # TamperError or corrupted rows
            return {"session_id": session_id, "chain_valid": False, "error": str(e)}

    def export_session(self, session_id: str) -> dict[str, Any]:
        chain = EventChain.from_dict(self.store.load_events(session_id), self.anchor)
        return export_bundle(session_id, chain)

    def verify_bundle(self, bundle: dict[str, Any]) -> dict[str, Any]:
        return verify_bundle(bundle, self.anchor)

    def audit(self, session_id: str, *, principal: str | None = None,
              event_type: str | None = None) -> list[dict[str, Any]]:
        """Queryable audit trail: every action with full identity context."""
        events = [e["event"] for e in self.store.load_events(session_id)]
        if principal:
            events = [e for e in events if e.get("principal") == principal
                      or e.get("approver") == principal]
        if event_type:
            events = [e for e in events if e.get("type") == event_type]
        return events


def _digest(result: Any) -> str:
    import hashlib
    import json
    return hashlib.sha256(json.dumps(result, sort_keys=True,
                                     default=str).encode()).hexdigest()[:16]
