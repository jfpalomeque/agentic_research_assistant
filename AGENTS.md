# Agentic Research Assistant

A reusable OpenCode configuration for archaeological research: project instructions, skills, bundled Python CLIs and a guided example workflow. It configures an existing agent harness; it is not a custom agent framework.

## Layout

- `.opencode/` — project skills and commands. The guided tour is `/tour`.
- `src/research_tools/` — bundled Python CLIs, usable directly without OpenCode or an LLM.
- `examples/` — sample data and scenario supporting the tour.
- Research files may be created anywhere in the repo. There is no mandatory `data/`, `temp/` or `outputs/` pipeline; follow existing conventions.

## Commands

Requires `pyproject.toml`; if it is absent, the toolchain has not been set up yet.

- `uv sync` — install dependencies.
- `uv run <command>` — run a CLI without activating a virtualenv.
- `uv sync --frozen` — verify a clean install without changing `uv.lock`.
- Test a bundled CLI directly (`uv run <cli> --help`) before debugging it through the agent.

## Research rules

- Preserve original inputs. Write derived data separately, and ask before deleting or overwriting files.
- Cite sources in notes and outputs; distinguish retrieved evidence from interpretation.
- ARIADNE catalogue metadata describes records about resources, not direct archaeological observations.
- Verify commands and tool output before claiming success. Report failures as failures.
- Semantic tool selection (choosing a tool from a natural-language request) is not semantic retrieval; do not describe keyword search as semantic search.
- Keep credentials out of the repo. ARIADNE and Zotero are optional; the core tour must work without authenticated services.

## Adapting the template

- Replace project instructions, example data and skills for a new discipline rather than modifying OpenCode itself.
- Keep bundled CLIs executable outside the harness and document their interfaces.
