# Try the Agentic Research Assistant

An AI research assistant for archaeology. It can read excavation reports, explore site datasets, combine evidence across files and produce traceable research notes.

**You do not need to know anything about AI agents.** Open this project in OpenCode, type a question in ordinary language and ask follow-up questions.

## Start here

1. Open the project in OpenCode from this folder.
2. Copy one of the questions below into the chat.
3. Ask a follow-up such as “Show me the sources” or “What can’t you conclude?”

You do not need to mention an **EW number**; those are simply examples in the [full workflow catalogue](README.md#example-workflows).

## Four questions to try

### 1. Explore the archaeological site files — EW16

> I have archaeological data in this project. What can you help me investigate? First, explain what files are available, what each can support, and suggest three possible next questions. State any important limitations in plain language.

**What it shows:** how the assistant understands a dataset before analysing it.

### 2. Create a whole-site finds report — EW11

> Using the archaeological site files, create a preliminary finds report for the whole site. Join the finds to their contexts, summarise the pottery, lithics and other material, and flag missing information or uncertain dates. Save the report as Markdown.

**What it shows:** multi-file analysis, synthesis and a usable research output.

### 3. Check the dataset for problems — EW12

> Audit the archaeological site files for duplicate records, unmatched contexts, undefined codes, missing units and inconsistent periods. Show the source rows and recommend what should be checked. Do not change the original files.

**What it shows:** critical checking rather than simply accepting the data.

### 4. Compare two excavation reports — EW9

> Compare the evidence for Neolithic crop cultivation at Meadowend Farm and Kinbeachie. Distinguish observed plant remains from the authors’ interpretation, do not treat charcoal alone as crop evidence, and cite the relevant pages.

**What it shows:** document reading, evidence comparison and page-level citation.

## What you should expect

- Answers grounded in the supplied files.
- Clear separation between **observed evidence** and **interpretation**.
- Source rows or report pages so claims can be checked.
- Honest statements about missing units, uncertain dates and incomplete coverage.
- Markdown reports saved in `research/`.

## Useful follow-up questions

- “Show me the source rows behind that conclusion.”
- “Which findings are uncertain, and why?”
- “Turn the findings into a comparison table.”
- “What can’t you answer from these files?”
- “Give me the three contexts that need priority review.”

## Suggested demo routes

| Time available | Route |
|---|---|
| 5 minutes | EW16, then ask for a data-quality audit. |
| 10 minutes | EW11, then ask for the contexts requiring priority review. |
| Report-reading demo | EW9, then ask the assistant to defend one conclusion using its cited pages. |

## Important limits

The supplied CSVs are a **demo subset**, not the complete excavation archive. Weight units, sampling information and spatial coordinates are not available, so the assistant should not invent them or present absolute totals as precise activity measures. Demonstrating these limits is part of a responsible research workflow.

See [README.md](README.md#example-workflows) for all EW1–EW16 examples.
