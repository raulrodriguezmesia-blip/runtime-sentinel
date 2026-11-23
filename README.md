# Runtime Sentinel

**Resurrecting RTOS-grade trust for the age of AI agents.**

> Runtime Sentinel does not ask developers to trust AI decisions. It generates verifiable evidence for every decision.

## Demo

- **Video:** Coming soon
- **Repository:** https://github.com/raulrodriguezmesia-blip/runtime-sentinel

---

## The Problem

AI agents can take actions — delete records, apply brakes, move money. But when something goes wrong, there is no reliable way to prove what was decided, by whom, under which policy, and when. Logs can be edited. Dashboards can lie. Traditional audit trails are not tamper-evident.

Safety-critical systems solved this decades ago. AI agents have not.

## Why It Matters

- **Developers** need to know that an agent's decision can be reproduced and verified.
- **Auditors** need a chain of evidence that cannot be silently modified.
- **Organizations** need to explain why an action was allowed or denied — to regulators, customers, or themselves.

Without verifiable evidence, trust in AI agents is assumed, not proven.

## The Solution

Runtime Sentinel intercepts agent actions before execution, evaluates them through deterministic policies (ALLOW / DENY), and records every decision in a hash-linked, tamper-evident ledger. Any decision can later be audited, explained, and chain-verified. Policies can expire and decay over time without breaking historical evidence.

No blockchain. No LLM in the runtime core. No cloud dependency. Python and SQLite only.

## Quick Start

```bash
git clone https://github.com/raulrodriguezmesia-blip/runtime-sentinel.git
cd runtime-sentinel

pip install -r requirements.txt

python src/cli/sentinel.py --db evidence.db evaluate \
  --actor any.agent \
  --action delete_customer_record \
  --resource customer_data
```

## Quick Example

```bash
sentinel evaluate --actor vehicle.agent --action brake_apply --resource brake_front
```

```
Decision: ALLOW
Policy:   POL-SAFETY-BRAKING
Latency:  511800 ns
Evidence: #1 (a4b4def440e1...)
```

```bash
sentinel evaluate --actor any.agent --action delete_customer_record --resource customer_data
```

```
Decision: DENY
Policy:   POL-DATA-DELETION-FORBIDDEN
Latency:  189900 ns
Evidence: #2 (5337cb83a87a...)
```

```bash
sentinel audit 1
```

```
Decision:  ALLOW
Policy:    POL-SAFETY-BRAKING
Actor:    vehicle.agent
Action:   brake_apply
Resource: brake_front
Latency:  511800 ns
Evidence: a4b4def440e198165fc50663683519113e9ef7a081ea761019eb2cb441eddb8a
Chain:    VERIFIED
```

```bash
sentinel explain 2
```

```
Decision: DENY
Policy:   POL-DATA-DELETION-FORBIDDEN
Actor:    any.agent
Action:   delete_customer_record
Resource: customer_data
Latency:  189900 ns
Evidence: 5337cb83a87a...
Chain:    a4b4def4 -> 5337cb83
Chain Status: VERIFIED
```

```bash
sentinel verify
```

```
Chain Status: VERIFIED
```

If the database is tampered with:

```bash
sentinel verify
```

```
Chain Status: TAMPERING DETECTED at entry #2
```

## Core Principle

**Every runtime decision must produce a verifiable chain of evidence.**

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

## What Makes It Different

- **Decision Provenance** — every ALLOW/DENY is recorded with actor, action, resource, policy, timestamp, and hash. Nothing is lost.
- **Tamper Detection** — the ledger is hash-linked. Altering any entry breaks chain verification.
- **Forensic Audit** — `sentinel explain <id>` answers "why was this allowed or denied?" in plain terms.
- **Policy Decay** — policies can expire. When they do, decisions fall back to default DENY. Historical evidence remains verifiable.

## Kiro Integration

Runtime Sentinel was built with Kiro as a first-class development tool:

- **Specs** (`.kiro/specs/`) — requirements were defined before code, driving implementation.
- **Steering** (`.kiro/steering/`) — architecture guidance that shaped every module.
- **Hooks** (`.kiro/hooks/`) — automated validation and verification steps.
- **Crew** — a Kiro Crew agent (`Sentinel Auditor`) that generates policies, validates them, explains decisions, and checks chain integrity.
- **MCP** — connects the evidence ledger to external audit tooling.
- **Property-Based Testing** — PBT enforces invariants such as "every decision is persisted" and "tampering always breaks verification."

## Validation Results

- 10/10 property-based tests passing.
- Tamper detection verified — manual SQLite modification is detected by `sentinel verify`.
- Benchmark p99 = 33,100 ns (target: < 100,000 ns) — ~3x margin.
- Policy Decay implemented and tested (active and expired policies).
- Full CLI workflow validated: evaluate, audit, explain, verify.

## Why This Fits Resurrection

We are not resurrecting a technology. We are resurrecting the trust model of safety-critical RTOS systems — deterministic evaluation, tamper-evident records, and forensic explainability — and applying it to the age of AI agents.

## Roadmap

- **Current version:** Runtime Sentinel v1 (policy engine, evidence ledger, CLI, tamper detection, policy decay, Kiro integration).
- **Future:** See [ROADMAP_V2.md](docs/ROADMAP_V2.md) for planned enhancements.

## Status

Release Ready. All core features implemented, tested, and validated.

## License

MIT — see [LICENSE](LICENSE).
filePath">
C:\Users\Administrador\Documents\GitHub\runtime-sentinel\README.md