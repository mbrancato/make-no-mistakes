---
id: process
title: Test-Driven Development
summary: A language- and framework-agnostic process for test-driven software development.
category: process
---

# Priorities

Prioritize correctness, maintainability, readability, testability, reuse, and simplicity. Prefer
clear, well-structured implementations over clever or overly compact ones. Fit changes into the
existing architecture rather than adding isolated patterns or one-off implementations.

# Test-First Development

Use test-driven development for new behavior and behavioral changes:

1. **Red:** Write or update a test that describes the desired externally meaningful behavior.
2. **Green:** Implement the smallest change that makes the test pass.
3. **Refactor:** Improve the implementation only while the behavior remains covered by passing
   tests.

For a defect, first add a test that reproduces it. It must fail before the fix and pass afterward.
Do not weaken, remove, or bypass a test merely to make a change pass unless the expected behavior
intentionally changed.

# Incremental Changes and Refactoring

Keep changes small, coherent, and reviewable. Prefer the simplest solution that meets the behavior
and preserves existing contracts.

Refactor when the change exposes nearby duplication, unclear responsibilities, tight coupling,
difficult-to-test code, missing abstractions, or obsolete code. Keep refactoring proportional to the
requested work; avoid unrelated rewrites. Establish coverage for existing behavior before changing
its structure.

Before adding code, look for existing utilities, components, services, and abstractions that already
provide the needed behavior. Reuse or coherently extend them when that improves maintainability. Do
not create overly generic abstractions solely to remove a few similar lines.

# Definition of Done

Consider work complete only when:

- The requested behavior is implemented and appropriately covered.
- Defects have a regression test.
- Relevant tests and required repository checks pass.
- New and modified behavior targets 100% coverage where reasonably testable.
- Documentation is accurate for changed behavior, configuration, APIs, usage, or operations.
- Obsolete code, temporary debugging output, unused imports, unused configuration, and superseded
  dependencies are removed.
- No unnecessary or unrelated changes remain.

When these expectations conflict with more-specific repository guidance, follow the more-specific
guidance unless it violates an explicit requirement of the change.
