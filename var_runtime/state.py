"""Durable State Store — checkpoints for crash recovery and replay.

SQLite, append-only. After every step the runtime serializes session state
(messages, tool results, memory, pending actions, identity envelope); after a
crash the session resumes from the latest checkpoint — no re-execution, no
re-payment. Any checkpoint can be reloaded for audit/replay.

Postgres/S3/Redis adapters are the same four methods against a different
driver; add when a second backend is actually needed.
"""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1

_SCHEMA = """
CREATE TABLE IF NOT EXISTS checkpoints (
    session_id TEXT NOT NULL,
    step_index INTEGER NOT NULL,
    created_at REAL NOT NULL,
    state_json TEXT NOT NULL,
    PRIMARY KEY (session_id, step_index, created_at)
);
CREATE INDEX IF NOT EXISTS idx_ck_session ON checkpoints(session_id, created_at);
CREATE TABLE IF NOT EXISTS events (
    session_id TEXT NOT NULL,
    seq INTEGER NOT NULL,
    entry_json TEXT NOT NULL,
    PRIMARY KEY (session_id, seq)
);
CREATE TABLE IF NOT EXISTS tool_stats (
    tool TEXT NOT NULL, latency_ms REAL NOT NULL, ok INTEGER NOT NULL, ts REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_stats_tool ON tool_stats(tool, ts);
"""


class StateStore:
    def __init__(self, path: str | Path = ":memory:"):
        self.path = str(path)
        self.db = sqlite3.connect(self.path)
        self.db.executescript(_SCHEMA)

    def close(self) -> None:
        self.db.commit()
        self.db.close()

    # -- checkpoints -----------------------------------------------------------

    def save_checkpoint(self, session_id: str, step_index: int,
                        state: dict[str, Any]) -> None:
        state = {"schema_version": SCHEMA_VERSION, **state}
        self.db.execute(
            "INSERT INTO checkpoints VALUES (?,?,?,?)",
            (session_id, step_index, time.time(),
             json.dumps(state, sort_keys=True, default=str)))

    def latest_checkpoint(self, session_id: str) -> tuple[int, dict[str, Any]] | None:
        row = self.db.execute(
            "SELECT step_index, state_json FROM checkpoints "
            "WHERE session_id=? ORDER BY created_at DESC, step_index DESC LIMIT 1",
            (session_id,)).fetchone()
        return (row[0], json.loads(row[1])) if row else None

    def checkpoints(self, session_id: str) -> list[dict[str, Any]]:
        return [{"step_index": r[0], "created_at": r[1], "state": json.loads(r[2])}
                for r in self.db.execute(
                    "SELECT step_index, created_at, state_json FROM checkpoints "
                    "WHERE session_id=? ORDER BY created_at, step_index",
                    (session_id,))]

    def sessions(self) -> list[str]:
        return [r[0] for r in self.db.execute(
            "SELECT DISTINCT session_id FROM checkpoints ORDER BY session_id")]

    # -- attestation chain persistence ----------------------------------------

    def append_event(self, session_id: str, entry: dict[str, Any]) -> None:
        self.db.execute("INSERT OR REPLACE INTO events VALUES (?,?,?)",
                        (session_id, entry["seq"], json.dumps(entry, default=str)))

    def load_events(self, session_id: str) -> list[dict[str, Any]]:
        return [json.loads(r[0]) for r in self.db.execute(
            "SELECT entry_json FROM events WHERE session_id=? ORDER BY seq",
            (session_id,))]

    # -- tool performance ------------------------------------------------------

    def record_tool_stat(self, tool: str, latency_ms: float, ok: bool) -> None:
        self.db.execute("INSERT INTO tool_stats VALUES (?,?,?,?)",
                        (tool, latency_ms, int(ok), time.time()))

    def tool_stats(self, tool: str, window_seconds: float = 3600) -> list[tuple[float, int]]:
        return self.db.execute(
            "SELECT latency_ms, ok FROM tool_stats WHERE tool=? AND ts>?",
            (tool, time.time() - window_seconds)).fetchall()

    def commit(self) -> None:
        self.db.commit()
