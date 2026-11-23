# Runtime Sentinel — Implementation Roadmap (Execution Contract)

## Core Principle

Every runtime decision must produce a verifiable chain of evidence.

## Project: Runtime Sentinel
- Category: Kiroween 2026 — Resurrection
- Thesis: "Resurrecting RTOS-grade trust for the age of AI agents."
- Deadline: 4 Dec 2026, 2:00 p.m. PT
- Submission URL: kiroween.devpost.com

## Phases (immutable order)

### PHASE 1 — Policy Engine

**Objective:** Create a deterministic Policy Engine.

**Requirements:**
- Input: `actor`, `action`, `resource`, `context`
- Output: `ALLOW` or `DENY`
- Default behavior = DENY
- No randomness, no external dependencies, deterministic

**Deliverables:** `src/policy_engine/` → `models.py`, `policies.py`, `engine.py`

**Acceptance Criteria:** Given identical input, evaluation always returns identical result.

### PHASE 2 — Evidence Ledger

**Objective:** Create a tamper-evident Evidence Ledger.

**Requirements:**
- For every decision: `decision_id`, `timestamp`, `actor`, `action`, `resource`, `decision`, `policy_name`, `prev_hash`, `entry_hash`
- Hash algorithm: SHA-256
- Storage: SQLite
- Every entry references previous hash
- Genesis entry supported
- Evidence persists after application restart

**Deliverables:** `src/evidence_ledger/` → `schema.py`, `sqlite_store.py`, `hashing.py`, `ledger.py`

**Acceptance Criteria:** Every decision generates one evidence record.

### PHASE 3 — Chain Verification

**Objective:** Detect evidence tampering.

**Requirements:**
- `verify_chain()` → `VERIFIED` | `TAMPERING DETECTED` | `BROKEN CHAIN`
- Recalculate hashes, detect edited/deleted records, return failing record index
- Demo: user modifies SQLite manually, Runtime Sentinel detects corruption

**Acceptance Criteria:** Tampering is always detected.

### PHASE 4 — Forensic Audit

**Objective:** Allow humans to investigate decisions.

**Commands:** `sentinel audit <id>`, `sentinel explain <id>`

**Audit Output:** Decision, Policy, Actor, Action, Resource, Timestamp, Chain Status
**Explain Output:** Human-readable explanation

**Acceptance Criteria:** Any recorded decision can be explained.

### PHASE 5 — Governance & Kiro Integration

**Objective:** Demonstrate advanced Kiro usage.

**Requirements:**
- Populate `.kiro/specs`, `.kiro/steering`, `.kiro/hooks`
- Property-Based Testing (PBT) with 4 required properties:
  1. Every decision creates evidence
  2. Every evidence entry links to previous entry
  3. Any modification breaks chain verification
  4. Same input => same decision
- Sentinel Auditor Crew (generate policies, validate policies, explain decisions, verify chain integrity)

**Acceptance Criteria:** Kiro artifacts are visible and actively used.

### PHASE 6 — Demo & Devpost

**Objective:** Create a winning hackathon demonstration.

**Demo Script:**
1. Agent attempts: `delete_customer_record()`
2. Runtime Sentinel intercepts
3. Policy evaluation returns `DENY`
4. Evidence created
5. Chain verified
6. Database record altered manually
7. `verify_chain()` returns `TAMPERING DETECTED`
8. `audit` command explains why decision was denied

**Final Message:** "Runtime Sentinel does not ask developers to trust AI decisions. It generates verifiable evidence for every decision."

**Acceptance Criteria:** Entire flow demonstrated in under 3 minutes.

## Success Metric

Runtime Sentinel does not ask developers to trust AI decisions.
It generates verifiable evidence for every decision.

## Rules (immutable)

- Prioritize simplicity over complexity.
- Avoid unnecessary abstractions.
- No LLM in the runtime core.
- No DSL implementation.
- No microservice architecture.
- No cloud dependency.
- SQLite only.
- Python only.
- Design for local execution.
- Favor readability and auditability.
- Every feature must contribute directly to: Determinism, Evidence, Verification, Explainability.

## Phase Gate Rule

Never continue to the next phase until the current phase objectives are met.
For each phase: explain architecture decisions, generate production-quality code, generate tests, generate acceptance criteria, identify risks.