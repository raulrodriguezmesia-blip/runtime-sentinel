"""Policy definitions for Runtime Sentinel."""

from dataclasses import dataclass, field
from typing import Callable, Optional


import fnmatch


@dataclass
class Policy:
    """A deterministic policy rule."""
    policy_id: str
    description: str
    match_actor: str = "*"
    match_action: str = "*"
    match_resource: str = "*"
    decision: str = "DENY"
    priority: int = 0
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    enabled: bool = True

    def matches(self, actor: str, action: str, resource: str) -> bool:
        if not self.enabled:
            return False
        if self.match_actor != "*" and not fnmatch.fnmatch(actor, self.match_actor):
            return False
        if self.match_action != "*" and not fnmatch.fnmatch(action, self.match_action):
            return False
        if self.match_resource != "*" and not fnmatch.fnmatch(resource, self.match_resource):
            return False
        return True

    def is_active(self, now_date: str) -> bool:
        if self.valid_from and now_date < self.valid_from:
            return False
        if self.valid_until and now_date > self.valid_until:
            return False
        return True

    def as_dict(self) -> dict:
        return {
            "policy_id": self.policy_id,
            "description": self.description,
            "match_actor": self.match_actor,
            "match_action": self.match_action,
            "match_resource": self.match_resource,
            "decision": self.decision,
            "priority": self.priority,
            "valid_from": self.valid_from,
            "valid_until": self.valid_until,
            "enabled": self.enabled,
        }


# Default policy set (safety-critical style)
DEFAULT_POLICIES = [
    Policy(
        policy_id="POL-SAFETY-BRAKING",
        description="Allow safety agents to apply brakes",
        match_actor="vehicle.agent",
        match_action="brake_apply",
        match_resource="brake_*",
        decision="ALLOW",
        priority=100,
    ),
    Policy(
        policy_id="POL-SAFETY-BRAKE-RELEASE",
        description="Allow safety agents to release brakes",
        match_actor="vehicle.agent",
        match_action="brake_release",
        match_resource="brake_*",
        decision="ALLOW",
        priority=100,
    ),
    Policy(
        policy_id="POL-DATA-READ",
        description="Allow telemetry agents to read ECU data",
        match_actor="telemetry.agent",
        match_action="read",
        match_resource="ecu_*",
        decision="ALLOW",
        priority=50,
    ),
    Policy(
        policy_id="POL-DATA-WRITE",
        description="Deny telemetry agents from writing ECU data",
        match_actor="telemetry.agent",
        match_action="write",
        match_resource="ecu_*",
        decision="DENY",
        priority=50,
    ),
    Policy(
        policy_id="POL-DATA-DELETION-FORBIDDEN",
        description="Forbid deletion of customer records",
        match_actor="*",
        match_action="delete_customer_record",
        match_resource="customer_data",
        decision="DENY",
        priority=200,
    ),
    Policy(
        policy_id="POL-POWER-SET",
        description="Allow powertrain agents to set torque",
        match_actor="powertrain.agent",
        match_action="set",
        match_resource="powertrain_*",
        decision="ALLOW",
        priority=80,
    ),
    Policy(
        policy_id="POL-TEMP-SAFETY-OVERRIDE",
        description="Temporary safety override (expires 2026-12-15)",
        match_actor="vehicle.agent",
        match_action="emergency_stop",
        match_resource="brake_*",
        decision="ALLOW",
        priority=150,
        valid_from="2026-11-23",
        valid_until="2026-12-15",
    ),
    Policy(
        policy_id="POL-DEFAULT-DENY",
        description="Default deny for unmatched actions",
        match_actor="*",
        match_action="*",
        match_resource="*",
        decision="DENY",
        priority=0,
    ),
]