---
id: health-checks
title: Health Checks
summary: Fast, bounded liveness and readiness endpoints.
category: observability
section: observability
section_title: Observability and Operations
---

# Observability with Health Checks

Provide liveness checks that report whether the process should remain running and readiness checks
that report whether it can safely receive work. Keep checks fast, repeatable, and bounded by
timeouts. Mark readiness unhealthy before accepting no new work during graceful shutdown.
