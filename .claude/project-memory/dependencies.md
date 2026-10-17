# dependencies - TNHacks26

- 2026-10-17 - [SUPERSEDED ~13:00 CDT: the stack is Python] Stack is Next.js + OCI TypeScript SDK (decisions.md). Nothing
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
- 2026-10-17 16:50 CDT - Runtime deps are Python, in requirements.txt, now
  pinned to the versions tested on the laptop: oci 2.188.0, fastapi 0.143.3
  (starlette 1.8.0 comes with it), uvicorn 0.54.0, python-multipart 0.0.32.
  The VM venv's installed versions are NOT recorded (an SSH read was denied
  by the session's permission mode); `pip freeze` there before relying on it.
  The redeploy (`git archive HEAD app`) does not reinstall requirements.
