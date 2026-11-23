# Runtime Sentinel — Requirements Specification

## Core Principle

**Every runtime decision must produce a verifiable chain of evidence.**

## Design Goals

1. **Deterministic decisions** — the same input always yields the same `ALLOW` / `DENY`.
2. **Verifiable evidence** — every decision is recorded in a tamper-evident, hash-linked ledger.
3. **Explainable outcomes** — any decision can be reconstructed and explained after the fact.
4. **Tamper detection** — any modification or deletion of evidence breaks chain verification.
5. **Developer-friendly governance** — a small, composable core that developers can extend.

## Primary User Story

> As a developer building AI agents,
> I want every runtime decision to be governed, recorded, and later explained,
> so that I can prove what happened and why.

## Functional Requirements

### Runtime Action Interception & Policy Evaluation

- Intercept AI agent actions prior to execution (e.g. `delete_customer_record`, `brake_apply`).
- Evaluate deterministic `ALLOW` / `DENY` policies against `actor`, `action`, `resource`, and context attributes.
- Policies are expressed declaratively and evaluated deterministically.

### Verifiable Chain of Evidence

- Persist every decision in SQLite linked via cryptographic hashes (`prev_hash -> entry_hash`) so any tampering or deletion breaks chain verification.
- Provide a chain verification routine (`verify_chain`) that returns `VERIFIED` or a precise tamper location.

### Forensic Decision Inspection

- Provide an audit command (`sentinel audit <id>`) capable of:
  - Retrieving a decision by ID.
  - Explaining the matching policy.
  - Displaying chain verification status.
  - Identifying evidence tampering.

### Explainability

- Provide a human-readable explanation (`sentinel explain <id>`) that answers "why was this allowed or denied?" with actor, action, resource, policy, decision, and chain status.

### Temporal Policy Lifecycle

- Policies have a validity window (activation + expiry).
- When a policy expires, new decisions under it are governed by a fallback (`DENY` or a successor policy), while historical evidence remains verifiable.

### Kiro Integration

- Specs, steering, hooks, Crew agent (Sentinel Auditor), MCP integrations, and property-based testing are first-class parts of the build.

## Non-Goals

- Runtime Sentinel is **not** a machine learning system.
- Runtime Sentinel does **not** decide policies automatically.
- Runtime Sentinel does **not** replace existing authorization systems.
- Runtime Sentinel focuses on **evidence generation, verification, and explanation**.

## Acceptance Criteria (MVP)

- `verify_chain()` returns `VERIFIED` on an unmodified ledger.
- `verify_chain()` returns a tamper location when a record is altered.
- `sentinel audit <id>` returns decision + policy + chain status.
- A policy that has expired no longer authorizes new actions but preserves historical evidence.
- Property-based tests cover the invariants above.