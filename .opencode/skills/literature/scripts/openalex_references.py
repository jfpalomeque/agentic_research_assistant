#!/usr/bin/env python3
"""Export works linked as references of an OpenAlex work to BibTeX."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from openalex_citations import API, bibtex, request_json, write_new


def crossref_record(doi):
    url = "https://api.crossref.org/works/" + quote(doi, safe="")
    with urlopen(Request(url, headers={"User-Agent": "ARA-literature-lookup/1.0"}), timeout=30) as response:
        return url, json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("seed", help="Seed DOI, doi.org URL, OpenAlex ID or OpenAlex URL")
    parser.add_argument("--output", required=True, type=Path, help="New BibTeX file; never overwritten")
    parser.add_argument("--workdir", required=True, type=Path, help="Existing empty directory for raw responses and manifest")
    args = parser.parse_args()
    if args.output.exists() or not args.workdir.is_dir() or any(args.workdir.iterdir()):
        parser.error("output must not exist and workdir must be an existing empty directory")
    if not args.output.parent.is_dir():
        parser.error("output parent directory must exist")
    seed = args.seed.strip()
    if seed.lower().startswith("https://openalex.org/"):
        seed = seed.rsplit("/", 1)[-1]
    elif seed.lower().startswith("https://doi.org/"):
        seed = seed[len("https://doi.org/"):]
    if re.fullmatch(r"W\d+", seed, re.I):
        seed_url = API + "/" + seed.upper()
    elif re.fullmatch(r"10\.\d{4,9}/\S+", seed, re.I):
        seed_url = API + "/https://doi.org/" + quote(seed, safe="")
    else:
        parser.error("seed must be a DOI, doi.org URL or OpenAlex work ID")
    manifest = {"source": "OpenAlex", "direction": "references", "started_at": datetime.now(timezone.utc).isoformat(),
                "seed_request": seed_url, "batches": [], "complete": False}
    try:
        seed_record = request_json(seed_url)
        write_new(args.workdir / "seed.json", json.dumps(seed_record, ensure_ascii=False, indent=2))
        manifest["seed"] = {k: seed_record.get(k) for k in ("id", "doi", "title", "publication_year")}
        refs = seed_record["referenced_works"]
        if not isinstance(refs, list) or any(not re.fullmatch(r"https://openalex\.org/W\d+", ref) for ref in refs):
            raise ValueError("OpenAlex reference list missing or invalid")
        refs = list(dict.fromkeys(refs))
        manifest["linked_references"] = len(refs)
        manifest["reported_reference_count"] = seed_record.get("referenced_works_count")
        works = {}
        for start in range(0, len(refs), 100):
            batch = refs[start:start + 100]
            ids = "|".join(ref.rsplit("/", 1)[-1] for ref in batch)
            url = API + "?" + urlencode({"filter": "openalex:" + ids, "per_page": 100})
            payload = request_json(url)
            write_new(args.workdir / f"batch-{start // 100 + 1:04d}.json", json.dumps(payload, ensure_ascii=False, indent=2))
            results = payload["results"]
            manifest["batches"].append({"url": url, "requested": len(batch), "returned": len(results)})
            for work in results:
                if work["id"] in batch:
                    works[work["id"]] = work
        manifest["unresolved_ids"] = [ref for ref in refs if ref not in works]
        manifest["unique_records"] = len(works)
        manifest["complete"] = not manifest["unresolved_ids"] and (
            manifest["reported_reference_count"] is None or manifest["reported_reference_count"] == len(refs))
        manifest["missing_doi"] = sum(not w.get("doi") for w in works.values())
        manifest["missing_title"] = sum(not w.get("title") for w in works.values())
        manifest["missing_author"] = sum(not w.get("authorships") for w in works.values())
        manifest["missing_year"] = sum(not w.get("publication_year") for w in works.values())
        doi_url = seed_record.get("doi") or ""
        doi = doi_url.removeprefix("https://doi.org/")
        if re.fullmatch(r"10\.\d{4,9}/\S+", doi, re.I):
            try:
                cr_url, crossref = crossref_record(doi)
                write_new(args.workdir / "crossref-seed.json", json.dumps(crossref, ensure_ascii=False, indent=2))
                metadata = crossref["message"]
                references = metadata.get("reference", [])
                openalex_dois = {w["doi"].removeprefix("https://doi.org/").lower() for w in works.values() if w.get("doi")}
                deposited_dois = {r["DOI"].lower() for r in references if r.get("DOI")}
                manifest["crossref_comparison"] = {"url": cr_url, "reported_reference_count": metadata.get("reference-count"),
                    "deposited_entries": len(references), "entries_with_doi": sum(bool(r.get("DOI")) for r in references),
                    "unique_dois_matching_openalex": len(deposited_dois & openalex_dois),
                    "dois_not_matching_openalex": sorted(deposited_dois - openalex_dois),
                    "limitation": "Exact DOI comparison only; unmatched DOI does not prove a work is absent, and entries without DOIs are not compared."}
            except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as error:
                manifest["crossref_comparison"] = {"error": str(error)}
        write_new(args.output, "\n".join(bibtex(works[ref]) for ref in refs if ref in works))
        manifest["output"] = str(args.output)
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        manifest["error"] = str(error)
    manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
    write_new(args.workdir / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if manifest["complete"] else 1


if __name__ == "__main__":
    sys.exit(main())
