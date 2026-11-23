"""SQLite storage for Runtime Sentinel Evidence Ledger."""

import sqlite3
import os
from typing import Optional, List

GENESIS_HASH = "GENESIS"


class SQLiteStore:
    """SQLite-backed evidence store."""

    def __init__(self, db_path: str = "evidence.db"):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def open(self) -> None:
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")
        self._create_table()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def _create_table(self) -> None:
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_ns INTEGER NOT NULL,
                actor_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                resource_id TEXT NOT NULL,
                policy_id TEXT,
                decision TEXT NOT NULL,
                latency_ns INTEGER NOT NULL,
                prev_hash TEXT NOT NULL,
                entry_hash TEXT NOT NULL,
                context_json TEXT
            )
        """)
        self._conn.commit()

    def insert(self, record: dict) -> int:
        cursor = self._conn.execute(
            """INSERT INTO evidence
               (timestamp_ns, actor_id, action_type, resource_id, policy_id, decision,
                latency_ns, prev_hash, entry_hash, context_json)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                record["timestamp_ns"],
                record["actor_id"],
                record["action_type"],
                record["resource_id"],
                record["policy_id"],
                record["decision"],
                record["latency_ns"],
                record["prev_hash"],
                record["entry_hash"],
                record.get("context_json"),
            ),
        )
        self._conn.commit()
        return cursor.lastrowid

    def get_by_id(self, decision_id: int) -> Optional[dict]:
        row = self._conn.execute(
            "SELECT * FROM evidence WHERE id = ?", (decision_id,)
        ).fetchone()
        return dict(row) if row else None

    def get_last_hash(self) -> str:
        row = self._conn.execute(
            "SELECT entry_hash FROM evidence ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return row["entry_hash"] if row else GENESIS_HASH

    def get_all(self) -> List[dict]:
        rows = self._conn.execute(
            "SELECT * FROM evidence ORDER BY id ASC"
        ).fetchall()
        return [dict(r) for r in rows]

    def count(self) -> int:
        row = self._conn.execute("SELECT COUNT(*) as c FROM evidence").fetchone()
        return row["c"]

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()
        return False