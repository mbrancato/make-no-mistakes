---
id: testcontainers
title: Integration Tests with Testcontainers
summary: Containerized local dependencies for integration tests.
category: testing
render: body
requires: [integration-tests]
---

# Integration Tests with Testcontainers

When local integration tests use containerizable external services such as databases, queues,
caches, object storage, or search, use Testcontainers as the default harness.

- Reuse expensive containers at an appropriate suite scope.
- Reset state between tests.
- Wait for readiness programmatically.
- Configure connections automatically.
- Shut resources down cleanly.

When an official emulator container for a cloud service is available, prefer it and run it through
Testcontainers. Use a lightweight local implementation only when an official emulator and
Testcontainers are unsuitable.
