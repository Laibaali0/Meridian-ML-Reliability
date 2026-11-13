# Reproducible evaluation protocol

## Retrieval

Compare BM25, truncated SVD and fused rankings on the same held-out, labeled queries. Report recall@k, reciprocal rank and nDCG, including each query rather than only means. Use a larger external public dataset before claiming an improvement over a production baseline.

## Inference and memory

Fix the workload seed, arrival times, prompt lengths, output lengths and cache budget before comparing FIFO, priority and shortest-output scheduling. Report latency distribution and percentage violating SLOs. The tick model does **not** measure actual accelerator utilization or tokens/second.

## Quantization

Use the same FP32 weight matrix and input tensor when computing storage, mean absolute weight error and output L2 error. Include quantization scale metadata in memory estimates. For real models, add held-out task quality and hardware-specific throughput.

## Agent reliability

Evaluate read-only deterministic trace fixtures, recording whether each failure was expected. Distinguish successful model tasks from successful tool permission checks; the current setup has no model and tests only the latter.

## Temporal validity

Require explicit target version/date, named source, publication timestamp and validity window. Score source support/refutation only when both temporal and release constraints hold. Track abstentions and conflicting evidence. These examples are not independent evidence that an API was really changed.

## Statistical and data quality checks

Use bootstrapping at the independent unit (query, user or session). Current demos use i.i.d. rows and are not a substitute for grouped resampling when user interactions correlate. Run calibration, drift, per-group errors, chronological holdouts, point-in-time feature joins, and manifest fingerprints before reporting measured results.

## Evidence levels

1. **Unit-test pass:** implementation behaves as specified on artificial fixtures.
2. **Synthetic experiment:** algorithm shows measurable behavior under simulated assumptions.
3. **Public benchmark:** quality measured on documented external data with reproducible hardware/settings.
4. **Production impact:** observed deployment with reliable attribution and permissions to disclose.

Meridian currently provides evidence at levels 1 and 2 only.
