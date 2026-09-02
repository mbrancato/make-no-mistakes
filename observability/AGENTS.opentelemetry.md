---
id: opentelemetry
title: OpenTelemetry
summary: Distributed tracing with OpenTelemetry context propagation.
category: observability
render: guide
requires: [structured-logging]
---

# Observability with OpenTelemetry

When a service uses OpenTelemetry:

- Propagate trace context across process and service boundaries.
- Create spans for significant operations and external calls.
- Connect latency and failures to the initiating request or job.
