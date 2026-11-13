# Contributing

The project is intentionally organized as small, independently testable modules. When making changes:

1. Explain the failure mode or research question before introducing an algorithm.
2. Add deterministic unit tests for normal, edge, and invalid inputs.
3. Keep synthetic data separate from public benchmarks and never use unlicensed company or personal data.
4. Run the full suite with `python -m pytest -q` and the relevant `meridian` CLI command.
5. Make comparison reports reproducible with fixed seeds, declared baselines, and recorded hardware where appropriate.
6. Describe limitations honestly, especially when using heuristic safety checks, discrete-time simulations, or simplified probability assumptions.
7. Use specific commit messages tied to what changed, rather than submitting no-op files to inflate activity.

Some initial code was created with AI assistance; review and revise it carefully before presenting any technique as mastered or production-proven.
