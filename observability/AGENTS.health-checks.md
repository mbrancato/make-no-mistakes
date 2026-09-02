---
id: health-checks
title: Health Checks
summary: Fast, bounded liveness and readiness endpoints.
category: observability
render: guide
---

# Observability with Health Checks

When a service exposes health endpoints:

- Provide liveness checks that report whether the process should remain running.
- Provide readiness checks that report whether it can safely receive work.
- Keep checks fast, repeatable, and bounded by timeouts.
- Mark readiness unhealthy before accepting no new work during graceful shutdown.
