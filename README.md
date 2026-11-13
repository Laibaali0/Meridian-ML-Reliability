# Meridian — ML Systems Reliability Lab

An independent, reproducible reference codebase exploring **retrieval ranking**, **inference scheduling**, **agent tool safety**, **temporal API validity**, and **model evaluation**.

The modules are designed to be inspectable and testable on an ordinary laptop. They are deliberately **small implementations and discrete simulations**, not enterprise deployments, state-of-the-art ML models, or replacements for production services. This repository was developed with AI coding assistance and should be reviewed and understood before being presented as personal technical experience.

## What is implemented

| Track | Implementations | Evidence |
| --- | --- | --- |
| Retrieval | BM25, TF-IDF, truncated SVD, reciprocal rank fusion, MMR reranking, IVF approximate search | Graded toy relevance judgments and recall/MRR/nDCG |
| Model serving | Discrete-tick continuous batching, KV-cache allocator, admission limits, token bucket, priority queues | Simulated latency, throughput proxy, SLA and memory accounting |
| Quantization | Groupwise packed INT4 weights with scales, reconstruction and output error | CPU numerical/error comparisons (not GPU acceleration) |
| Agent reliability | Typed tool contracts, explicit allowlists, write-action denial, resource budgets, trace replay | Deterministic outcomes, expected denial tests, audit records |
| Temporal reliability | Semantic release constraints, source applicability windows, support/refute evidence, abstention | Fictional API migration timeline with claim-to-source provenance |
| Evaluation | Brier/ECE, paired bootstrap, PSI/JS drift, temporal splits, as-of joins, experiment fingerprints | Deterministic synthetic evaluation and regression tests |

## Setup

Use Python 3.10+.

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m meridian.cli retrieval
python -m meridian.cli serving
python -m meridian.cli quantization
python -m meridian.cli agents
python -m meridian.cli temporal
python -m meridian.cli calibration
```

Write a JSON report for further inspection:

```bash
python -m meridian.cli calibration --seed 17 --output outputs/calibration.json
```

## Evaluation boundaries

- Synthetic examples and hand-authored relevance judgments are not real model benchmarks.
- Low-rank SVD search is not a pretrained transformer semantic encoder.
- Inference scheduling simulates ticks; it does not run vLLM, CUDA, or serving hardware.
- The packed 4-bit routine dequantizes weights on CPU. It does not establish GPU throughput.
- Agent trace replay uses deterministic tools, not a generative model.
- Temporal API compatibility is based on explicitly supplied evidence, not automatic web research.

See [Architecture](docs/architecture.md), [Evaluation Methodology](docs/evaluation_methodology.md), and [Safety](docs/security.md).

## Contribution and integrity notes

Project development was AI-assisted; commits in the imported history describe actual incremental files and changes, all made during this development session. No dates are backfilled, and no company code or sensitive data is included. The existence of code or a commit count is not proof of experience, production impact, or independent authorship.
