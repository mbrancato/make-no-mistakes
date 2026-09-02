---
id: py-async
title: Async-First Python
summary: Asyncio structured concurrency, cancellation, and non-blocking I/O.
category: language
render: guide
language: python-async
requires: [python]
---

# Async-First Python

Use Python 3.11 or later.

- Prefer asynchronous functions and async-capable libraries at I/O boundaries.
- Do not run blocking file, network, database, logging, or CPU-bound work on the event-loop thread.

## Structured Concurrency

- Run application entry points with `asyncio.run`.
- Do not manually manage event loops in application code or nest event loops.

For concurrent work:

- Use `asyncio.TaskGroup` for related tasks.
- Retain and await deliberately detached tasks.
- Define the owner of each detached task and observe its exceptions.
- Apply `asyncio.timeout` at external boundaries.
- Bound concurrency with a semaphore, queue, or worker pool.
- Do not create unbounded tasks for unbounded input.

## Cancellation and Resources

- Treat cancellation as normal control flow.
- Use `try`/`finally` for cleanup.
- Re-raise `CancelledError` after cleanup.
- Do not swallow cancellation or use `uncancel` except for an explicitly justified case.
- Use `async with` and `async for` for resource and stream lifecycles.
- Explicitly close early-terminated asynchronous generators with `aclose` or `contextlib.aclosing`.

## Boundaries and Validation

- Keep asyncio objects confined to their event-loop thread.
- Use thread-safe scheduling APIs only at deliberate thread boundaries.
- Run blocking or CPU-bound work in a bounded executor or process pool.
- Enable asyncio debug mode in development and CI where practical.
- Treat never-awaited coroutines, unobserved task exceptions, slow callbacks, and resource warnings
  as defects.
- Test concurrency limits, timeouts, cancellation, and cleanup.
- Test task-group error propagation and streaming early exits.
- Test successful behavior as well.
