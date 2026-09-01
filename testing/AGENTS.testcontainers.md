---
id: testcontainers
title: Integration Tests with Testcontainers
summary: Containerized local dependencies for integration tests.
category: testing
requires: [integration-tests]
---

# Integration Tests with Testcontainers

Use Testcontainers by default for containerizable external services such as databases, queues,
caches, object storage, and search. Reuse expensive containers at an appropriate suite scope, but
reset state between tests. Wait for readiness programmatically, configure connections automatically,
and shut resources down cleanly.

Prefer official emulators or lightweight local implementations only when Testcontainers is
unsuitable.
