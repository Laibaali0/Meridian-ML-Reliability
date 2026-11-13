# Tool execution and data handling safeguards

This reference code is intentionally local and makes no external requests. Agent tools are synthetic; **write permissions are off by default**.

## Trust boundaries

- Tool input must use exact declared argument names and scalar types.
- Missing/unknown tools are blocked before reaching handlers.
- A bounded budget prevents unlimited scripted tool calls.
- Side-effecting tools are separately identified and denied by default.
- Error details from underlying handlers are not exposed to the caller.
- Redaction helpers mask basic API-key-like fields and email addresses.
- Prompt-injection string checks are heuristic and **not security controls** on their own.

## Not included

There is no secret manager, sandbox isolation boundary, production auth, RBAC, cross-tenant isolation, network transport, or adversarially hardened LLM agent. Deploying any of the code would require a dedicated security review and more extensive implementation.

## No private data

Use only fabricated traces, generated numerical tensors and licensed public datasets. Do not upload employer code, user data, or credentials. The codebase contains no real endpoint tokens or production connections.
