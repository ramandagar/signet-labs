"""Verifiable Agent Runtime (VAR) — Proof-or-Stop control layer.

Sits between an agent framework and its tools. Intercepts critical actions,
demands mechanically verifiable evidence, propagates signed identity, meters
cost, checkpoints state, classifies errors, and attests every decision.
"""

from .errors import Category, StructuredError, classify
from .identity import IdentityEnvelope, TrustAnchor
from .attestation import EventChain
from .state import StateStore
from .cost import Budget, Meter, ModelRouter, ToolPerformanceRegistry
from .evidence import ProofRegistry, GateEngine, GateDecision
from .runtime import VerifiableRuntime

__version__ = "0.1.0"
__all__ = [
    "Category", "StructuredError", "classify",
    "IdentityEnvelope", "TrustAnchor",
    "EventChain", "StateStore",
    "Budget", "Meter", "ModelRouter", "ToolPerformanceRegistry",
    "ProofRegistry", "GateEngine", "GateDecision",
    "VerifiableRuntime",
]
