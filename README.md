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
make generate INCLUDE=tdd,clean-layered,go OUTPUT=AGENTS.md
```

`INCLUDE` values are guide IDs, not category names. The structure category requires one guide;
`clean-layered` is the available structure guide.

The generator overwrites its output by default. Add `PROVENANCE=1` to include the selected guide IDs
and generator version in output front matter. Provenance is omitted by default.

## Make Targets

| Command                                                   | Purpose                             |
| --------------------------------------------------------- | ----------------------------------- |
| `make`                                                    | Format Markdown files.              |
| `make generate`                                           | Interactively generate `AGENTS.md`. |
| `make generate INCLUDE=tdd,clean-layered,python,py-async` | Generate from specified guide IDs.  |
| `make test`                                               | Run generator tests.                |
| `make help`                                               | List available targets.             |

## Layout

The guides are intentionally layered. Shared guidance defines cross-language expectations, while a
language guide adds only language-specific conventions.

| Folder           | Category              | Selection            |
| ---------------- | --------------------- | -------------------- |
| `structure/`     | Code Structure        | Required; select one |
| `process/`       | Development Process   | Required; select one |
| `support/`       | Development Support   | Optional; select any |
| `guidance/`      | Shared Guidance       | Optional; select any |
| `testing/`       | Testing               | Optional; select any |
| `observability/` | Observability and Ops | Optional; select any |
| `languages/`     | Language-Specific     | Optional; select any |

The root `AGENTS.all.md` guide supplies the shared header and is included automatically.

More-specific repository, directory, language, and framework guidance supplements the shared guides.
When guidance conflicts, follow the most-specific applicable instruction unless it violates an
explicit task requirement.

The structure category is a required one-of choice for high-level code layout and architecture. The
process category is a required one-of choice for the high-level development workflow. Development
Support, guidance, testing, observability, and language guides are composable and may be selected
together. Guide dependencies are included automatically.
