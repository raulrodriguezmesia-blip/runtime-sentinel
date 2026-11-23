# Runtime Sentinel — How Kiro Was Used

## Kiro Integration Report (for Devpost submission)

### Kiro IDE, CLI, Web, Crew

**Primary tool: Kiro IDE** with specification-driven workflow.

- **Specs**: `.kiro/specs/requirements.md` defines the core principle, design goals, non-goals, functional requirements, and acceptance criteria *before* writing code. Kiro reads these specs and generates implementation scaffolding.
- **Steering**: `.kiro/steering/architecture.md` steers Kiro's implementation decisions (language: Python for MVP, deterministic hot path, no I/O in evaluation, SQLite-backed ledger).
- **Hooks**: `.kiro/hooks/pre_build.yaml` and `post_build.yaml` automate PBT execution, chain verification, and benchmark regeneration on every build.
- **Crew**: `.kiro/crew/sentinel-auditor.yml` defines the Sentinel Auditor agent that generates policies, validates them, explains decisions, and verifies chain integrity.
- **MCP**: `mcp/server.py` exposes `sentinel_audit` and `sentinel_verify` as tools for external agents.
- **PBT**: `tests/test_chain.py` enforces 4 invariants via property-based testing.

### Agentes personalizados

**Sentinel Auditor** (`.kiro/crew/sentinel-auditor.yml`):
- Role: security auditor for Runtime Sentinel
- Tasks: generate policy rules from specs, validate that every decision has evidence, explain decisions in plain language, verify chain integrity
- Tools: `sentinel_audit`, `sentinel_verify`, `policy_generate`, `explain_decision`

### Ganchos de agente (Agent Hooks)

| Hook | Trigger | Purpose |
|------|---------|---------|
| `pre_build` | Before build | Run PBT + `verify_chain()` against fixture ledger |
| `post_build` | After build | Regenerate benchmark baselines; fail if p99 > 100,000 ns |

### Desarrollo basado en especificaciones (Spec-Driven Development)

1. **Requirements first**: `.kiro/specs/requirements.md` defines core principle, design goals, non-goals, functional requirements, and acceptance criteria.
2. **Architecture steering**: `.kiro/steering/architecture.md` drives implementation decisions (layers, language, Kiro usage).
3. **Implementation**: Code is generated from specs, not the other way around.
4. **Validation**: PBT tests enforce the invariants defined in specs.

This approach improved development by ensuring every line of code traces back to a requirement. Without spec-driven development, the policy engine would have been ad-hoc and harder to audit.

### Documentos de dirección (Steering)

The steering document (`architecture.md`) defines:
- System shape (Policy Engine, Evidence Ledger, Chain Verification, Forensic Audit, Policy Lifecycle, Kiro Layer)
- Layer responsibilities
- Kiro usage expectations
- Language decision (Python for MVP, Rust for v2)

Steering prevented scope creep by clearly defining what Runtime Sentinel is NOT (not ML, not automatic policy decision, not replacement for authorization systems).

### MCP (Model Context Protocol)

`mcp/server.py` exposes two tools for external agents:
- `sentinel_audit(decision_id, db_path)` — audit a decision by ID
- `sentinel_verify(db_path)` — verify the entire evidence chain

These tools allow Kiro agents or other AI systems to query Runtime Sentinel's evidence without direct database access.

### Pruebas basadas en propiedades (PBT)

10 property-based tests enforce:
1. **Determinism**: same input always yields same decision
2. **Default deny**: unmatched actions are denied
3. **Allow case**: safety braking is allowed with correct policy
4. **Deny case**: data deletion is denied with correct policy
5. **Evidence creation**: every decision creates exactly one evidence record
6. **Chain verification**: unmodified chain returns VERIFIED
7. **Tamper detection**: any modification breaks chain verification
8. **Policy decay active**: active policy authorizes before expiry
9. **Policy decay expired**: expired policy falls back to DENY
10. **Historical preservation**: evidence remains verifiable after policy expiry

PBT caught edge cases that unit tests would miss: policy priority conflicts, hash chain corruption scenarios, and temporal boundary conditions.

### Kiro Powers

- **Specs → Implementation**: requirements.md drove the policy engine and ledger design.
- **Steering → Architecture**: architecture.md prevented scope creep (no DSL, no microservices, no cloud).
- **Hooks → Automation**: pre_build runs PBT + chain verification; post_build regenerates benchmarks.
- **Crew → Agent roles**: Sentinel Auditor agent generates, validates, explains, and verifies.
- **MCP → Integration**: external agents can audit and verify via MCP tools.
- **PBT → Invariants**: 10 property-based tests enforce core invariants.

### Summary

Runtime Sentinel uses Kiro as the **primary development platform**, not as an afterthought. Spec-driven development ensured every line of code traces back to a requirement. Steering prevented scope creep. Hooks automated validation. Crew provided agent capabilities. MCP enabled integration. PBT caught edge cases.

This is not a project that "mentions Kiro" — it is a project **built with Kiro** from specification to delivery.