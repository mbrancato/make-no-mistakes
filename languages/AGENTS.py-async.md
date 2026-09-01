---
id: py-async
title: Async-First Python
summary: Asyncio structured concurrency, cancellation, and non-blocking I/O.
category: language
language: python-async
requires: [python]
---

# Async-First Python

Use Python 3.11 or later. Make asynchronous functions and async-capable libraries the default at I/O
boundaries. Do not run blocking file, network, database, logging, or CPU-bound work on the
event-loop thread.

## Structured Concurrency

Run application entry points with `asyncio.run`. Do not manually manage event loops in application
code or nest event loops.

Use `asyncio.TaskGroup` for related concurrent work. Retain and await any deliberately detached
task, define its owner, and observe its exceptions. Apply `asyncio.timeout` at external boundaries,
and bound concurrency with a semaphore, queue, or worker pool rather than creating unbounded tasks
for unbounded input.

## Cancellation and Resources

Treat cancellation as normal control flow. Use `try`/`finally` for cleanup, re-raise
`CancelledError` after cleanup, and do not swallow it or use `uncancel` except for an explicitly
justified case.

Use `async with` and `async for` for resource and stream lifecycles. Explicitly close
early-terminated asynchronous generators with `aclose` or `contextlib.aclosing`.

## Boundaries and Validation

Keep asyncio objects confined to their event-loop thread. Use thread-safe scheduling APIs only at
deliberate thread boundaries. Run blocking or CPU-bound work in a bounded executor or process pool.

Enable asyncio debug mode in development and CI where practical. Treat never-awaited coroutines,
unobserved task exceptions, slow callbacks, and resource warnings as defects.

Test concurrency limits, timeouts, cancellation, cleanup, task-group error propagation, and
streaming early exits in addition to successful behavior.
