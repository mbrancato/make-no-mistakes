---
id: test-design
title: Test Design
summary: Behavioral tests, coverage, mocks, regressions, and completion checks.
category: testing
render: body
---

# Test Design

Test meaningful behavior through stable boundaries. Aim for complete coverage of new or modified
behavior where reasonably testable; coverage never replaces useful assertions.

- Cover successful behavior, invalid input, boundaries, relevant errors, branches, and dependency
  interactions.

Use deterministic unit tests with fakes, stubs, or mocks at external boundaries, not internal
implementation details. Keep test-first workflow and completion checks in the process guide.
