"""Evidence Ledger for Runtime Sentinel."""

import time
import json
from typing import Optional, List
from .schema import EvidenceRecord
from .hashing import compute_entry_hash
from .sqlite_store import SQLiteStore, GENESIS_HASH


class EvidenceLedger:
    """Tamper-evident evidence ledger backed by SQLite."""

    def __init__(self, db_path: str = "evidence.db"):
        self.store = SQLiteStore(db_path)
        self.store.open()

    def close(self) -> None:
        self.store.close()

    def record(self, actor_id: str, action_type: str, resource_id: str,
               policy_id: Optional[str], decision: str, latency_ns: int,
               context_json: Optional[str] = None) -> EvidenceRecord:
        """Record a new decision in the ledger."""
        timestamp_ns = int(time.time() * 1_000_000_000)
        prev_hash = self.store.get_last_hash()
        decision_id = self.store.count() + 1

        rec = EvidenceRecord(
            decision_id=decision_id,
            timestamp_ns=timestamp_ns,
            actor_id=actor_id,
            action_type=action_type,
            resource_id=resource_id,
            policy_id=policy_id,
            decision=decision,
            latency_ns=latency_ns,
            prev_hash=prev_hash,
            entry_hash="",
            context_json=context_json,
        )
        rec.entry_hash = compute_entry_hash(rec.canonical_json(), prev_hash)

        self.store.insert({
            "timestamp_ns": rec.timestamp_ns,
            "actor_id": rec.actor_id,
            "action_type": rec.action_type,
            "resource_id": rec.resource_id,
            "policy_id": rec.policy_id,
            "decision": rec.decision,
            "latency_ns": rec.latency_ns,
            "prev_hash": rec.prev_hash,
            "entry_hash": rec.entry_hash,
            "context_json": rec.context_json,
        })

        rec.decision_id = self.store.count()
        return rec

    def get_by_id(self, decision_id: int) -> Optional[dict]:
        return self.store.get_by_id(decision_id)

    def get_all(self) -> List[dict]:
        return self.store.get_all()

    def count(self) -> int:
        return self.store.count()

    def verify_chain(self) -> tuple:
        """Verify the integrity of the entire chain."""
        rows = self.store.get_all()
        if not rows:
            return True, "VERIFIED (empty chain)"

        prev_hash = GENESIS_HASH
        for row in rows:
            canonical = json.dumps(
                {
                    "decision_id": row["id"],
                    "timestamp_ns": row["timestamp_ns"],
                    "actor_id": row["actor_id"],
                    "action_type": row["action_type"],
                    "resource_id": row["resource_id"],
                    "policy_id": row["policy_id"],
                    "decision": row["decision"],
                    "latency_ns": row["latency_ns"],
                    "prev_hash": row["prev_hash"],
                },
                sort_keys=True,
                separators=(",", ":"),
            )
            expected = compute_entry_hash(canonical, prev_hash)
            if row["entry_hash"] != expected:
                return False, f"TAMPERING DETECTED at entry #{row['id']}"
            if row["prev_hash"] != prev_hash:
                return False, f"BROKEN CHAIN at entry #{row['id']}"
            prev_hash = row["entry_hash"]

        return True, "VERIFIED"

    def explain(self, decision_id: int) -> Optional[str]:
        """Generate a human-readable explanation of a decision."""
        row = self.store.get_by_id(decision_id)
        if not row:
            return None
        return (
            f"Decision: {row['decision']}\n"
            f"Policy:   {row['policy_id']}\n"
            f"Actor:    {row['actor_id']}\n"
            f"Action:   {row['action_type']}\n"
            f"Resource: {row['resource_id']}\n"
            f"Latency:  {row['latency_ns']} ns\n"
            f"Evidence: {row['entry_hash'][:12]}...\n"
            f"Chain:    {row['prev_hash'][:8]} -> {row['entry_hash'][:8]}"
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False