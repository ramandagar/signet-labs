"""Cost Governor — budgets, real-time metering, adaptive model routing.

Every LLM and tool call is metered (tokens, USD, wall-clock). Budget breach
triggers a declarative policy: hard stop, degrade to a cheaper model, or
escalate for human approval. A rolling Tool Performance Registry feeds
latency/failure stats for routing decisions.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .errors import Category, StructuredError

# USD per 1M tokens (input, output). Update as pricing moves.
MODEL_PRICING: dict[str, tuple[float, float]] = {
    "flagship": (3.00, 15.00),   # high-stakes, irreversible actions
    "standard": (0.80, 4.00),
    "fast": (0.15, 0.60),        # low-stakes, reversible actions
}


@dataclass
class Budget:
    max_tokens: int | None = None
    max_usd: float | None = None
    max_wall_clock_seconds: float | None = None
    degrade_threshold: float = 0.8   # fraction used -> route to cheaper model
    on_breach: str = "hard_stop"     # hard_stop | degrade | escalate


class BudgetExceeded(StructuredError):
    def __init__(self, usage: dict[str, float], budget: Budget):
        over = [k for k in ("tokens", "usd", "wall_clock_seconds")
                if (lim := getattr(budget, f"max_{k}")) is not None
                and usage[k] > lim]
        super().__init__(error_code="BUDGET_EXCEEDED", category=Category.PERMANENT,
                         message=f"budget exceeded: {over}; usage={usage}",
                         recovery={"strategy": "escalate_to_human", "max_retries": 0},
                         context={"usage": usage, "over": over})


@dataclass
class Meter:
    budget: Budget
    started_at: float = field(default_factory=time.monotonic)
    tokens: int = 0
    usd: float = 0.0
    llm_calls: int = 0
    tool_calls: int = 0
    retries: int = 0

    def meter_llm(self, model: str, input_tokens: int, output_tokens: int) -> float:
        pin, pout = MODEL_PRICING.get(model, (1.0, 5.0))
        cost = (input_tokens * pin + output_tokens * pout) / 1_000_000
        self.tokens += input_tokens + output_tokens
        self.usd += cost
        self.llm_calls += 1
        return cost

    def meter_tool(self, latency_ms: float, *, retry: bool = False) -> None:
        self.tool_calls += 1  # retries counted by the caller's retry loop

    def usage(self) -> dict[str, float]:
        return {"tokens": self.tokens, "usd": round(self.usd, 6),
                "wall_clock_seconds": round(time.monotonic() - self.started_at, 3)}

    def fraction_used(self) -> float:
        u = self.usage()
        fracs = [u[k] / getattr(self.budget, f"max_{k}")
                 for k in ("tokens", "usd", "wall_clock_seconds")
                 if getattr(self.budget, f"max_{k}")]
        return max(fracs, default=0.0)

    def check(self) -> dict[str, Any]:
        """OK / degrade / escalate / hard_stop per the declared policy."""
        u = self.usage()
        over = any(lim is not None and u[k] > lim
                   for k, lim in (("tokens", self.budget.max_tokens),
                                  ("usd", self.budget.max_usd),
                                  ("wall_clock_seconds",
                                   self.budget.max_wall_clock_seconds)))
        if over:
            action = self.budget.on_breach
            if action == "hard_stop":
                raise BudgetExceeded(u, self.budget)
            return {"status": action, "usage": u}  # degrade | escalate
        if self.fraction_used() >= self.budget.degrade_threshold:
            return {"status": "degrade", "usage": u}
        return {"status": "ok", "usage": u}


@dataclass
class ModelRouter:
    """Stakes-based routing: irreversible work earns the flagship model,
    reversible work gets the cheap one. Budget pressure pushes everything down
    a tier."""
    degrade_threshold: float = 0.8

    def route(self, stakes: str, budget_used_fraction: float = 0.0) -> str:
        model = {"high": "flagship", "medium": "standard",
                 "low": "fast"}.get(stakes, "standard")
        if budget_used_fraction >= self.degrade_threshold:
            model = {"flagship": "standard", "standard": "fast", "fast": "fast"}[model]
        return model


def percentile(values: list[float], p: float) -> float:
    """Nearest-rank percentile. O(n log n), fine at registry scale."""
    if not values:
        return 0.0
    s = sorted(values)
    return s[min(int(p / 100 * (len(s) - 1) + 0.5), len(s) - 1)]


@dataclass
class ToolPerformanceRegistry:
    """Rolling latency percentiles + failure rate per tool, backed by the
    StateStore's tool_stats table."""
    store: Any  # StateStore; typed as Any to avoid import cycle

    def record(self, tool: str, latency_ms: float, ok: bool) -> None:
        self.store.record_tool_stat(tool, latency_ms, ok)

    def profile(self, tool: str) -> dict[str, float]:
        rows = self.store.tool_stats(tool)
        lats = [r[0] for r in rows]
        fails = sum(1 for r in rows if not r[1])
        return {"calls": len(rows), "p50_ms": percentile(lats, 50),
                "p99_ms": percentile(lats, 99),
                "failure_rate": round(fails / len(rows), 4) if rows else 0.0}
