"""Hashing utilities for Runtime Sentinel Evidence Ledger."""

import hashlib
import json


def compute_entry_hash(record_canonical: str, prev_hash: str) -> str:
    """Compute SHA-256 hash of canonical record + previous hash."""
    payload = (record_canonical + prev_hash).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def hash_string(value: str) -> str:
    """Hash a single string."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()