---
id: python
title: Python Coding Guidance
summary: General Pythonic coding standards and practices.
category: language
render: guide
language: python
---

# Python Coding Guidance

## Coding Standards

Follow PEP 8 and format code with the project's formatter.

- Prefer clear, explicit code, small focused functions, and descriptive names.
- Use type hints for public APIs and non-obvious values.
- Keep imports organized.
- Prefer the standard library and existing project dependencies before adding packages.
- Raise specific exceptions with useful context.
- Avoid bare `except` clauses.
- Use context managers for resources that require cleanup.
- Use docstrings for public modules, classes, functions, and methods when their contract is not
  self-evident.
- Use inline comments only to explain non-obvious intent, invariants, or tradeoffs.
- Do not restate code that clear names and structure already explain.
