"""Schema definitions for Runtime Sentinel Evidence Ledger."""

from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class EvidenceRecord:
    """A single evidence record in the ledger."""
    decision_id: int
    timestamp_ns: int
    actor_id: str
    action_type: str
    resource_id: str
    policy_id: Optional[str]
    decision: str
    latency_ns: int
    prev_hash: str
    entry_hash: str
    context_json: Optional[str] = None

    def canonical_json(self) -> str:
        """Canonical JSON representation for hashing."""
        return json.dumps(
            {
                "decision_id": self.decision_id,
                "timestamp_ns": self.timestamp_ns,
                "actor_id": self.actor_id,
                "action_type": self.action_type,
                "resource_id": self.resource_id,
                "policy_id": self.policy_id,
                "decision": self.decision,
                "latency_ns": self.latency_ns,
                "prev_hash": self.prev_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def as_dict(self) -> dict:
        return {
            "decision_id": self.decision_id,
            "timestamp_ns": self.timestamp_ns,
            "actor_id": self.actor_id,
            "action_type": self.action_type,
            "resource_id": self.resource_id,
            "policy_id": self.policy_id,
            "decision": self.decision,
            "latency_ns": self.latency_ns,
            "prev_hash": self.prev_hash,
            "entry_hash": self.entry_hash,
            "context_json": self.context_json,
        }