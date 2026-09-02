---
id: integration-tests
title: Integration Tests
summary: Real dependency testing with deterministic local infrastructure.
category: testing
render: body
requires: [clean-layered]
---

# Integration Tests

Use integration tests where correctness depends on component interaction or real infrastructure
behavior. When local integration testing is selected, prefer realistic containerized dependencies to
heavily mocked behavior.

- Isolate tests from machine state, production credentials, shared mutable environments,
  uncontrolled networks, and execution order.

Build reusable harnesses that:

- Start dependencies and wait with bounded readiness checks.
- Apply migrations and seed minimal data.
- Reset state and allocate conflict-free resources.
- Clean up reliably.
