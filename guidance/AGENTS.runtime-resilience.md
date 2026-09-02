---
id: runtime-resilience
title: Runtime Resilience
summary: Explicit configuration, bounded external operations, and graceful lifecycle management.
category: guidance
render: body
---

# Configuration and Runtime Resilience

Keep configuration explicit, validate it at startup where possible, and separate it from code.

- Never commit secrets.
- Never log secret values.
- Do not require production credentials for local development or tests.

For network and external-service operations:

- Use bounded timeouts.
- Retry only transient, idempotent operations.
- Bound retry attempts and use backoff.
- Surface final failures with useful context rather than retrying indefinitely.

Applications that manage long-lived work must handle termination signals gracefully:

- Stop accepting new work.
- Cancel or drain in-flight work within a bounded deadline.
- Release resources.
- Exit with an accurate status.
