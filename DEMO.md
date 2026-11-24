# Agentic Research Assistant

*An experimental research environment for archaeology*

**Ask research questions. Explore archaeological evidence. Follow the sources.**

## What is ARA?

The Agentic Research Assistant (ARA) is an experimental environment built around OpenCode, specialist research tools, project instructions and archaeological data. It can gather information from traceable sources, work across different files and services, and produce research outputs that can be checked.

It is not a purpose-built archaeology chatbot with a fixed list of commands. Ask questions in ordinary language, then explore where the investigation leads.

## What can it do?

- **Discover archaeological records:** Search catalogues such as ARIADNE and investigate associated sources.
- **Explore academic literature:** Find publications, DOIs, citations and reference lists.
- **Read excavation reports:** Compare evidence, find relevant passages and cite pages.
- **Analyse archaeological data:** Join records, check inconsistencies and summarise finds.
- **Carry out research workflows:** Combine tools, follow leads and save reports or datasets.

## Try it on this computer

OpenCode is already running in the browser. No installation or login is needed.

1. **Ask:** Enter a question in the chat. Choose an example from page 2 or ask your own.
2. **Explore:** Read the response and use the OpenCode file explorer to inspect source files and results. Demonstration inputs are in `demo_files/`; research outputs are normally saved in `research/`.
3. **Continue:** Ask for evidence, refine the question or request a table, CSV or report.

**Can't see a newly created file?** OpenCode's file explorer sometimes does not update immediately. Refresh the browser page.

## Investigate, don't just ask

Try a short sequence of follow-up questions:

> What can you tell me about the archaeological files in this project?

> Which records might need closer checking?

> Show me the source rows behind those findings.

> Can you save a short report without changing the original data?

## Check the evidence

ARA is experimental and can make mistakes. A catalogue search result is not itself proof of an archaeological claim. Check source rows and report pages, distinguish observations from interpretations, and ask what remains uncertain or missing.

## Take ARA home

Repository, example workflows and installation instructions:

**[github.com/jfpalomeque/agentic_research_assistant](https://github.com/jfpalomeque/agentic_research_assistant)**

<!-- PRINT PAGE BREAK: the remaining sections are page 2 of the visitor handout. -->

# What can you ask ARA?

All 16 **example workflows (EWs)** are described in full in [README.md](README.md#example-workflows), which ARA can consult. You can copy and paste a complete prompt from there, or simply ask **"Run EW12 from README.md"** (or any other EW number). There is no need to type out the full instruction.

The short descriptions below are a menu of ideas, not fixed commands. You can also ask your own question. Some searches need an internet connection; local datasets and reports are already supplied.

### ARIADNE: Archaeological records

- **EW1.** Find Neolithic sites within 50 km of York.
- **EW2.** Find Neolithic sites near York with charred plant remains and/or radiocarbon dates. Save a CSV.
- **EW3.** Find the underlying report for Echline Fields and check its evidence for charred plant remains.
- **EW8.** Find Late Neolithic ARIADNE records in Scotland and summarise their geographical distribution.

### Academic literature

- **EW4.** Retrieve bibliographic details for DOI `10.1017/S0003598X00047864`.
- **EW5.** Find Enrico Crema's 2022 paper about SPDs.
- **EW6.** Find publications citing Stevens and Fuller (2012), and export BibTeX.
- **EW7.** Find publications referenced by Stevens and Fuller (2012), and export BibTeX.

### Excavation reports

- **EW9.** Compare evidence for Neolithic crop cultivation at Meadowend Farm and Kinbeachie. Cite report pages and distinguish observations from interpretation.

### Archaeological datasets

- **EW10.** Combine finds and contexts to investigate iron, slag, industrial waste and building material by area, period and feature.
- **EW11.** Produce a preliminary finds report using the context, pottery, lithic and other finds registers.
- **EW12.** Audit the site files for duplicates, unmatched contexts, undefined codes, missing units and inconsistent periods.
- **EW13.** Reconstruct recorded cut-and-fill relationships and flag missing links.
- **EW14.** Build a source-linked evidence dossier for selected archaeological contexts.
- **EW15.** Produce a specialist study of pottery and lithic assemblages.
- **EW16.** Explore the supplied CSVs and suggest research questions they could answer.

## Other questions to try

- What are the strongest and weakest conclusions supported by these files?
- Can you check whether a claim is supported by the original excavation report?
- What information is missing, and what would we need to investigate next?
- Can you compare information from two sources and explain any disagreement?
- Which records should an archaeologist review first?
- Can you investigate a related question using more than one tool?

## Useful follow-ups

**"Show me the source rows or report pages."** · **"What assumptions did you make?"** · **"Can you try another approach?"** · **"Save the methodology and results."**

*The supplied site registers are a demonstration subset, not the complete excavation archive. Treat results as provisional and check their sources.*
