# Runtime Sentinel — Roadmap v2 (post-hackathon)

> **Status:** Archived. Do not work on this before the Kiroween submission (4 Dec 2026, 2:00 p.m. PT).

## Core Principle (unchanged)

Every runtime decision must produce a verifiable chain of evidence.

## Vision

Runtime Sentinel does not ask developers to trust AI decisions.
It generates verifiable evidence for every decision.

Long-term identity: **A platform of evidence and audit for AI decisions**, not a hackathon project.

---

## V2.1 — Product Hardening (post-hackathon)

Converts the MVP into a usable tool.

### 1. External policy files (YAML)

**Current:** Policies are hardcoded in `src/policy_engine/policies.py`.

**V2:**

```yaml
# policies/security.yaml
name: DATA_DELETION_FORBIDDEN
actor: "*"
action: delete_customer_record
resource: customer_data
decision: DENY
priority: 200
```

**Benefit:** No need to modify Python to create new policies. Closer to OPA/Cedar.

**Impact:** ⭐⭐⭐⭐⭐ | **Effort:** ⭐⭐

### 2. Forensic Timeline (moved up from V2.2 — high value, low effort)

```bash
sentinel timeline
```

Output:

```
2026-11-20 10:00  Policy Created    SAFETY_BRAKING (V1)
2026-11-20 10:15  ALLOW             brake_apply     (vehicle.agent)
2026-11-20 10:20  DENY              delete_customer_record (support-agent)
2026-11-20 10:30  Policy Expired    SAFETY_BRAKING (V1)
```

**Benefit:** Immediate clarity for audits. Judges and auditors understand value in seconds.

**Impact:** ⭐⭐⭐⭐⭐ | **Effort:** ⭐⭐

### 3. Exportable reports

```bash
sentinel export --format json   # report.json
sentinel export --format csv    # report.csv
sentinel export --format html   # report.html
```

**Impact:** ⭐⭐⭐⭐ | **Effort:** ⭐⭐

### 4. Ledger configuration

```yaml
ledger:
  sqlite_path: evidence.db
  hash_algorithm: sha256
```

**Impact:** ⭐⭐⭐ | **Effort:** ⭐

---

## V2.2 — Advanced Audit (post-hackathon)

### 5. Merkle Snapshots

Not blockchain. Not exotic cryptography. Simply:

```
100 decisions
↓
Merkle Snapshot
↓
Root Hash
```

**Benefit:** Verifiable evidence at scale. Better than linear hash chain for large datasets.

**Impact:** ⭐⭐⭐⭐ | **Effort:** ⭐⭐⭐

### 6. Decision Provenance Graph

Visual representation:

```
Policy
  ↓
Decision
  ↓
Evidence
  ↓
Verification
```

**Benefit:** High demo value. Shows the full chain visually.

**Impact:** ⭐⭐⭐⭐⭐ | **Effort:** ⭐⭐⭐

---

## V2.3 — Long-term vision (future)

### 7. Agent Gateway

```python
sentinel.evaluate(
    actor="agent",
    action="delete_customer_record",
    resource="customer_data"
)
```

Interface for agents, copilots, and MCP tools to call Runtime Sentinel programmatically.

**Impact:** ⭐⭐⭐⭐⭐

### 8. Runtime SDK

```bash
pip install runtime-sentinel
```

```python
from sentinel import evaluate
result = evaluate(actor, action, resource)
```

Converts Runtime Sentinel from a project to a platform.

**Impact:** ⭐⭐⭐⭐⭐

### 9. Multi-agent Evidence

```
Agent A → Agent B → Agent C → Final Decision
```

Full traceability across multiple agents in a single decision chain.

**Impact:** ⭐⭐⭐⭐⭐

---

## What NOT to do (ever)

- ❌ Blockchain
- ❌ Cryptocurrencies
- ❌ Zero-Knowledge by trend
- ❌ LLM in the decision core
- ❌ Microservices
- ❌ Kubernetes
- ❌ 10 databases

These add complexity without adding value to the core mission.

## Priorities for V2 (top 3)

1. **Forensic Timeline** — judges and auditors immediately understand what happened, when, and why.
2. **External YAML Policies** — converts MVP into a usable tool.
3. **Agent SDK** — converts Runtime Sentinel from project to platform.

## Core principle for V2

> More evidence, more traceability, better audit experience.
> Not more intelligence. Not more complexity. Just better governance.

## Identity

Runtime Sentinel is not a hackathon project.
It is a platform of evidence and audit for AI decisions.

Long-term answer to "What is Runtime Sentinel?":

> "A platform of evidence and audit for AI decisions."

---

## Status

```
Runtime Sentinel v1 = FROZEN (submitted to Kiroween 2026)
Runtime Sentinel v2 = ARCHIVED (post-hackathon roadmap)

Do not work on v2 before the submission deadline (4 Dec 2026, 2:00 p.m. PT).
```