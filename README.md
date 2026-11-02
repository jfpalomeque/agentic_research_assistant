# Agentic Research Assistant

An OpenCode-based research environment for archaeological research.

## Requirements

Install these before using the repository:

- [OpenCode](https://opencode.ai)
- [Git](https://git-scm.com/downloads)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.11 or newer — uv can install and manage this, so a separate Python installation is optional.

`uv sync` installs the project dependencies, including:

- [`ariadnesearch-cli`](https://github.com/jfpalomeque/ariadnesearch-cli) and its dependencies.

## Example workflows

EW1. Find, in ARIADNE, Neolithic sites 50 km around the city of York, UK.
EW2. Find, in ARIADNE, Neolithic sites 50 km around the city of York, UK, with charred plant remains and/or radiocarbon dates, and save them in a CSV file.
EW3. Find the underlying report for the Echline Fields ARIADNE record. If accessible, check its evidence for charred plant remains and cite the relevant pages. If not, explain what the catalogue says and why the claim remains unverified.
EW4. Provide bibliographic details for https://doi.org/10.1017/S0003598X00047864.
EW5. Find bibliographic details for Enrico Crema's 2022 paper about SPDs.
EW6. Find works indexed by OpenAlex that cite Stevens and Fuller's 2012 paper on the decline of Neolithic crop cultivation, and save their bibliographic details in a BibTeX file.
EW7. Find works referenced by Stevens and Fuller's 2012 paper using OpenAlex, and save their bibliographic details in a BibTeX file.

The literature skill's standalone Python helpers search Crossref, look up a DOI, and export OpenAlex citing or referenced works to BibTeX. Run `python3 .opencode/skills/literature/scripts/crossref.py --help`, `python3 .opencode/skills/literature/scripts/openalex_citations.py --help`, or `python3 .opencode/skills/literature/scripts/openalex_references.py --help` for usage. Optionally set `CROSSREF_MAILTO` to a real contact email for Crossref requests. `OPENALEX_API_KEY` is optional for ordinary paging and required for cursor paging beyond 10,000 OpenAlex results; usage may be metered. Individual bibliographic lookups are answered inline by default, with saving offered on request.
