"""CLI for Runtime Sentinel."""

import argparse
import json
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from policy_engine.engine import PolicyEngine
from policy_engine.policies import DEFAULT_POLICIES
from evidence_ledger.ledger import EvidenceLedger


def cmd_evaluate(args):
    """Evaluate a policy decision and record evidence."""
    engine = PolicyEngine(policies=DEFAULT_POLICIES, now_date=args.now_date)
    ledger = EvidenceLedger(args.db)
    try:
        decision = engine.evaluate(args.actor, args.action, args.resource)
        rec = ledger.record(
            actor_id=args.actor,
            action_type=args.action,
            resource_id=args.resource,
            policy_id=decision.matched_policy,
            decision=decision.decision,
            latency_ns=decision.latency_ns,
        )
        print(f"Decision: {decision.decision}")
        print(f"Policy:   {decision.matched_policy}")
        print(f"Latency:  {decision.latency_ns} ns")
        print(f"Evidence: #{rec.decision_id} ({rec.entry_hash[:12]}...)")
        if args.json:
            print(json.dumps(rec.as_dict(), indent=2))
    finally:
        ledger.close()


def cmd_audit(args):
    """Audit a decision by ID."""
    ledger = EvidenceLedger(args.db)
    try:
        row = ledger.get_by_id(args.id)
        if not row:
            print(f"Decision #{args.id} not found.")
            sys.exit(1)
        verified, msg = ledger.verify_chain()
        print(f"Decision:  {row['decision']}")
        print(f"Policy:    {row['policy_id']}")
        print(f"Actor:    {row['actor_id']}")
        print(f"Action:   {row['action_type']}")
        print(f"Resource: {row['resource_id']}")
        print(f"Latency:  {row['latency_ns']} ns")
        print(f"Evidence: {row['entry_hash']}")
        print(f"Chain:    {msg}")
    finally:
        ledger.close()


def cmd_explain(args):
    """Explain a decision in human-readable form."""
    ledger = EvidenceLedger(args.db)
    try:
        explanation = ledger.explain(args.id)
        if explanation is None:
            print(f"Decision #{args.id} not found.")
            sys.exit(1)
        print(explanation)
        verified, msg = ledger.verify_chain()
        print(f"Chain Status: {msg}")
    finally:
        ledger.close()


def cmd_verify(args):
    """Verify the integrity of the entire chain."""
    ledger = EvidenceLedger(args.db)
    try:
        verified, msg = ledger.verify_chain()
        print(f"Chain Status: {msg}")
        if not verified:
            sys.exit(1)
    finally:
        ledger.close()


def main():
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description="Runtime Sentinel — verifiable evidence for AI decisions.",
    )
    parser.add_argument("--db", default="evidence.db", help="Path to SQLite DB")
    sub = parser.add_subparsers(dest="command", required=True)

    p_eval = sub.add_parser("evaluate", help="Evaluate a policy decision")
    p_eval.add_argument("--actor", required=True)
    p_eval.add_argument("--action", required=True)
    p_eval.add_argument("--resource", required=True)
    p_eval.add_argument("--now-date", default=None)
    p_eval.add_argument("--json", action="store_true")
    p_eval.set_defaults(func=cmd_evaluate)

    p_audit = sub.add_parser("audit", help="Audit a decision by ID")
    p_audit.add_argument("id", type=int)
    p_audit.set_defaults(func=cmd_audit)

    p_explain = sub.add_parser("explain", help="Explain a decision")
    p_explain.add_argument("id", type=int)
    p_explain.set_defaults(func=cmd_explain)

    p_verify = sub.add_parser("verify", help="Verify the entire chain")
    p_verify.set_defaults(func=cmd_verify)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()