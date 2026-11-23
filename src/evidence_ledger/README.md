# Runtime Sentinel — Evidence Ledger (skeleton)

This directory will hold the hash-linked, tamper-evident ledger.

Schema (SQLite):

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Row number |
| timestamp_ns | INTEGER | Nanoseconds since epoch |
| actor_id | TEXT | e.g. "vehicle.agent" |
| action_type | TEXT | e.g. "delete_customer_record" |
| resource_id | TEXT | e.g. "customer_data" |
| policy_id | TEXT | e.g. "DATA_DELETION_FORBIDDEN" |
| decision | TEXT | "ALLOW" or "DENY" |
| latency_ns | INTEGER | Policy evaluation latency |
| prev_hash | TEXT | SHA-256 of previous entry |
| entry_hash | TEXT | SHA-256 of canonical json + prev_hash |

Verifier:

```
verify_chain()
  -> "VERIFIED" | ("BROKEN", entry_index)
```
