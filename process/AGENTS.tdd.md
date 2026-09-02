---
id: process
title: Test-Driven Development
summary: A language- and framework-agnostic process for test-driven software development.
category: process
render: body
---

# Priorities

Prioritize the following qualities:

- Correctness, maintainability, readability, testability, reuse, and simplicity.
- Clear, well-structured implementations over clever or overly compact ones.
- Changes that fit the existing architecture rather than isolated patterns or one-off
  implementations.

# Test-Driven Development

Use test-driven development as the default pattern for new behavior and behavioral changes:

1. **Red:** Write or update a test that describes the desired externally meaningful behavior.
2. **Green:** Implement the smallest change that makes the test pass.
3. **Refactor:** Improve the implementation only while the behavior remains covered by passing
   tests.

For defects:

- Add a test that reproduces the defect before implementing the fix.
- Confirm that the regression test fails before the fix and passes afterward.
- Do not weaken, remove, or bypass a test merely to make a change pass unless the expected behavior
  intentionally changed.

# Incremental Changes and Refactoring

Keep changes small, coherent, and reviewable. Prefer the simplest solution that meets the behavior
and preserves existing contracts.

Refactor when the change exposes:

- Nearby duplication.
- Unclear responsibilities or tight coupling.
- Difficult-to-test code or missing abstractions.
- Obsolete code.

Keep refactoring proportional to the requested work and avoid unrelated rewrites. Establish coverage
for existing behavior before changing its structure.

Before adding code, look for existing utilities, components, services, and abstractions that already
provide the needed behavior. Reuse or coherently extend them when that improves maintainability. Do
not create overly generic abstractions solely to remove a few similar lines.

# Definition of Done

Consider implementation work complete only when:

- The requested behavior is implemented and appropriately covered.
- Defects have a regression test.
- Relevant tests and required repository checks pass.
- New and modified behavior has complete meaningful coverage where reasonably testable; coverage
  percentages do not replace useful assertions.
- Documentation is accurate for changed behavior, configuration, APIs, usage, or operations.
- Obsolete code, temporary debugging output, unused imports, unused configuration, and superseded
  dependencies are removed.
- No unnecessary or unrelated changes remain.

When these expectations conflict with more-specific repository guidance, follow the more-specific
guidance unless it violates an explicit requirement of the change.
