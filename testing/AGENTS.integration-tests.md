---
id: integration-tests
title: Integration Tests
summary: Real dependency testing with deterministic local infrastructure.
category: testing
requires: [clean-layered]
---

# Integration Tests

Use integration tests where correctness depends on component interaction or real infrastructure
behavior. Prefer local, realistic dependencies to heavily mocked integration behavior. Keep tests
isolated from machine state, production credentials, shared mutable environments, uncontrolled
networks, and execution order.

Build reusable harnesses that start dependencies, wait with bounded readiness checks, apply
migrations, seed minimal data, reset state, allocate conflict-free resources, and clean up.
