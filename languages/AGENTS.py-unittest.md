---
id: py-unittest
title: Python unittest Named Test Scenarios
summary: Named Python test scenarios with unittest subtests.
category: language
language: python-unittest
requires: [test-scenarios]
---

# Python unittest Named Test Scenarios

This guide supplements the shared test-scenarios guidance with unittest-specific named test
mechanics.

## Named Test Scenarios

Use `subTest` with descriptive labels for related scenarios. Failures must identify the scenario
without requiring readers to inspect the test implementation.

Keep a test method focused on one meaningful behavior. Use separate tests or classes when grouping
materially different behaviors would reduce clarity.

Example shape:

```python
class CreateUserTests(unittest.TestCase):
    def test_create_user(self) -> None:
        cases = [
            ("valid user", "user@example.com", True),
            ("duplicate email", "taken@example.com", False),
        ]

        for name, email, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(create_user(email), expected)
```
