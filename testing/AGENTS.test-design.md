---
id: test-design
title: Test Design
summary: Behavioral tests, coverage, mocks, regressions, and completion checks.
category: testing
---

# Test Design

Test meaningful behavior through stable boundaries. Cover successful behavior, invalid input,
boundaries, relevant errors, branches, and dependency interactions. New or modified behavior targets
100% coverage where reasonably testable; coverage never replaces useful assertions.

Use deterministic unit tests with fakes, stubs, or mocks at external boundaries, not internal
implementation details. Add a regression test for every defect. Before completion, run documented
formatting, linting, static analysis, tests, and coverage checks.
