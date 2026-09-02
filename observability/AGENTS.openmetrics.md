---
id: openmetrics
title: OpenMetrics
summary: Metrics exposed through an OpenMetrics-compatible endpoint.
category: observability
render: guide
---

# Observability with OpenMetrics

When a service exposes metrics, prefer an OpenMetrics-compatible endpoint.

- Measure operation volume, latency, failures, and saturation or capacity where applicable.
- Use stable, bounded-cardinality labels.
- Never use request IDs, user IDs, or unbounded values as labels.
