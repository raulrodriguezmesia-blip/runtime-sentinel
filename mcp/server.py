"""Minimal MCP server for Runtime Sentinel.

Exposes sentinel_audit and sentinel_verify as MCP tools.
This is a stub for demonstration purposes — it wraps the CLI logic.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evidence_ledger.ledger import EvidenceLedger


def sentinel_audit(decision_id: int, db_path: str = "evidence.db") -> dict:
    """Audit a decision by ID. Returns decision details and chain status."""
    ledger = EvidenceLedger(db_path)
    try:
        row = ledger.get_by_id(decision_id)
        if not row:
            return {"error": f"Decision #{decision_id} not found."}
        verified, msg = ledger.verify_chain()
        return {
            "decision_id": row["id"],
            "decision": row["decision"],
            "policy_id": row["policy_id"],
            "actor_id": row["actor_id"],
            "action_type": row["action_type"],
            "resource_id": row["resource_id"],
            "timestamp_ns": row["timestamp_ns"],
            "latency_ns": row["latency_ns"],
            "entry_hash": row["entry_hash"],
            "chain_status": msg,
            "chain_verified": verified,
        }
    finally:
        ledger.close()


def sentinel_verify(db_path: str = "evidence.db") -> dict:
    """Verify the integrity of the entire evidence chain."""
    ledger = EvidenceLedger(db_path)
    try:
        verified, msg = ledger.verify_chain()
        return {
            "verified": verified,
            "message": msg,
            "record_count": ledger.count(),
        }
    finally:
        ledger.close()


# MCP tool definitions (minimal, for demonstration)
TOOLS = [
    {
        "name": "sentinel_audit",
        "description": "Audit a decision by ID. Returns decision details and chain status.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "decision_id": {"type": "integer", "description": "The decision ID to audit"},
                "db_path": {"type": "string", "description": "Path to SQLite DB (default: evidence.db)"},
            },
            "required": ["decision_id"],
        },
    },
    {
        "name": "sentinel_verify",
        "description": "Verify the integrity of the entire evidence chain.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "db_path": {"type": "string", "description": "Path to SQLite DB (default: evidence.db)"},
            },
        },
    },
]


if __name__ == "__main__":
    # Demo: run audit on decision #1
    import json
    result = sentinel_audit(1)
    print(json.dumps(result, indent=2))
    result = sentinel_verify()
    print(json.dumps(result, indent=2))