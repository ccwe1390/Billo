# dependencies - TNHacks26

- 2026-10-17 - Stack is Next.js + OCI TypeScript SDK (decisions.md). Nothing
  installed or pinned yet.
- 2026-10-17 - `npm view` confirms OCI TypeScript SDK packages exist for all
  three planned services, each at version 2.143.0 on that date:
  `oci-generativeaiinference` (Generative AI), `oci-aidocument` (Document
  Understanding), `oci-ailanguage` (Language); umbrella `oci-sdk` 2.143.0.
  Prefer the per-service packages over the umbrella (smaller install) -
  inferred, verify when installing.
- 2026-10-17 - Installed (Evan approved the downloads): Eclipse Temurin JDK
  17.0.20.1+1 ZIP from github.com/adoptium/temurin17-binaries (190,817,615
  bytes, sha256 e53a79c3...affc7cb0, matching Adoptium's published checksum),
  extracted to `C:\Users\daruw\tools\jdk-17.0.20.1+1\`. Synthea
  `synthea-with-dependencies.jar` from the `master-branch-latest` release
  (published 2026-08-18; 197,025,542 bytes; our sha256 018ad7f0...fae224ac;
  no upstream checksum published) at `C:\Users\daruw\tools\`. The release tag
  moves - keep this jar; re-downloading may give a different Synthea.
