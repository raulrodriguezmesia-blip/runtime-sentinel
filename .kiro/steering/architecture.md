# Runtime Sentinel — Architecture Steering

This document steers Kiro's implementation. Keep it in sync with `specs/requirements.md`.

## System shape

```
Runtime Sentinel
|
+-- Policy Engine          (deterministic ALLOW/DENY)
+-- Evidence Ledger        (hash-linked chain, SQLite-backed)
+-- Chain Verification     (verify_chain, tamper detection)
+-- Forensic Audit         (sentinel audit / sentinel explain)
+-- Policy Lifecycle       (expiry / decay / fallback)
+-- Kiro Layer             (specs, steering, hooks, Crew, MCP, PBT)
```

## Layers

### 1. Policy Engine
- Input: `actor`, `action`, `resource`, `context`.
- Output: `decision` (`ALLOW` / `DENY`) + `matched_policy` + `latency_ns`.
- Deterministic. No I/O in the hot path.

### 2. Evidence Ledger
- One row per decision.
- Columns: `id`, `timestamp_ns`, `actor_id`, `action_type`, `resource_id`, `policy_id`, `decision`, `latency_ns`, `prev_hash`, `entry_hash`.
- `entry_hash = sha256(canonical_json(record_without_entry_hash) + prev_hash)`.
- Backed by SQLite for persistence and queryability.

### 3. Chain Verification
- Recompute each `entry_hash` from stored data and compare.
- Returns `VERIFIED` or the first broken entry.

### 4. Forensic Audit
- `sentinel audit <id>`: retrieve + explain + verify.
- `sentinel explain <id>`: human-readable rationale.

### 5. Policy Lifecycle
- Policies have `valid_from`, `valid_until`.
- Evaluation consults `is_active(now)`; expired policies deny by default.
- Historical ledger entries keep their original policy attribution.

## Kiro usage (expected)

- **Specs**: requirements.md drives what to build.
- **Steering**: this file drives how to build it.
- **Hooks**: automate `verify_chain` + PBT run on change.
- **Crew (Sentinel Auditor)**: generate/validate policies, explain decisions, verify chain.
- **MCP**: expose audit/verify as tools to external agents.
- **PBT**: invariants like "every ALLOW/DENY is persisted" and "any tamper breaks verification".

## Language decision

- Implement the core in **Python** for velocity in 12 days.
- Keep the hot path dependency-free and deterministic.
- Rust is a v2 option; Python is the MVP.