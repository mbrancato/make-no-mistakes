---
id: structured-logging
title: Structured Logging
summary: Opinionated structured logging for actionable, safe diagnostics.
category: observability
render: guide
---

# Observability with Structured Logging

Emit structured logs with:

- A severity and stable event name.
- Actionable context.
- Correlation, request, job, or trace IDs when available.

Log failures at the boundary where they become actionable.

- Use consistent field names.
- Never log secrets, credentials, tokens, or sensitive personal data.
- Avoid full payloads unless they are known safe and necessary for diagnosis.
