---
id: structured-logging
title: Structured Logging
summary: Opinionated structured logging for actionable, safe diagnostics.
category: observability
section: observability
section_title: Observability and Operations
---

# Observability with Structured Logging

Emit structured logs with severity, a stable event name, actionable context, and correlation,
request, job, or trace IDs when available. Log failures at the boundary where they become
actionable.

Use consistent field names. Never log secrets, credentials, tokens, or sensitive personal data.
Avoid full payloads unless they are known safe and necessary for diagnosis.
