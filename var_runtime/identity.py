"""Identity Broker — signed identity propagation through every tool call.

Creates a JWT-shaped envelope (header.payload.signature, base64url, HMAC-
SHA256) carrying principal, agent, scoped permissions, approval chain, and
expiry. Injected into MCP `_meta` as `io.var.identity.envelope`.

ponytail: HMAC (symmetric) — anyone who can verify can also sign. Swap the
sign/verify pair for Ed25519 via `cryptography` when third parties must
verify without holding the signing key; the envelope format stays identical.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass, field
from typing import Any

META_KEY = "io.var.identity.envelope"
DEFAULT_TTL_SECONDS = 3600


def _b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


@dataclass
class TrustAnchor:
    """Key registry. Verifiers look up the runtime key by key_id."""
    keys: dict[str, bytes] = field(default_factory=dict)
    active_key_id: str = "var-key-1"

    @classmethod
    def generate(cls, key_id: str = "var-key-1") -> "TrustAnchor":
        return cls(keys={key_id: hashlib.sha256(
            f"var-{key_id}-{time.time_ns()}".encode()).digest()}, active_key_id=key_id)

    @classmethod
    def from_secret_hex(cls, hex_secret: str, key_id: str = "var-key-1") -> "TrustAnchor":
        return cls(keys={key_id: bytes.fromhex(hex_secret)}, active_key_id=key_id)

    def sign(self, payload: bytes) -> tuple[str, str]:
        kid = self.active_key_id
        sig = hmac.new(self.keys[kid], payload, hashlib.sha256).digest()
        return _b64(sig), kid

    def verify_sig(self, payload: bytes, sig_b64: str, key_id: str) -> bool:
        key = self.keys.get(key_id)
        if key is None:
            return False
        return hmac.compare_digest(hmac.new(key, payload, hashlib.sha256).digest(),
                                   _unb64(sig_b64))


class IdentityError(Exception):
    pass


@dataclass
class IdentityEnvelope:
    principal_id: str
    agent_id: str
    session_id: str
    permissions: list[str]
    issued_at: int
    expiry: int
    approval_chain: list[dict[str, Any]] = field(default_factory=list)

    def to_payload(self) -> dict[str, Any]:
        return {"principal_id": self.principal_id, "agent_id": self.agent_id,
                "session_id": self.session_id, "permissions": sorted(self.permissions),
                "approval_chain": self.approval_chain,
                "iat": self.issued_at, "exp": self.expiry}

    def has_permission(self, perm: str) -> bool:
        return perm in self.permissions or "*" in self.permissions

    def require(self, perm: str) -> None:
        if not self.has_permission(perm):
            raise IdentityError(
                f"principal {self.principal_id} lacks permission '{perm}' "
                f"(has: {self.permissions})")

    def with_approval(self, approver: str, role: str, claim: str,
                      anchor: "TrustAnchor", now: int | None = None) -> str:
        """Re-issue with a human approval appended (step 8 of the lifecycle)."""
        self.approval_chain.append({"approver": approver, "role": role,
                                    "claim": claim, "approved_at": int(now or time.time())})
        return issue(self, anchor)

    # -- token encode/decode -------------------------------------------------

    def encode(self, anchor: TrustAnchor) -> str:
        header = {"alg": "HS256", "typ": "JWT", "kid": anchor.active_key_id}
        signing_input = f"{_b64(canonical(header))}.{_b64(canonical(self.to_payload()))}"
        sig, _ = anchor.sign(signing_input.encode())
        return f"{signing_input}.{sig}"

    @classmethod
    def decode(cls, token: str) -> "IdentityEnvelope":
        parts = token.split(".")
        if len(parts) != 3:
            raise IdentityError("malformed envelope: expected 3 segments")
        payload = json.loads(_unb64(parts[1]))
        return cls(principal_id=payload["principal_id"], agent_id=payload["agent_id"],
                   session_id=payload["session_id"], permissions=payload["permissions"],
                   issued_at=payload["iat"], expiry=payload["exp"],
                   approval_chain=payload.get("approval_chain", []))


def issue(envelope: IdentityEnvelope, anchor: TrustAnchor) -> str:
    return envelope.encode(anchor)


def verify(token: str, anchor: TrustAnchor, *, now: int | None = None,
           require_permission: str | None = None) -> IdentityEnvelope:
    """Full verification: signature, expiry, optional permission. Security
    path — no lazy shortcuts."""
    parts = token.split(".")
    if len(parts) != 3:
        raise IdentityError("malformed envelope: expected 3 segments")
    header = json.loads(_unb64(parts[0]))
    if header.get("alg") != "HS256":
        raise IdentityError(f"unsupported alg {header.get('alg')!r}")
    sig, kid = parts[2], header.get("kid", "")
    if not anchor.verify_sig(f"{parts[0]}.{parts[1]}".encode(), sig, kid):
        raise IdentityError("envelope signature verification failed")
    env = IdentityEnvelope.decode(token)
    ts = int(now if now is not None else time.time())
    if ts >= env.expiry:
        raise IdentityError(f"envelope expired at {env.expiry} (now {ts})")
    if require_permission is not None:
        env.require(require_permission)
    return env


def inject_meta(token: str, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the MCP `_meta` payload carrying the envelope."""
    meta = dict(meta or {})
    meta[META_KEY] = token
    return meta
