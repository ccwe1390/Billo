# gotchas - TNHacks26

- 2026-10-17 - Synthea is NOT deterministic with default threading, even
  with -s/-cs/-r fixed. Pass `--generate.thread_pool_size=1` (verified
  byte-identical across 2 runs). Source: data.md.
- 2026-10-17 - Synthea's `master-branch-latest` jar is a moving tag; pin by
  our recorded sha256 (dependencies.md), not by re-downloading.
- 2026-10-17 - Synthea output has no contractual adjustments (0 nonzero
  ADJUSTMENTS rows); error type 3 needs adjustments we generate.
- 2026-10-17 - Java is portable, not on PATH: call it by full path.
