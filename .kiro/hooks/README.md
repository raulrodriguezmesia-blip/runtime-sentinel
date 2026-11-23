# Runtime Sentinel — Kiro Hooks

This directory holds Kiro agent hooks that automate Runtime Sentinel validation.

## Expected hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `pre_build` | Before compilation | Run property-based tests (PBT) and `verify_chain()` against any fixture ledger. |
| `post_build` | After build | Regenerate benchmark baselines; fail if p99 > 100,000 ns (100 µs). |
| `pre_commit` | Git commit | Ensure `/.kiro/specs/` and `/.kiro/steering/` are up to date with implementation. |

## Example hook manifest (adapt to your Kiro version)

```yaml
# .kiro/hooks/sentinel.yaml
hooks:
  - name: verify-chain
    trigger: pre_commit
    command: python -m pytest tests/test_chain.py -q
  - name: audit-policies
    trigger: post_build
    command: python -m tests.test_policy_decay -q
```

**Note:** Hooks are declarative wiring between Kiro Crew and the Runtime Sentinel CLI. They are not part of the runtime binary; they enforce governance during development.
