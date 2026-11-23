"""Latency Benchmark for Runtime Sentinel."""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.policy_engine.engine import PolicyEngine
from src.policy_engine.policies import DEFAULT_POLICIES

ITERATIONS = 1000

actors = ["vehicle.agent", "telemetry.agent", "unknown.agent"]
actions = ["brake_apply", "brake_release", "read", "write", "delete_customer_record", "unknown"]
resources = ["brake_front", "brake_rear", "ecu_engine", "customer_data", "unknown_resource"]


def main():
    engine = PolicyEngine(policies=DEFAULT_POLICIES)
    latencies = []

    for i in range(ITERATIONS):
        actor = actors[i % len(actors)]
        action = actions[(i * 3) % len(actions)]
        resource = resources[(i * 7) % len(resources)]
        result = engine.evaluate(actor, action, resource)
        latencies.append(result.latency_ns)

    latencies.sort()
    p50 = latencies[ITERATIONS // 2]
    p95 = latencies[int(ITERATIONS * 0.95)]
    p99 = latencies[int(ITERATIONS * 0.99)]
    mean = sum(latencies) / ITERATIONS
    min_v = min(latencies)
    max_v = max(latencies)

    print("=== Runtime Sentinel Latency Benchmark ===")
    print(f"Iterations:  {ITERATIONS}")
    print(f"Mean:        {mean:.2f} ns")
    print(f"Min:         {min_v} ns")
    print(f"Max:         {max_v} ns")
    print(f"p50:         {p50} ns")
    print(f"p95:         {p95} ns")
    print(f"p99:         {p99} ns")
    print()
    print("Hypothesis: policy eval < 100,000 ns (100 us)")
    print(f"p99 result:  {'PASS' if p99 < 100000 else 'FAIL'}")
    print(f"p95 result:  {'PASS' if p95 < 100000 else 'FAIL'}")
    print(f"p50 result:  {'PASS' if p50 < 100000 else 'FAIL'}")


if __name__ == "__main__":
    main()