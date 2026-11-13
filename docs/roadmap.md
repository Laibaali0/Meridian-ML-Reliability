# Development roadmap

Current state: self-contained algorithms, synthetic demonstrations, tests, CLI and documentation.

## Retrieval

- [ ] Evaluate IVF recall vs exhaustive search across varying probe counts
- [ ] Add a product-disjoint benchmark split and licensed public query corpus
- [ ] Evaluate real embedding encoders with a declared GPU/CPU configuration
- [ ] Add incremental index updates and online index-consistency tests

## Serving

- [ ] Replace discrete ticks with a calibrated prefill/decode cost model
- [ ] Model dynamic KV cache growth and eviction
- [ ] Implement a real GPU kernel/serving backend before claiming throughput
- [ ] Record TTFT, TPOT, p95 latency and hardware utilization

## Agents

- [ ] Add model-provider-independent trace ingestion
- [ ] Compare policy enforcement against prompt-injection attack suites
- [ ] Build reviewable tool-call traces with redacted user data
- [ ] Keep irreversible actions human-approved

## Temporal evidence

- [ ] Expand semantic version constraints and prerelease ordering
- [ ] Ingest versioned release notes from licensed sources
- [ ] Evaluate precision/recall with dated, human-labeled technical claims
- [ ] Compare against ordinary retrieval and recency-only baselines

## Evaluation

- [ ] Implement user-clustered confidence intervals
- [ ] Add historical backtest windows, negative controls, and sensitivity checks
- [ ] Publish exact training/evaluation artifacts with provenance

Only mark items completed after code and test evidence exists; synthetic demo metrics are not production results.
