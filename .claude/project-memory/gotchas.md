# gotchas - TNHacks26

- 2026-10-17 - Synthea is NOT deterministic with default threading, even
  with -s/-cs/-r fixed. Pass `--generate.thread_pool_size=1` (verified
  byte-identical across 2 runs). Source: data.md.
- 2026-10-17 - Synthea's `master-branch-latest` jar is a moving tag; pin by
  our recorded sha256 (dependencies.md), not by re-downloading.
- 2026-10-17 - Synthea output has no contractual adjustments (0 nonzero
  ADJUSTMENTS rows); error type 3 needs adjustments we generate.
- 2026-10-17 - Java is portable, not on PATH: call it by full path.
- 2026-10-17 - Evan's local shell is PowerShell 5.1: no `&&`, no `chmod`.
  VM commands (dnf, Node upgrade) run INSIDE the SSH session (bash on Oracle
  Linux), not locally. Windows OpenSSH refuses a private key that other users
  can read; restrict it with `icacls .\key.pem /inheritance:r` then
  `icacls .\key.pem /grant:r "$($env:USERNAME):(R)"` (the README's
  `chmod 600` is the macOS/Linux equivalent).
- 2026-10-17 - SSH key file name/location (Evan): save the starter kit's
  generated key as `C:\Users\daruw\.ssh\HackTN26.pem` - outside the repo so it
  can never be committed. Use that path in the icacls/ssh commands above.
