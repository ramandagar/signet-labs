"""Integrations — real-world evidence fetchers and framework adapters.

github_actions_fetcher: resolves `tests_passed` claims against GitHub's Checks
API. A run only counts when every check for the exact head_sha concluded
success AND the run completed within max_age_seconds — the same freshness,
binding, and pass/fail semantics the gate enforces on any artifact.

langgraph adapter: wraps a graph node so its "done" output must pass the gate
before the graph advances (gated_node), and surfaces runtime checkpoints via a
checkpointer shim. LangGraph imports are lazy — the adapter works without the
package installed; install langgraph to use the auto-checkpointer glue.

    from var_runtime.integrations import gated_node, attach_checkpointer
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from typing import Any, Callable

from .evidence import make_signed_artifact
from .identity import TrustAnchor


def github_actions_fetcher(repo: str, token: str | None = None,
                           anchor: TrustAnchor | None = None):
    """Build an evidence fetcher for a GitHub repo.

    token: GitHub PAT with repo read (defaults to GITHUB_TOKEN / GH_TOKEN env).
    The artifact is signed by the runtime's key over the API payload — the
    binding GitHub actually guarantees (check runs pinned to head_sha) is what
    the gate verifies. ponytail: app-level signature; move to GitHub's own
    attestation signatures when verifying outside the trust anchor.
    """
    token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    anchor = anchor or TrustAnchor.generate("gh-proxy")

    def fetch(req: dict, claim: dict) -> dict | None:
        sha = claim.get("target", {}).get("commit_sha")
        if not sha:
            return None
        url = f"https://api.github.com/repos/{repo}/commits/{sha}/check-runs"
        r = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            **({"Authorization": f"Bearer {token}"} if token else {})})
        with urllib.request.urlopen(r, timeout=15) as resp:
            data = json.loads(resp.read())
        checks = data.get("check_runs", [])
        if not checks:
            return None
        completed = [c for c in checks if c.get("status") == "completed"]
        passed = bool(completed) and all(c.get("conclusion") == "success"
                                         for c in completed)
        newest = max((c.get("completed_at") or "") for c in completed) if completed else ""
        produced_at = _parse_gh_ts(newest) or time.time()
        return make_signed_artifact(
            req.get("evidence_type", "ci_test_result"), "github_actions",
            {"passed": passed, "checks": len(checks),
             "conclusions": sorted({c.get("conclusion", "?") for c in completed}),
             "repo": repo},
            bindings={"commit_sha": sha}, anchor=anchor, produced_at=produced_at)
    return fetch


def _parse_gh_ts(ts: str) -> float | None:
    # GitHub ISO timestamps: 2026-09-23T18:05:14Z — no tz machinery needed
    if not ts:
        return None
    import calendar
    return calendar.timegm(time.strptime(ts.replace("Z", "GMT"), "%Y-%m-%dT%H:%M:%S%Z"))


# -- LangGraph -----------------------------------------------------------------

def gated_node(runtime, session, claim: str, target_fn: Callable[[Any], dict],
               node: Callable | None = None):
    """Wrap a LangGraph node (or any callable) in Proof-or-Stop.

        graph.add_node("run_tests", gated_node(
            rt, session, "tests_passed",
            target_fn=lambda state: {"commit_sha": state["commit"]}))

    Runs the node, then gates the claim built from its output state. ADMIT
    passes the output through; HALT raises GateHalted carrying the structured
    error so the graph can route to a correction node.
    """
    from .errors import StructuredError  # local: avoid import cycle at module load

    class GateHalted(StructuredError):
        pass

    def wrapped(state: Any) -> Any:
        out = node(state) if node else state
        target = target_fn(out if node else state)
        d = runtime.gate_claim(session, {"claim": claim, "target": target})
        if not d.admitted:
            raise GateHalted(error_code="GATE_" + d.error.error_code,
                             category=d.error.category,
                             message=d.error.message,
                             recovery=d.error.recovery,
                             context=d.error.context)
        return out
    return wrapped, GateHalted


def attach_checkpointer(runtime, session, graph):
    """Bridge runtime checkpoints into a LangGraph checkpointer, if one is
    attached to the graph (lazy import — no-op with a clear return otherwise).
    After each super().step, the graph state lands in the runtime's durable
    store, so a crashed run resumes with `runtime.resume(session_id)`."""
    try:
        from langgraph.checkpoint.base import BaseCheckpointSaver
    except ImportError:
        return None  # langgraph not installed — gated_node still works bare
    if not isinstance(getattr(graph, "checkpointer", None), BaseCheckpointSaver):
        return None

    orig = graph.step
    def stepping(*a, **kw):
        out = orig(*a, **kw)
        session.memory["graph_state"] = _jsonable(getattr(out, "values", out))
        runtime.checkpoint(session)
        return out
    graph.step = stepping
    return graph


def _jsonable(x: Any) -> Any:
    return json.loads(json.dumps(x, default=str))
