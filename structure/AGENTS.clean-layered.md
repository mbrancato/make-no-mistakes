---
id: clean-layered
title: Clean, Layered Architecture
summary: Expectations for clean, layered code structure and runtime behavior.
category: structure
---

# Layout, Naming, and Dependencies

Keep code modular with clear, focused responsibilities. Use names that communicate the domain role
and behavior of the thing being named; avoid ambiguous abbreviations and names tied to incidental
implementation details.

Keep functions, modules, and components small enough that their responsibility, inputs, outputs, and
error behavior are understandable without excessive navigation. Split code when responsibilities are
mixed, but do not fragment cohesive behavior merely to meet an arbitrary size limit.

Dependencies must point from higher-level policy toward lower-level details through stable
boundaries. Domain and application logic must not depend directly on delivery mechanisms,
infrastructure clients, or framework details when an adapter boundary can isolate them. Avoid
dependency cycles.

Prefer capabilities already provided by the project, its standard library, or existing dependencies.
Before adding a dependency, verify that it solves a material problem better than the current stack
and does not duplicate an overlapping utility, framework, or transitive dependency workaround.

Add a dependency when it provides a clear, maintained capability that would otherwise require
substantial bespoke, risky, or poorly supported code. Evaluate its maintenance, license
compatibility, security posture, transitive footprint, version compatibility, operational burden,
and upgrade or removal cost. Add the narrowest suitable dependency at the correct layer, and
document non-obvious or high-impact additions in the change description or relevant documentation.

# Interfaces and Reuse

Use interfaces, protocols, abstract classes, traits, or equivalent boundaries when they define a
meaningful contract, permit substitution, improve testability, reduce coupling, encapsulate external
details, or support multiple credible implementations.

Do not introduce abstractions solely for abstraction. A direct implementation is preferable when an
added boundary does not provide a clear architectural benefit.

Prefer reuse to duplicated behavior. Share or extract substantially identical logic only when the
resulting abstraction has a coherent responsibility and preserves clear intent.

# Errors and Compatibility

Handle errors deliberately. Validate inputs at appropriate boundaries, preserve useful diagnostic
context, and return or propagate failures using established project conventions. Do not silently
swallow errors or use exceptional control flow for normal expected outcomes unless that is idiomatic
for the environment.

Avoid breaking public behavior and interfaces unless the change explicitly requires it. When a
contract changes, identify and update callers, tests, and documentation consistently; preserve
compatibility where practical.

# Documentation and Comments

Document public and reusable code using the language's standard documentation format. Explain
contracts, guarantees, inputs, outputs, error behavior, side effects, and non-obvious constraints as
needed. Do not add comments that merely restate the code.

Keep user-facing and developer-facing documentation current for installation, configuration, usage,
APIs, examples, operational procedures, and development workflows affected by a change.

# Configuration and Runtime Resilience

Keep configuration explicit, validated at startup where possible, and separate from code. Never
commit secrets, log secret values, or require production credentials for local development or tests.

Give network and external-service operations bounded timeouts. Retry only transient, idempotent
operations with bounded attempts and backoff; surface final failures with useful context rather than
retrying indefinitely.

Applications that manage long-lived work must handle termination signals gracefully: stop accepting
new work, cancel or drain in-flight work within a bounded deadline, release resources, and exit with
an accurate status.
