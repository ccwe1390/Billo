# dependencies - TNHacks26

- 2026-10-17 - Stack is Next.js + OCI TypeScript SDK (decisions.md). Nothing
  installed or pinned yet.
- 2026-10-17 - `npm view` confirms OCI TypeScript SDK packages exist for all
  three planned services, each at version 2.143.0 on that date:
  `oci-generativeaiinference` (Generative AI), `oci-aidocument` (Document
  Understanding), `oci-ailanguage` (Language); umbrella `oci-sdk` 2.143.0.
  Prefer the per-service packages over the umbrella (smaller install) -
  inferred, verify when installing.
