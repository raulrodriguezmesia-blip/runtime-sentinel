# Runtime Sentinel — Tests

Property-based tests (PBT) enforce invariants:

1. Every decision is persisted.
2. Tampering breaks chain verification.
3. Expired policies do not authorize new actions.
4. Historical evidence remains verifiable after expiry.

Framework: hypothesis (Python) or equivalent.
Directory layout:
- tests/test_chain.py
- tests/test_policy_decay.py
- tests/test_pbt_invariants.py
