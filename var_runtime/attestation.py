"""Attestation & Provenance — tamper-evident execution history.

Dapr-compatible model: every runtime event is hashed (SHA-256) and linked to
the previous event's hash; batches of events are signed and each signature
covers the preceding signature, so removing or editing any event breaks the
chain downstream. Bundles verify offline against a TrustAnchor.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any

from .identity import TrustAnchor, canonical


def event_digest(prev_hash: str, event: dict[str, Any]) -> str:
    return hashlib.sha256(
        bytes.fromhex(prev_hash) + canonical(event)).hexdigest()


GENESIS = "00" * 32


@dataclass
class ChainEntry:
    seq: int
    prev_hash: str
    event: dict[str, Any]
    hash: str
    batch_signature: str | None = None  # set on the last entry of a signed batch
    key_id: str | None = None


@dataclass
class EventChain:
    """In-memory chain; the StateStore persists entries (append-only)."""
    anchor: TrustAnchor
    entries: list[ChainEntry] = field(default_factory=list)
    last_signature: str = "(genesis)"

    def append(self, event: dict[str, Any], *, sign_batch: bool = True) -> ChainEntry:
        prev = self.entries[-1].hash if self.entries else GENESIS
        e = dict(event)
        e.setdefault("ts", int(time.time()))
        entry = ChainEntry(seq=len(self.entries), prev_hash=prev, event=e,
                           hash=event_digest(prev, e))
        if sign_batch:
            payload = f"{entry.hash}:{self.last_signature}".encode()
            sig, kid = self.anchor.sign(payload)
            entry.batch_signature, entry.key_id = sig, kid
            self.last_signature = sig
        self.entries.append(entry)
        return entry

    # -- verification ---------------------------------------------------------

    def verify(self) -> dict[str, Any]:
        """Re-walk the whole chain: recompute hashes, check links and batch
        signatures. Returns a report; raises on tamper with the exact break."""
        prev, last_sig = GENESIS, "(genesis)"
        for e in self.entries:
            if e.prev_hash != prev:
                raise TamperError(f"entry {e.seq}: prev_hash broken (chain forked)")
            if event_digest(prev, e.event) != e.hash:
                raise TamperError(f"entry {e.seq}: hash mismatch "
                                  f"(event modified or entries removed)")
            if e.batch_signature is not None:
                payload = f"{e.hash}:{last_sig}".encode()
                if not self.anchor.verify_sig(payload, e.batch_signature,
                                              e.key_id or ""):
                    raise TamperError(f"entry {e.seq}: batch signature invalid")
                last_sig = e.batch_signature
            prev = e.hash
        return {"chain_valid": True, "length": len(self.entries),
                "head_hash": prev, "signed_by": self.anchor.active_key_id}

    def to_dict(self) -> list[dict[str, Any]]:
        # dict(e.event): copy — exports/rebuilds must not alias live entries
        return [{"seq": e.seq, "prev_hash": e.prev_hash, "event": dict(e.event),
                 "hash": e.hash, "batch_signature": e.batch_signature,
                 "key_id": e.key_id} for e in self.entries]

    @classmethod
    def from_dict(cls, data: list[dict[str, Any]], anchor: TrustAnchor) -> "EventChain":
        chain = cls(anchor=anchor)
        for d in data:
            chain.entries.append(ChainEntry(**d))
        signed = [e for e in chain.entries if e.batch_signature]
        if signed:
            chain.last_signature = signed[-1].batch_signature
        return chain


class TamperError(Exception):
    pass


def verify_bundle(bundle: dict[str, Any], anchor: TrustAnchor) -> dict[str, Any]:
    """Offline verification of an exported attestation bundle."""
    report = {"session_id": bundle.get("session_id"),
              "exported_at": bundle.get("exported_at"), "events": {}}
    chain = EventChain.from_dict(bundle["chain"], anchor)
    try:
        report["events"] = chain.verify()
    except TamperError as t:
        report["events"] = {"chain_valid": False, "error": str(t)}
    return report


def export_bundle(session_id: str, chain: EventChain) -> dict[str, Any]:
    return {"session_id": session_id, "exported_at": int(time.time()),
            "chain": chain.to_dict()}
