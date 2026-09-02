---
id: clean-layered
title: Clean, Layered Architecture
summary: Focused responsibilities, dependency direction, interfaces, reuse, and compatibility.
category: structure
render: body
---

# Layout, Naming, and Dependencies

- Keep code modular and give each unit a focused responsibility.
- Use names that communicate the domain role and behavior.
- Avoid ambiguous abbreviations and incidental implementation details.
- Keep functions, modules, and components small enough that their responsibility, inputs, outputs,
  and error behavior are understandable without excessive navigation.
- Split units when responsibilities are mixed.
- Do not fragment cohesive behavior merely to meet an arbitrary size limit.

Dependencies must point from higher-level policy toward lower-level details through stable
boundaries.

- Keep domain and application logic independent of delivery mechanisms, infrastructure clients, and
  framework details when an adapter boundary can isolate them.
- Avoid dependency cycles.

# Interfaces and Reuse

Use interfaces, protocols, abstract classes, traits, or equivalent boundaries when they:

- Define a meaningful contract.
- Permit substitution or improve testability.
- Reduce coupling or encapsulate external details.

Do not introduce abstractions solely for abstraction. A direct implementation is preferable when an
added boundary does not provide a clear architectural benefit.

Prefer reuse to duplicated behavior. Share or extract substantially identical logic only when the
resulting abstraction has a coherent responsibility and preserves clear intent.

# Errors and Compatibility

Handle errors deliberately.

- Validate inputs at appropriate boundaries.
- Preserve useful diagnostic context.
- Return or propagate failures using established project conventions.
- Do not silently swallow errors or use exceptional control flow for normal expected outcomes unless
  idiomatic.

Avoid breaking public behavior and interfaces unless the change explicitly requires it.

- When a contract changes, identify and update callers, tests, and documentation consistently.
- Preserve compatibility where practical.
