---
id: go
title: Go Coding Guidance
summary: Idiomatic Go coding standards and named subtests.
category: language
language: go
requires: [test-scenarios]
---

# Go Coding Guidance

This guide describes Go-specific coding standards and test organization.

## Coding Standards

Follow idiomatic Go conventions and format code with `gofmt`. Prefer small, cohesive packages with
clear names; package names should be short, lowercase, and avoid stuttering in exported identifiers.

Prefer standard-library types and facilities when they meet the requirement. Add external
dependencies only when they provide a clear capability unavailable from the standard library or
existing project dependencies.

Write Go doc comments for exported packages, types, functions, methods, and fields when their
contract is not self-evident; begin each comment with the declared identifier. Use inline comments
only for non-obvious intent, invariants, or tradeoffs. Do not comment code that is already clear
from its names and structure.

Accept interfaces at the point of use and keep them minimal. Return concrete types unless callers
need abstraction. Prefer explicit control flow and simple composition over reflection, clever
generic abstractions, or unnecessary frameworks.

Return errors rather than panicking for expected failures. Wrap errors with operation context using
`%w` when callers need to inspect the cause, and check errors immediately. Use `context.Context` as
the first parameter for request-scoped work; propagate cancellation and deadlines rather than
creating detached contexts.

Make ownership and concurrency explicit. Do not start goroutines without a defined lifecycle,
cancellation path, and way to observe completion or errors. Protect shared state, avoid leaking
resources, and close resources at the scope that acquires them.

## Concurrency and Streaming Pipelines

Use goroutines and channels only when they make ownership, latency, or parallelism clearer than
synchronous code. Build streaming pipelines as focused, composable stages that receive input,
transform it, send output, and remain independent of other stage implementations.

Each stage closes only its outbound channel after all sends complete; receivers never close inbound
channels. Propagate `context.Context` cancellation and deadlines through every stage, and select on
cancellation for blocking sends and receives so downstream early exits cannot leak upstream
goroutines.

Use fan-out only for independently processable work, with bounded worker counts, buffering, and
resource use. Merge fan-in results only after all senders finish. Treat channel buffers as
deliberate capacity and back-pressure decisions, never as a substitute for cancellation or leak
prevention.

Define pipeline error behavior explicitly. Cancel on the first unrecoverable error unless partial
results are intentional, and return errors with useful context. Test cancellation, early consumer
exit, channel closure, error propagation, and goroutine or resource cleanup in addition to the
successful data flow.

## Test Cases

Use table-driven tests with descriptive case names for related input and behavior variations.
Execute each case as a named subtest with `t.Run`, so failures report the scenario without requiring
readers to inspect the test body.

Keep top-level test functions focused on a meaningful unit or behavior. Use nested subtests only
when the hierarchy improves the failure report and remains easy to navigate. Call `t.Parallel` only
when the test and all shared fixtures are safe for concurrent execution.

Example shape:

```go
func TestCreateUser(t *testing.T) {
    tests := []struct {
        name string
        // inputs and expected results
    }{
        {name: "valid user"},
        {name: "duplicate email"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // test one named scenario
        })
    }
}
```
