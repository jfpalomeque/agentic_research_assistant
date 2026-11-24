# Agentic Research Assistant

An OpenCode-based research environment for archaeological research.

## Installation

Clone this repository and enter the directory:

```bash
git clone https://github.com/jfpalomeque/agentic_research_assistant.git
cd agentic_research_assistant
```

Then install the dependencies (see [Requirements](#requirements) below):

```bash
uv sync
```

You can then open the project in OpenCode from this directory.

## Requirements

Install these before using the repository:

- [OpenCode](https://opencode.ai)
- [Git](https://git-scm.com/downloads)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Python 3.11 or newer — uv can install and manage this, so a separate Python installation is optional.

`uv sync` installs the project dependencies, including:

- [`ariadnesearch-cli`](https://github.com/jfpalomeque/ariadnesearch-cli) and its dependencies.

## Start a demo

New to AI agents? Open this project in OpenCode and ask a question in ordinary language. For example:

- “What can I do with the archaeological site files?”
- “Create a preliminary finds report for this site.”
- “Check this dataset for errors or missing information.”
- “Compare the Neolithic crop evidence in the two excavation reports.”

See the printable [demo guide](DEMO.md) for copy-and-paste prompts, expected outputs and suggested demo routes.

## Example workflows

- EW1. Find, in ARIADNE, Neolithic sites 50 km around the city of York, UK.
- EW2. Find, in ARIADNE, Neolithic sites 50 km around the city of York, UK, with charred plant remains and/or radiocarbon dates, and save them in a CSV file.
- EW3. Find the underlying report for the Echline Fields ARIADNE record. If accessible, check its evidence for charred plant remains and cite the relevant pages. If not, explain what the catalogue says and why the claim remains unverified.
- EW4. Provide bibliographic details for https://doi.org/10.1017/S0003598X00047864.
- EW5. Find bibliographic details for Enrico Crema's 2022 paper about SPDs.
- EW6. Find works indexed by OpenAlex that cite Stevens and Fuller's 2012 paper on the decline of Neolithic crop cultivation, and save their bibliographic details in a BibTeX file.
- EW7. Find works referenced by Stevens and Fuller's 2012 paper using OpenAlex, and save their bibliographic details in a BibTeX file.
- EW8. Find ARIADNE catalogue records relating to the Late Neolithic in Scotland and summarise their geographical distribution.
- EW9. Compare the evidence for Neolithic crop cultivation at Meadowend Farm and Kinbeachie, using the reports in `demo_files/`. Create a table with: site, dated Neolithic context, identified plant remains, dating evidence, reported interpretation, limitations, and page references. Clearly distinguish directly observed evidence from the authors' interpretation. Do not treat charcoal alone as crop evidence.
- EW10. Using the finds and context registers in `demo_files/archaeological_site_files/`, join finds to their archaeological contexts. Which excavation areas, published periods and feature types contain the greatest total recorded weight of iron, slag, industrial waste and building material? Provide summary tables and context-level evidence, keeping counts and weights separate. Flag unspecified weight units, unmatched contexts and ambiguous period codes rather than guessing. Save the methodology, findings, source references and limitations as a Markdown report in `research/`.
- EW11. Using the files in `demo_files/archaeological_site_files/`, join the quantified finds, finds log, pottery and lithics to the context register and produce a preliminary whole-site finds report. Summarise each material class and its context, area and period distribution; flag unspecified weight units, unmatched contexts, ambiguous period codes and possible overlapping records rather than guessing. Save the methodology, findings, source references and limitations as a Markdown report in `research/`.
- EW12. Audit `demo_files/archaeological_site_files/` for duplicate records, unmatched contexts, undefined codes, missing units and inconsistent period fields. Produce an issue register with source rows and recommended checks. Do not alter the source data.
- EW13. Use `Fill_of` in `Context_Reg.csv` to reconstruct cut-and-fill relationships. Identify fills without valid parent cuts, cuts without recorded fills and finds attached to cuts rather than fills. Produce a traceable relationship table and flag uncertainties rather than inferring missing stratigraphy.
- EW14. Generate a complete evidence dossier for selected contexts in `demo_files/archaeological_site_files/`, combining their description, parent cut, area, period, quantified finds, pottery, lithics and spot dates. Include source-row references and distinguish observed records from interpretation. Save the dossiers as Markdown in `research/`.
- EW15. Produce a combined specialist finds study with separate pottery and lithic sections. Summarise pottery by date, fabric, form, condition and EVE, and lithics by raw material, type, technology, cortex, rolling, breakage and burning. Relate both assemblages to contexts and areas, identify the contexts driving each category, and assess preservation and collection limitations. Flag undefined fabrics, inconsistent condition codes and unsupported phase abbreviations rather than re-identifying or rephasing material. Save the methodology, findings, source references and limitations as a Markdown report in `research/`.
- EW16. Inspect the CSVs in `demo_files/archaeological_site_files/` and explain what research questions and workflows they can support. Summarise each file's contents, key fields, join relationships, coverage and data-quality limitations. Suggest concrete follow-up prompts grouped by theme, stating the required files, expected output and any additional data needed. Distinguish questions answerable from the supplied data from those requiring assumptions or external evidence. Save the capability guide as a Markdown report in `research/`.

## Resetting the conference demo

The demonstration computer is already configured with OpenCode, its web interface, the required dependencies, and a dedicated event API key. Volunteers do not need to reinstall anything.

Before the event, test the setup and create a **local** baseline tag in the demo repository:

```bash
git tag demo-ready
```

Once a visitor has finished, open a terminal **in the ARA repository root** and run:

```bash
git reset --hard demo-ready
git clean -fdX -- research/
```

- `git reset --hard demo-ready` restores tracked project files to the tested baseline and discards changes made to them.
- `git clean -fdX -- research/` deletes ignored research outputs and temporary files under `research/`. Original demonstration inputs in `demo_files/` and the installed environment are retained.
- These commands **do not clear OpenCode conversation history** or untracked files outside `research/`. Start a new chat for the next visitor; handle old demonstration sessions separately if needed.
- Refresh the OpenCode web page if the file explorer still shows old files or does not show newly generated ones.

**Warning:** The reset permanently discards local changes to tracked files and ignored files in `research/`. Only run it when the previous visitor has finished. The `demo-ready` tag must already exist on that computer. Event API credentials should remain outside tracked files and must be revoked after the event.

## Writing research outputs

Use OpenCode's dedicated file-editing tools when creating or updating reports, notes, CSV files, and other repository artefacts. Do not use long shell commands to construct file contents when a dedicated editing tool is available: shell safety checks may reject complex commands, leaving the intended output unwritten. Use the terminal for standalone research tools and data-processing commands where it is the appropriate interface.

The literature skill's standalone Python helpers search Crossref, look up a DOI, and export OpenAlex citing or referenced works to BibTeX. Run `python3 .opencode/skills/literature/scripts/crossref.py --help`, `python3 .opencode/skills/literature/scripts/openalex_citations.py --help`, or `python3 .opencode/skills/literature/scripts/openalex_references.py --help` for usage. Optionally set `CROSSREF_MAILTO` to a real contact email for Crossref requests. `OPENALEX_API_KEY` is optional for ordinary paging and required for cursor paging beyond 10,000 OpenAlex results; usage may be metered. Individual bibliographic lookups are answered inline by default, with saving offered on request.

## References

Sources used by the demo files and example workflows:

- Barclay, G J, Carter, S P, Dalland, M M, Hastie, M, Holden, T G, MacSween, A & Wickham-Jones, C R 2001. 'A possible Neolithic settlement at Kinbeachie, Black Isle, Highland'. *Proceedings of the Society of Antiquaries of Scotland* 131, 57–85. https://doi.org/10.9750/PSAS.131.57.85 — `demo_files/neolithic_reports/barclay-et-al-2001-kinbeachie-neolithic-settlement.pdf`.
- Jones, E, Sheridan, A & Franklin, J 2018. 'Neolithic and Bronze Age occupation at Meadowend Farm, Clackmannanshire: pots, pits and roundhouses'. *Scottish Archaeological Internet Reports* 77. https://doi.org/10.9750/issn.2056-7421.2018.77 — `demo_files/neolithic_reports/jones-et-al-2018-meadowend-farm-neolithic-bronze-age.pdf`.
- Cotswold Archaeology 2024. *Site Data from an Archaeological Excavation at the DIRFT III Development Area, Watling Street, Northamptonshire, August 2015 to April 2016*. https://doi.org/10.5284/1122828 — source for the `site_records` collection.
