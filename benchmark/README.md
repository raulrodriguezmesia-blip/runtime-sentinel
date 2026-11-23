# Runtime Sentinel — Benchmark

Target: p99 < 100,000 ns (100 µs).

Output format:

```
p50 = XXX ns
p95 = XXX ns
p99 = XXX ns
Target: < 100,000 ns (100 us)
Result: PASS / FAIL
```

Benchmarks run in `.kiro/hooks/` post_build.
