---
name: Literature lookup
description: Find publication metadata by DOI or partial details, or export OpenAlex citing works or references to BibTeX.
---

# Literature lookup

Use the Crossref helper at `scripts/crossref.py` (relative to this skill directory). It uses Python 3.11+ and the standard library; no API key is required. Run `python3 <skill-directory>/scripts/crossref.py --help` for the interface. An optional `CROSSREF_MAILTO` environment variable supplies a real contact email to Crossref; never invent one.

## Known DOI

1. Run `python3 <skill-directory>/scripts/crossref.py get 'DOI-or-doi.org-URL'`. Inspect the returned record, including its type, dates, abstract and any update information.
2. If Crossref cannot find the DOI, do not assume it is invalid: it may be registered elsewhere. Check another appropriate source if available, and report what was attempted. Do not invent missing metadata.

## Publication from partial details

1. Extract the author's name, approximate year, title words and topic. Expand shorthand where appropriate, but state consequential assumptions; for example, SPD may mean summed probability distribution of radiocarbon dates.
2. Search with the clues, for example `python3 <skill-directory>/scripts/crossref.py search --author 'Enrico Crema' --query 'summed probability distributions radiocarbon' --year 2022`. The search is keyword-based, not semantic. Crossref ranks candidates, not confirmed matches, and author queries are not exact filters.
3. Compare candidate author, date, title and context. Broaden or vary terms and dates if needed. Retrieve promising candidates with `get` to inspect full metadata and the abstract. If the match remains uncertain, present alternatives or ask the user; do not turn a likely match into a certainty.

## Export works citing a paper

1. Identify the seed using a DOI or the partial-details workflow; confirm it is the intended work. OpenAlex's `cites` filter finds works that cite the seed, not works cited by it, and is not a subject relevance screen.
2. Create a unique investigation directory under `research/temp/`, and select a new output filename under `research/` without overwriting. Run `python3 <skill-directory>/scripts/openalex_citations.py 'DOI-or-OpenAlex-ID' --workdir research/temp/<unique-directory> --output research/<new-file>.bib`. The work directory must exist and be empty. The script preserves the seed and each raw response and produces a manifest with source URLs, counts and completeness checks.
3. Inspect the manifest and exit status. Report the seed, source, retrieval date, number exported, missing metadata, and any failure or incomplete pagination. Counts can change while paging; matching counts do not guarantee a consistent snapshot or complete coverage. Do not claim that a partial export is complete. BibTeX preserves source types where mapped and uses `misc` for other types; bibliographic metadata may need review.
4. The helper uses basic paging through 10,000 records without a key. Larger sets require cursor paging and `OPENALEX_API_KEY` in the environment; keys are sent in an authorization header, never saved in URLs or output. API usage may be metered. Retries for rate limits are bounded. Do not silently substitute backward references for forward citations.

## Export works referenced by a paper

1. Identify the seed as above. Run `python3 <skill-directory>/scripts/openalex_references.py 'DOI-or-OpenAlex-ID' --workdir research/temp/<unique-empty-directory> --output research/<new-file>.bib`. This retrieves the seed's OpenAlex `referenced_works` IDs and resolves them in batches, not works citing the seed.
2. Inspect the manifest and exit status and report the linked, resolved and unresolved counts, missing fields, and source. The script saves the seed, batch responses and manifest. When a seed DOI is available it also attempts a Crossref reference-list comparison and saves the response. The comparison matches exact DOIs only: a non-match does not prove absence, and references without DOIs are not compared. Crossref-only references are not exported.
3. Completion means all IDs in OpenAlex's returned list were resolved, not that the paper's entire bibliography was captured. Check the original bibliography if a complete transcription is needed. Do not overwrite existing outputs.

## Answer and limitations

- Default to a Chicago author-date citation and a concise bibliographic field list. Preserve the deposited title in the details. Include the abstract when available, labelled as source metadata; do not silently paraphrase it. If unavailable, say so. Respect copyright when presenting source text.
- Cite the record URL and retrieval date. For partial-detail searches, also state search clues, assumptions, scope and limitations. Distinguish the metadata or abstract from the full text, which may not have been checked. API ranking, a title match, an absent update notice or absent open-access information does not establish a conclusion about the paper.
- Report material source disagreements and separate online and issue dates when relevant. Do not assume a DOI denotes a journal article, that an update notice exists or does not exist beyond the retrieved metadata, or that a missing open-access link means no copy exists.
- For these individual bibliographic lookups, answer inline and offer to save; do not create research files unless the user asks. If saving is requested, follow `AGENTS.md`, preserve existing files and ask before overwriting. Broader open-ended research still follows the research workflow rules in `AGENTS.md`.
