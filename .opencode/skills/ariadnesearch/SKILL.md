---
name: ARIADNE catalogue search
description: Use the installed ariadnesearch CLI to find ARIADNE catalogue records or follow a known ARIADNE record to its underlying source, report, DOI or archive.
---

# ARIADNE catalogue research

1. Run `uv run ariadnesearch docs` for the installed CLI's current commands, arguments and limitations. Use `uv run ariadnesearch search` to discover catalogue records and `uv run ariadnesearch get RECORD_ID` to inspect a known record. A record ID may appear at the end of an ARIADNE portal resource URL.
2. For an existing record, inspect its metadata, including the search candidate's `raw` data or the full `get` response, for a DOI, landing page, source identifier or archive link. Follow promising source links before using general web search as a fallback. A catalogue identifier is not necessarily a direct report link.
3. If asked to check an underlying report, locate and read the relevant source content when accessible, and cite page numbers where available. Clearly distinguish catalogue descriptions from evidence actually checked in the source. If access or reading fails, report what was attempted and the specific limitation; do not claim the report was checked.
4. ARIADNE returns catalogue records, not verified archaeological observations. Preserve record links and distinguish records from sites. Follow the research and output rules in `AGENTS.md`, including limitations on spatial approximations and evidence associations.
