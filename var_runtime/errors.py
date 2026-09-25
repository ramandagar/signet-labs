"""SERF — Structured Error Recovery Framework.

Turns raw tool/LLM failures into machine-readable errors: category, recovery
strategy, context. Agents self-correct programmatically instead of parsing
error strings.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Category(str, Enum):
    TRANSIENT = "TRANSIENT"            # retry with backoff
    PERMANENT = "PERMANENT"            # escalate or abort
    AUTHENTICATION = "AUTHENTICATION"  # refresh identity / request approval
    RATE_LIMIT = "RATE_LIMIT"          # wait and retry
    VALIDATION = "VALIDATION"          # correct input and retry
    DEPENDENCY = "DEPENDENCY"          # fallback or retry upstream


# Declarative taxonomy: signature -> category. First match wins; extend by
# appending. Signatures match HTTP status ints, exception class names, or
# lowercase substrings of the stringified error.
TAXONOMY: list[tuple[Any, Category]] = [
    (401, Category.AUTHENTICATION),
    (403, Category.AUTHENTICATION),
    (402, Category.AUTHENTICATION),
    (429, Category.RATE_LIMIT),
    (408, Category.TRANSIENT),
    (500, Category.TRANSIENT),
    (502, Category.DEPENDENCY),
    (503, Category.DEPENDENCY),
    (504, Category.TRANSIENT),
    ("timeout", Category.TRANSIENT),
    ("timed out", Category.TRANSIENT),
    ("connection reset", Category.TRANSIENT),
    ("connection refused", Category.DEPENDENCY),
    ("temporarily unavailable", Category.TRANSIENT),
    ("rate limit", Category.RATE_LIMIT),
    ("quota", Category.RATE_LIMIT),
    ("unauthorized", Category.AUTHENTICATION),
    ("forbidden", Category.AUTHENTICATION),
    ("permission denied", Category.AUTHENTICATION),
    ("invalid api key", Category.AUTHENTICATION),
    ("expired", Category.AUTHENTICATION),
    ("not found", Category.PERMANENT),
    ("unsupported", Category.PERMANENT),
    ("panic", Category.PERMANENT),
    ("invalid input", Category.VALIDATION),
    ("schema", Category.VALIDATION),
    ("validation", Category.VALIDATION),
    ("missing required", Category.VALIDATION),
]

RECOVERY: dict[Category, dict[str, Any]] = {
    Category.TRANSIENT: {"strategy": "retry_with_backoff", "max_retries": 3,
                         "backoff_seconds": [1, 5, 15]},
    Category.PERMANENT: {"strategy": "escalate_to_human", "max_retries": 0},
    Category.AUTHENTICATION: {"strategy": "refresh_identity_or_request_approval",
                              "max_retries": 1},
    Category.RATE_LIMIT: {"strategy": "wait_and_retry", "max_retries": 5,
                          "backoff_seconds": [30, 60, 120, 300, 600]},
    Category.VALIDATION: {"strategy": "correct_input_and_retry", "max_retries": 2},
    Category.DEPENDENCY: {"strategy": "fallback_or_retry", "max_retries": 3,
                          "backoff_seconds": [5, 15, 60]},
}


def classify(raw: Any, *, status: int | None = None,
             tool_name: str | None = None) -> "StructuredError":
    """Map a raw error (exception, string, or dict with 'status') to SERF."""
    if isinstance(raw, dict):
        status = status or raw.get("status")
        text = str(raw.get("error", raw))
    elif isinstance(raw, BaseException):
        text = f"{type(raw).__name__}: {raw}"
    else:
        text = str(raw)
    status = status if status is not None else _extract_status(text)

    category = Category.TRANSIENT  # conservative default: retrying is safe
    if status is not None:
        for sig, cat in TAXONOMY:
            if sig == status:
                category = cat
                break
    else:
        low = text.lower()
        for sig, cat in TAXONOMY:
            if isinstance(sig, str) and sig in low:
                category = cat
                break

    code = f"{category.value}" + (f"_HTTP_{status}" if status else "")
    return StructuredError(
        error_code=code, category=category, message=text[:500],
        tool_name=tool_name, recovery=dict(RECOVERY[category]),
    )


def _extract_status(text: str) -> int | None:
    for token in text.replace("-", " ").split():
        if token.isdigit() and token in {"401", "402", "403", "408", "429",
                                         "500", "502", "503", "504"}:
            return int(token)
    return None


@dataclass
class StructuredError(Exception):
    error_code: str
    category: Category
    message: str
    tool_name: str | None = None
    recovery: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    retry_after_seconds: float | None = None

    def __str__(self) -> str:  # keeps `raise StructuredError(...)` readable
        return f"{self.error_code}: {self.message}"

    def to_dict(self) -> dict[str, Any]:
        d = {"error_code": self.error_code, "category": self.category.value,
             "message": self.message, "recovery": self.recovery,
             "context": self.context}
        if self.tool_name:
            d["tool_name"] = self.tool_name
        if self.retry_after_seconds is not None:
            d["retry_after_seconds"] = self.retry_after_seconds
        return d

    @property
    def should_retry(self) -> bool:
        return self.recovery.get("max_retries", 0) > 0

    def next_backoff(self, attempt: int) -> float:
        offs = self.recovery.get("backoff_seconds", [])
        return float(offs[min(attempt, len(offs) - 1)]) if offs else 1.0


def backoff_sleep(err: StructuredError, attempt: int) -> None:
    """Actually sleep per the recovery plan. Tests monkeypatch time.sleep."""
    time.sleep(err.next_backoff(attempt))
