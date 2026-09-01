.DEFAULT_GOAL := all

.PHONY: all format generate help test

all: format ## Format all Markdown files.

format: ## Format all Markdown files.
	prettier --prose-wrap always --print-width 100 --write '**/*.md'

generate: ## Interactively generate AGENTS.md.
	python3 scripts/generate_agents.py $(if $(INCLUDE),--include "$(INCLUDE)") $(if $(OUTPUT),--output "$(OUTPUT)") $(if $(PROVENANCE),--provenance)

test: ## Run generator tests.
	python3 -m unittest discover -s tests

help: ## Show available targets.
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "%-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
