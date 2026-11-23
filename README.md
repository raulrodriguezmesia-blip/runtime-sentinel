# Runtime Sentinel

**Resurrecting RTOS-grade trust for the age of AI agents.**

> Runtime Sentinel does not ask developers to trust AI decisions. It generates verifiable evidence for every decision.

Runtime Sentinel resurrects the trust model of safety-critical RTOS systems and applies it to AI agents. Every runtime decision is evaluated through deterministic policies, recorded in a cryptographically verifiable chain of evidence, and can later be explained, audited, and validated.

---

## Why this exists

AI agents can take actions. The question is not *whether* they can act, but *how we prove what they decided and why*. Safety-critical systems solved this decades ago through deterministic evaluation and auditable records. Runtime Sentinel brings that discipline to AI-generated actions.

## Core principle

**Every runtime decision must produce a verifiable chain of evidence.**

## What it does

1. **Intercepts** AI agent actions before execution (e.g. `delete_customer_record`, `brake_apply`).
2. **Evaluates** deterministic `ALLOW` / `DENY` policies against actor, action, resource, and context.
3. **Records** every decision in a hash-linked ledger (tamper-evident chain of evidence).
4. **Explains** any decision through a forensic audit command.
5. **Respects time** — policies expire and decay without breaking historical evidence.

## Architecture

```
Action
  |
  v
Policy Engine  -->  ALLOW / DENY
  |
  v
Evidence Ledger  (hash-linked, tamper-evident)
  |
  v
Chain Verification
  |
  +--> Forensic Audit (sentinel audit / sentinel explain)
  +--> Policy Lifecycle (expiry / decay)
```

## Differentiators

- **Tamper-evident evidence** — every decision is part of a verifiable chain; altering history breaks verification.
- **Forensic explainability** — `sentinel explain <id>` answers "why was this allowed or denied?".
- **Temporal policy decay** — policies expire; historical evidence stays verifiable.
- **Kiro-native development** — spec-driven workflow, steering, agent hooks, Crew agents, MCP, and property-based testing.

## Kiro integration (what makes this a Kiro project)

- `.kiro/specs/` — specification-driven development (requirements before code).
- `.kiro/steering/` — direction docs that steer Kiro's implementation.
- `.kiro/hooks/` — agent hooks that automate validation and verification.
- **Sentinel Auditor** — a Kiro Crew agent that generates policies, validates them, explains decisions, and checks chain integrity.
- **MCP** — connects the ledger to external audit tooling.
- **PBT** — property-based tests enforce invariants (e.g. "every decision is persisted", "tampering always breaks verification").

## Category

**Resurrection** — resurrecting the trust model of safety-critical RTOS systems for the age of AI agents.

## Status

Pre-alpha. Specification phase (Bloque 1 of 12 days, target submission 4 Dec 2026).

## License

MIT — see [LICENSE](LICENSE).