"""Evidence Gate — Proof-or-Stop.

Intercepts lifecycle claims. A claim ("tests_passed") is only admitted when
mechanically verifiable evidence exists: right type, fresh enough, bound to
the exact target, and independently checkable (content hash + signature).
Otherwise: HALT with structured error semantics so the agent can self-correct.
Every decision is a first-class record the runtime attests.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .errors import Category, StructuredError
from .identity import TrustAnchor, canonical

# Fetcher: (requirement, claim) -> evidence artifact dict (or None if the
# source has nothing). Register per deployment; see runtime + demo for builts.
Fetcher = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any] | None]


def artifact_content_hash(artifact: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(artifact["payload"])).hexdigest()


@dataclass
class ProofRegistry:
    """Declarative claim -> evidence-requirement mappings. JSON file or dict;
    `proofs.json` ships defaults, customers extend/override per domain."""
    claims: dict[str, dict[str, Any]]

    @classmethod
    def load(cls, path: str | Path) -> "ProofRegistry":
        data = json.loads(Path(path).read_text())
        return cls(claims=data["claims"])

    def requirement(self, claim: str) -> dict[str, Any]:
        req = self.claims.get(claim)
        if req is None:
            raise StructuredError(
                error_code="CLAIM_UNKNOWN", category=Category.VALIDATION,
                message=f"no proof requirement registered for claim '{claim}'",
                recovery={"strategy": "correct_input_and_retry", "max_retries": 0})
        return req


@dataclass
class GateDecision:
    claim: str
    decision: str                    # ADMIT | HALT
    evidence_type: str
    checks: dict[str, Any]
    error: StructuredError | None = None
    decided_at: int = 0

    @property
    def admitted(self) -> bool:
        return self.decision == "ADMIT"

    def to_dict(self) -> dict[str, Any]:
        d = {"claim": self.claim, "decision": self.decision,
             "evidence_type": self.evidence_type, "checks": self.checks,
             "decided_at": self.decided_at}
        if self.error:
            d["error"] = self.error.to_dict()
        return d


def _halt(code: str, message: str, recovery: str, **ctx: Any) -> StructuredError:
    return StructuredError(error_code=code, category=Category.VALIDATION,
                           message=message,
                           recovery={"strategy": recovery, "max_retries": 3},
                           context=ctx)


@dataclass
class GateEngine:
    registry: ProofRegistry
    fetchers: dict[str, Fetcher] = field(default_factory=dict)
    anchor: TrustAnchor | None = None   # verifies signed evidence artifacts
    now: Callable[[], float] = time.time  # injectable clock

    def register(self, source: str, fetcher: Fetcher) -> None:
        self.fetchers[source] = fetcher

    def evaluate(self, claim: dict[str, Any]) -> GateDecision:
        """claim = {claim, target: {...}, confidence} — Proof-or-Stop loop."""
        name, target = claim.get("claim"), claim.get("target", {})
        req = self.registry.requirement(name)
        etype = req["evidence_type"]
        decided = int(self.now())

        if req.get("min_confidence") and claim.get("confidence", 1.0) < req["min_confidence"]:
            return self._stop(name, etype, decided, _halt(
                "CONFIDENCE_TOO_LOW",
                f"confidence {claim.get('confidence')} < required {req['min_confidence']}",
                "regather_evidence", required=req["min_confidence"]))

        fetcher = self.fetchers.get(req["source"])
        if fetcher is None:
            raise StructuredError(
                error_code="FETCHER_MISSING", category=Category.PERMANENT,
                message=f"no fetcher registered for evidence source '{req['source']}'",
                recovery={"strategy": "escalate_to_human", "max_retries": 0})
        artifact = fetcher(req, claim)

        checks: dict[str, Any] = {}
        if artifact is None:
            return self._stop(name, etype, decided, _halt(
                "EVIDENCE_MISSING", f"no {etype} evidence available from "
                f"{req['source']}", req.get("recovery", "produce_evidence")))
        checks["present"] = True

        # 1. type
        if artifact.get("type") != etype:
            return self._stop(name, etype, decided, _halt(
                "EVIDENCE_TYPE_MISMATCH",
                f"evidence type {artifact.get('type')!r} != required {etype!r}",
                "produce_evidence"), checks)
        checks["type"] = True

        # 2. freshness
        max_age = req.get("max_age_seconds")
        if max_age is not None:
            age = self.now() - artifact.get("produced_at", 0)
            checks["age_seconds"] = round(age, 1)
            if age > max_age:
                return self._stop(name, etype, decided, _halt(
                    "EVIDENCE_STALE",
                    f"evidence age {age:.0f}s exceeds max_age_seconds={max_age}",
                    req.get("recovery", "re_run_tests"),
                    required_age_seconds=max_age, actual_age_seconds=round(age, 1)),
                    checks)
            checks["fresh"] = True

        # 3. source-binding: every required field must pin the claim's target
        for binding in req.get("must_bind_to", []):
            got = artifact.get("bindings", {}).get(binding)
            want = target.get(binding)
            if got is None or got != want:
                return self._stop(name, etype, decided, _halt(
                    "EVIDENCE_UNBOUND",
                    f"evidence binding '{binding}'={got!r} does not pin target {want!r}",
                    "re_run_on_target", field=binding, expected=want, actual=got),
                    checks)
            checks[f"bound:{binding}"] = True

        # 4. mechanical verifiability: content hash recomputes; signature, if
        #    present, verifies against the trust anchor
        if artifact_content_hash(artifact) != artifact.get("content_hash"):
            return self._stop(name, etype, decided, _halt(
                "EVIDENCE_HASH_MISMATCH",
                "evidence content hash does not match payload",
                "re_fetch_evidence"), checks)
        checks["content_hash"] = True
        sig = artifact.get("signature")
        if sig is not None:
            if self.anchor is None or not self.anchor.verify_sig(
                    artifact["content_hash"].encode(), sig,
                    artifact.get("key_id", "")):
                return self._stop(name, etype, decided, _halt(
                    "EVIDENCE_SIGNATURE_INVALID",
                    "evidence artifact signature failed verification",
                    "re_fetch_evidence"), checks)
            checks["signed"] = True

        # 5. semantic pass/fail of the artifact itself (e.g. tests: failed run
        #    is fresh and bound but still not admissible)
        if artifact.get("payload", {}).get("passed") is False:
            return self._stop(name, etype, decided, _halt(
                "EVIDENCE_NEGATIVE", "evidence is present and valid but the "
                "result it proves is a failure", req.get("recovery", "fix_and_re_run")),
                checks)
        checks["passed"] = True

        return GateDecision(claim=name, decision="ADMIT", evidence_type=etype,
                            checks=checks, decided_at=decided)

    @staticmethod
    def _stop(name: str, etype: str, decided: int,
              err: StructuredError, checks: dict[str, Any] | None = None) -> GateDecision:
        return GateDecision(claim=name, decision="HALT", evidence_type=etype,
                            checks=checks or {}, error=err, decided_at=decided)


def make_signed_artifact(etype: str, source: str, payload: dict[str, Any],
                         bindings: dict[str, Any], anchor: TrustAnchor,
                         produced_at: float | None = None) -> dict[str, Any]:
    """Helper for evidence producers (CI systems, approval logs): build an
    artifact whose integrity is mechanically checkable and signed."""
    chash = hashlib.sha256(canonical(payload)).hexdigest()
    sig, kid = anchor.sign(chash.encode())
    return {"type": etype, "source": source, "produced_at": produced_at or time.time(),
            "bindings": bindings, "payload": payload, "content_hash": chash,
            "signature": sig, "key_id": kid}
