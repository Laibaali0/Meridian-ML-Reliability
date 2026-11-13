# Architecture overview

Meridian has five independent Python packages and a thin CLI.

```text
                   meridian.cli
                        |
      +-----------------+----------------+
      |                 |                |
  retrieval         inference         agents
  - BM25            - KV memory       - registry
  - SVD/IVF         - tick scheduler  - permissions
  - MMR/fusion      - INT4 weights    - replay/audit
      |                 |                |
      +-----------------+----------------+
                        |
                     reports
                        ^
        temporal -------+-------- evaluation
       - constraints           - calibration
       - time windows          - drift/uncertainty
       - evidence              - leakage checks
```

## Design boundaries

**Retrieval:** 
Document normalization and query-time scoring are separate. SVD uses a fixed TF-IDF matrix, while IVF uses seeded K-means coarse partitions. Rank fusion is deterministic and can be evaluated independently of index internals.

**Inference:**
Request arrival, KV memory allocation, admission, scheduling policy, decode progress and latency are distinct modules. The scheduler approximates decode in discrete ticks, making queue behavior testable without claiming hardware-level fidelity.

**Agent execution:**
The runtime validates every tool by registration, permission policy, exact argument schema and call budget before invoking a handler. Logs record allowed and denied attempts without automatically performing writes.

**Temporal validity:**
Claims specify a target version and date. Evidence links are only scored when the source was already published and its date/version scope covers the target. Conflicted/insufficient outputs are preserved instead of forcing binary decisions.

**Evaluation:**
Run fingerprints and artifact hashes help identify settings and outputs. Temporal splits and point-in-time feature joins prevent certain common leakage paths. The reference code is intentionally independent of databases, external APIs, and GPUs.
