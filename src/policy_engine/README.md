# Runtime Sentinel — Policy Engine (skeleton)

This directory will hold the deterministic policy engine.

MVP contract:

```
evaluate(actor, action, resource, context)
  -> decision: "ALLOW" | "DENY"
  -> matched_policy: str | None
  -> latency_ns: int
```

Design goals:

- Deterministic: same input always yields same decision.
- No I/O in the hot path.
- Runtime: Python for MVP; Rust v2 optional.
- All evaluation is driven from `.kiro/specs/`.
