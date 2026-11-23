"""Deterministic Policy Engine for Runtime Sentinel."""

import time
from typing import List, Optional
from .models import PolicyDecision, PolicyContext
from .policies import Policy


class PolicyEngine:
    """Deterministic policy engine."""

    def __init__(self, policies: Optional[List[Policy]] = None, now_date: Optional[str] = None):
        self.policies = policies or []
        self.now_date = now_date

    def evaluate(
        self,
        actor: str,
        action: str,
        resource: str,
        context: Optional[dict] = None,
    ) -> PolicyDecision:
        """Evaluate a policy. Default is DENY."""
        import time as _time
        start = _time.perf_counter_ns()

        matched: Optional[Policy] = None
        for policy in sorted(self.policies, key=lambda p: p.priority, reverse=True):
            if not policy.matches(actor, action, resource):
                continue
            if self.now_date and not policy.is_active(self.now_date):
                continue
            matched = policy
            break

        if matched is None:
            decision = "DENY"
            policy_id = None
        else:
            decision = matched.decision
            policy_id = matched.policy_id

        latency_ns = _time.perf_counter_ns() - start
        return PolicyDecision(
            decision=decision,
            matched_policy=policy_id,
            latency_ns=latency_ns,
        )

    def evaluate_context(self, ctx: PolicyContext) -> PolicyDecision:
        return self.evaluate(
            ctx.actor_id, ctx.action_type, ctx.resource_id, ctx.extra
        )