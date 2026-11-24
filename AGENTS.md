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
- When a source link is unavailable, a publicly accessible archived copy, such as one in the Internet Archive's Wayback Machine, may be worth checking. Past tasks have successfully used this approach for an ADS document. Availability is not guaranteed; cite the archived version and capture date, and respect access restrictions and copyright.
- ARIADNE catalogue metadata describes records about resources, not direct archaeological observations.
- For questions linking a site or resource to a period and specific evidence, treat search hits as candidates: check whether the available source actually connects the evidence to the requested site, period and context. A keyword match alone does not establish that relationship.
- Distinguish explicitly supported relationships from possible matches requiring source review, and exclude or explain matches where the evidence belongs to a different context. State when underlying reports have not been checked and when search terms or metadata may miss relevant evidence.
- Clarify consequential ambiguity in evidence categories when needed; for example, charcoal is charred wood but does not establish the presence of charred seeds or crops. Related evidence may appear in separate records, such as radiocarbon samples, rather than the site record.
- When the requested unit of output is ambiguous, preserve traceable source records rather than merging them into assumed sites. State clearly what each row represents and that multiple rows may refer to the same site; offer to regroup if the user prefers one row per site.
- For evidence searches with alternative conditions such as “and/or”, accept candidates supported by either condition, identify which evidence each has, and preserve relevant context and uncertainty. Do not imply that radiocarbon-dated plant material was charred unless the source says so.
- Record search terms, retrieval scope and any incomplete coverage. Review apparent keyword matches in context: terms may refer to unrelated periods, different features or descriptions such as colour. Clearly label selected results as a subset rather than a complete inventory when appropriate.
- Verify commands and tool output before claiming success. Report failures as failures.
- Semantic tool selection (choosing a tool from a natural-language request) is not semantic retrieval; do not describe keyword search as semantic search.
- Keep credentials out of the repo. ARIADNE and Zotero are optional; core workflows must work without authenticated services.

## Demo interaction

- Treat `DEMO.md` as the visitor-facing starting point and `README.md` as the complete EW catalogue.
- When a visitor asks an open-ended question about the available files, identify the relevant dataset or reports, explain useful next steps in plain language, and offer three to five concrete starter questions.
- Do not require visitors to know workflow IDs. Mention a relevant EW only as an optional example.
- Prefer the supplied local demo files so demonstrations do not depend on live external services.
- Preserve the project’s evidence standards: cite source rows or pages, distinguish observations from interpretation, and state limitations rather than filling gaps with assumptions.

## Open-ended research workflows

- For underspecified requests, identify consequential choices and explain their implications in plain language. Ask the user when a choice would materially affect the scope, method, interpretation or output. Make reasonable, reversible assumptions for minor details and state them.
- Discuss choices as evidence becomes available; do not require the user to settle every technical detail before the investigation begins.
- When you discover a useful shortcut or innovative method during a task, explain it and ask whether the user wants it documented for future workflows. Verify the method and its limitations before documenting it as reliable.
- When a tool cannot implement the requested method exactly, explain the limitation and proposed approximation. Ask the user whether it is acceptable or whether they need a more precise method, except for the default rectangular spatial approximation below.
- For ARIADNE radius queries, default to a bounding rectangle around a stated reference point and explain that results may fall outside the requested radius. Apply a precise distance filter if the user requests one; do not present rectangle matches as confirmed within the radius.
- Keep intermediate data, retrieved responses and working notes in a uniquely named per-investigation folder under `research/temp/`.
- Unless the user requests otherwise, save the final output directly in `research/`. For an open-ended question without a specified format, produce a Markdown summary report.
- In the report and response, distinguish samples from complete results, identify sources and limitations, and indicate where intermediate files were saved. Offer relevant follow-up or alternative output formats.
- Preserve existing files. Ask before overwriting or deleting them.

## Adapting the template

- Replace project instructions, example data and skills for a new discipline rather than modifying OpenCode itself.
- Keep bundled tools executable outside the harness and document their interfaces.
