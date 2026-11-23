"""Models for Runtime Sentinel Policy Engine."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PolicyContext:
    """Context attributes for policy evaluation."""
    actor_id: str
    action_type: str
    resource_id: str
    extra: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "actor_id": self.actor_id,
            "action_type": self.action_type,
            "resource_id": self.resource_id,
            "extra": self.extra,
        }


@dataclass
class PolicyDecision:
    """Result of a policy evaluation."""
    decision: str  # "ALLOW" or "DENY"
    matched_policy: Optional[str]
    latency_ns: int

    @property
    def is_allow(self) -> bool:
        return self.decision == "ALLOW"

    @property
    def is_deny(self) -> bool:
        return self.decision == "DENY"

    def as_dict(self) -> dict:
        return {
            "decision": self.decision,
            "matched_policy": self.matched_policy,
            "latency_ns": self.latency_ns,
        }