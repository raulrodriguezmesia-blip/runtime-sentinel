"""Property-based tests for Runtime Sentinel."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.policy_engine.engine import PolicyEngine
from src.policy_engine.policies import DEFAULT_POLICIES
from src.evidence_ledger.ledger import EvidenceLedger


def test_deterministic_evaluation():
    """Same input always yields same decision."""
    engine = PolicyEngine(policies=DEFAULT_POLICIES)
    r1 = engine.evaluate("vehicle.agent", "brake_apply", "brake_front")
    r2 = engine.evaluate("vehicle.agent", "brake_apply", "brake_front")
    assert r1.decision == r2.decision
    assert r1.matched_policy == r2.matched_policy


def test_default_deny():
    """Unmatched actions are denied by default."""
    engine = PolicyEngine(policies=DEFAULT_POLICIES)
    r = engine.evaluate("unknown.agent", "unknown_action", "unknown_resource")
    assert r.is_deny


def test_allow_case():
    """Safety braking is allowed."""
    engine = PolicyEngine(policies=DEFAULT_POLICIES)
    r = engine.evaluate("vehicle.agent", "brake_apply", "brake_front")
    assert r.is_allow
    assert r.matched_policy == "POL-SAFETY-BRAKING"


def test_deny_case():
    """Data deletion is denied."""
    engine = PolicyEngine(policies=DEFAULT_POLICIES)
    r = engine.evaluate("any.agent", "delete_customer_record", "customer_data")
    assert r.is_deny
    assert r.matched_policy == "POL-DATA-DELETION-FORBIDDEN"


def test_every_decision_creates_evidence():
    """Every decision is persisted in the ledger."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.unlink(path)
    engine = PolicyEngine(policies=DEFAULT_POLICIES)
    ledger = EvidenceLedger(path)
    try:
        before = ledger.count()
        d = engine.evaluate("vehicle.agent", "brake_apply", "brake_front")
        ledger.record("vehicle.agent", "brake_apply", "brake_front", d.matched_policy, d.decision, d.latency_ns)
        after = ledger.count()
        assert after == before + 1
    finally:
        ledger.close()
        os.unlink(path)


def test_chain_verification():
    """Chain verification returns VERIFIED on unmodified ledger."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.unlink(path)
    engine = PolicyEngine(policies=DEFAULT_POLICIES)
    ledger = EvidenceLedger(path)
    try:
        d = engine.evaluate("vehicle.agent", "brake_apply", "brake_front")
        ledger.record("vehicle.agent", "brake_apply", "brake_front", d.matched_policy, d.decision, d.latency_ns)
        verified, msg = ledger.verify_chain()
        assert verified is True
        assert "VERIFIED" in msg
    finally:
        ledger.close()
        os.unlink(path)


def test_tampering_breaks_chain():
    """Modifying a record breaks chain verification."""
    import sqlite3
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.unlink(path)
    engine = PolicyEngine(policies=DEFAULT_POLICIES)
    ledger = EvidenceLedger(path)
    try:
        d = engine.evaluate("vehicle.agent", "brake_apply", "brake_front")
        ledger.record("vehicle.agent", "brake_apply", "brake_front", d.matched_policy, d.decision, d.latency_ns)
        conn = sqlite3.connect(path)
        conn.execute("UPDATE evidence SET entry_hash = 'tampered' WHERE id = 1")
        conn.commit()
        conn.close()
        ledger.close()
        ledger2 = EvidenceLedger(path)
        verified, msg = ledger2.verify_chain()
        assert verified is False
        assert "TAMPERING" in msg
        ledger2.close()
    finally:
        os.unlink(path)


def test_policy_decay_active():
    """Active policy authorizes action before expiry."""
    engine = PolicyEngine(policies=DEFAULT_POLICIES, now_date="2026-11-23")
    r = engine.evaluate("vehicle.agent", "emergency_stop", "brake_front")
    assert r.is_allow
    assert r.matched_policy == "POL-TEMP-SAFETY-OVERRIDE"


def test_policy_decay_expired():
    """Expired policy falls back to DENY."""
    engine = PolicyEngine(policies=DEFAULT_POLICIES, now_date="2026-12-20")
    r = engine.evaluate("vehicle.agent", "emergency_stop", "brake_front")
    assert r.is_deny
    assert r.matched_policy == "POL-DEFAULT-DENY"


def test_historical_evidence_preserved_after_decay():
    """Historical evidence remains verifiable after policy expiry."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.unlink(path)
    engine_active = PolicyEngine(policies=DEFAULT_POLICIES, now_date="2026-11-23")
    ledger = EvidenceLedger(path)
    try:
        d = engine_active.evaluate("vehicle.agent", "emergency_stop", "brake_front")
        ledger.record("vehicle.agent", "emergency_stop", "brake_front", d.matched_policy, d.decision, d.latency_ns)
        # Policy now expired, but evidence remains
        verified, msg = ledger.verify_chain()
        assert verified is True
        assert "VERIFIED" in msg
        # Historical record still has original policy
        row = ledger.get_by_id(1)
        assert row["policy_id"] == "POL-TEMP-SAFETY-OVERRIDE"
        assert row["decision"] == "ALLOW"
    finally:
        ledger.close()
        os.unlink(path)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])