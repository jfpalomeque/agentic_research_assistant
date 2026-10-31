# Agentic Research Assistant

A reusable OpenCode configuration for archaeological research: project instructions, skills, bundled Python tools and example workflows. It configures an existing agent harness; it is not a custom agent framework.

## Layout

- `.opencode/` — OpenCode configuration: skills, commands, agents and plugins. Only add files here that OpenCode itself discovers, such as a skill's own `scripts/`.
- `tools/` — bundled Python CLIs and scripts used across workflows. They must run standalone, without OpenCode or an LLM. Tools do not go under `src/`.
- `research/` — the user's work: inputs, notes and generated artefacts. Its contents are gitignored.
- Example workflows are listed in `README.md`. They do not get their own directories.

## Commands

Requires `pyproject.toml`; if it is absent, the toolchain has not been set up yet.

- `uv sync` — install dependencies.
- `uv run <command>` — run a tool without activating a virtualenv.
- `uv sync --frozen` — verify a clean install without changing `uv.lock`.
- Exercise a bundled tool directly before debugging it through the agent.

## Research rules

- Keep research files in `research/`. Ask before writing outside it.
- Preserve original inputs. Write derived data separately, and ask before deleting or overwriting files.
- Cite sources in notes and outputs; distinguish retrieved evidence from interpretation.
- ARIADNE catalogue metadata describes records about resources, not direct archaeological observations.
- Verify commands and tool output before claiming success. Report failures as failures.
- Semantic tool selection (choosing a tool from a natural-language request) is not semantic retrieval; do not describe keyword search as semantic search.
- Keep credentials out of the repo. ARIADNE and Zotero are optional; core workflows must work without authenticated services.

## Adapting the template

- Replace project instructions, example data and skills for a new discipline rather than modifying OpenCode itself.
- Keep bundled tools executable outside the harness and document their interfaces.
