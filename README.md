# Make No Mistakes

A set of general and language-specific instructions for coding agents to help efficiently produce
high-quality code.

## Generate an AGENTS.md

Every source guide has YAML front matter that identifies its stable `id`, title, summary, category,
optional language, and any dependencies. The generator discovers these guides automatically.

Run `make generate` in a terminal to select guides interactively. For automation, select IDs with
`INCLUDE` as a comma-separated list of guide IDs and specify the output file with `OUTPUT`. For
example:

```sh
make generate INCLUDE=process,structure,go OUTPUT=AGENTS.md
```

The generator overwrites its output by default. Add `PROVENANCE=1` to include the selected guide IDs
and generator version in output front matter. Provenance is omitted by default.

## Make Targets

| Command                                 | Purpose                             |
| --------------------------------------- | ----------------------------------- |
| `make`                                  | Format Markdown files.              |
| `make generate`                         | Interactively generate `AGENTS.md`. |
| `make generate INCLUDE=python,py-async` | Generate from specified guide IDs.  |
| `make test`                             | Run generator tests.                |
| `make help`                             | List available targets.             |

## Layout

The guides are intentionally layered. Shared guidance defines cross-language expectations, while a
language guide adds only language-specific conventions.

| Location                                     | Scope                                                   |
| -------------------------------------------- | ------------------------------------------------------- |
| `process/AGENTS.tdd.md`                      | Development workflow and definition of done             |
| `process/AGENTS.development-commands.md`     | Setup and verification command guidance                 |
| `process/AGENTS.pull-request.md`             | Review-ready change and handoff guidance                |
| `structure/AGENTS.clean-layered.md`          | Code structure, design, dependencies, and compatibility |
| `structure/AGENTS.vertical-slice.md`         | Feature-oriented code organization                      |
| `guidance/AGENTS.runtime-resilience.md`      | Shared runtime resilience guidance                      |
| `guidance/AGENTS.security-configuration.md`  | Shared security and secure-boundary guidance            |
| `testing/AGENTS.test-design.md`              | Behavioral test design and coverage                     |
| `testing/AGENTS.integration-tests.md`        | Integration test infrastructure                         |
| `testing/AGENTS.testcontainers.md`           | Testcontainers integration testing                      |
| `testing/AGENTS.test-scenarios.md`           | Named and parameterized test scenarios                  |
| `observability/AGENTS.structured-logging.md` | Structured logging                                      |
| `observability/AGENTS.openmetrics.md`        | OpenMetrics endpoint                                    |
| `observability/AGENTS.opentelemetry.md`      | OpenTelemetry tracing                                   |
| `observability/AGENTS.health-checks.md`      | Liveness and readiness checks                           |
| `languages/AGENTS.go.md`                     | Go-specific guidance                                    |
| `languages/AGENTS.py.md`                     | General Python coding guidance                          |
| `languages/AGENTS.py-async.md`               | Async-first Python guidance                             |
| `languages/AGENTS.py-pytest.md`              | pytest named test scenarios                             |
| `languages/AGENTS.py-unittest.md`            | unittest named test scenarios                           |

More-specific repository, directory, language, and framework guidance supplements the shared guides.
When guidance conflicts, follow the most-specific applicable instruction unless it violates an
explicit task requirement.

The structure category is a required one-of choice for high-level code layout and architecture.
Guidance, process, testing, observability, and language guides are composable and may be selected
together. Guide dependencies are included automatically.
