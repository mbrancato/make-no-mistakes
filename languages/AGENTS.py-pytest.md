---
id: py-pytest
title: Python pytest Named Test Scenarios
summary: Named Python test scenarios with pytest parameter IDs.
category: language
render: guide
language: python-pytest
requires: [test-scenarios]
---

# Python pytest Named Test Scenarios

This guide supplements the shared test-scenarios guidance with pytest-specific named test mechanics.

## Named Test Scenarios

Use pytest parameterized tests with explicit `id` values for related scenarios.

- Ensure failures identify the scenario without requiring readers to inspect the implementation.
- Keep each test function or method focused on one meaningful behavior.
- Use separate tests or classes when grouping materially different behaviors would reduce clarity.

Example shape:

```python
@pytest.mark.parametrize(
    ("email", "expected"),
    [
        pytest.param("user@example.com", True, id="valid user"),
        pytest.param("taken@example.com", False, id="duplicate email"),
    ],
)
def test_create_user(email: str, expected: bool) -> None:
    assert create_user(email) is expected
```
