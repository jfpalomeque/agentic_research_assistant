#!/usr/bin/env python3
"""Export OpenAlex works citing a DOI or OpenAlex work ID to BibTeX."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

API = "https://api.openalex.org/works"


def request_json(url):
    headers = {"User-Agent": "ARA-literature-lookup/1.0"}
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        headers["Authorization"] = "Bearer " + key
    for attempt in range(4):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code != 429 or attempt == 3:
                raise
            retry = error.headers.get("Retry-After", "")
            delay = max(2 ** attempt, int(retry)) if retry.isdigit() else 2 ** attempt
            time.sleep(min(delay, 60))


def escape(value):
    # Protect TeX metacharacters without interpreting deposited metadata as TeX.
    substitutions = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}",
                     "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
                     "_": r"\_", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(substitutions.get(c, c) for c in re.sub(r"\s+", " ", str(value)).strip())


def bibtex(work):
    types = {"article": "article", "book": "book", "book-chapter": "incollection", "dissertation": "phdthesis"}
    kind = types.get(work.get("type"), "misc")
    key = work["id"].rstrip("/").split("/")[-1]
    fields = []
    def add(name, value):
        if value is not None and str(value).strip():
            fields.append(f"  {name} = {{{escape(value)}}},")
    if work.get("title"):
        fields.append("  title = {{" + escape(work["title"]) + "}},")
    names = [a.get("author", {}).get("display_name") for a in work.get("authorships", [])]
    names = [name for name in names if name]
    if names:
        # Braced names preserve OpenAlex display names, including organisations.
        fields.append("  author = {" + " and ".join("{" + escape(name) + "}" for name in names) + "},")
    add("year", work.get("publication_year"))
    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    if kind == "article":
        add("journal", source.get("display_name"))
    elif kind == "incollection":
        add("booktitle", source.get("display_name"))
    biblio = work.get("biblio") or {}
    add("volume", biblio.get("volume"))
    add("number", biblio.get("issue"))
    first, last = biblio.get("first_page"), biblio.get("last_page")
    add("pages", f"{first}--{last}" if first and last and first != last else first or last)
    doi = work.get("doi")
    add("doi", doi.removeprefix("https://doi.org/") if doi else None)
    add("url", location.get("landing_page_url") or doi or work.get("id"))
    add("note", "OpenAlex " + work["id"] + "; source type: " + str(work.get("type") or "unknown"))
    return "@" + kind + "{" + key + ",\n" + "\n".join(fields) + "\n}\n"


def write_new(path, text):
    with open(path, "x", encoding="utf-8") as file:
        file.write(text)


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
    manifest = {"source": "OpenAlex", "started_at": datetime.now(timezone.utc).isoformat(),
                "seed_request": seed_url, "pages": [], "complete": False}
    works = {}
    try:
        seed_record = request_json(seed_url)
        write_new(args.workdir / "seed.json", json.dumps(seed_record, ensure_ascii=False, indent=2))
        seed_id = seed_record["id"].rsplit("/", 1)[-1]
        manifest["seed"] = {k: seed_record.get(k) for k in ("id", "doi", "title", "publication_year")}
        page = 1
        cursor = None
        while True:
            params = {"filter": "cites:" + seed_id, "per_page": 100}
            if cursor is None:
                params["page"] = page
            else:
                params["cursor"] = cursor
            url = API + "?" + urlencode(params)
            payload = request_json(url)
            write_new(args.workdir / f"page-{page:04d}.json", json.dumps(payload, ensure_ascii=False, indent=2))
            results = payload["results"]
            total = payload["meta"]["count"]
            manifest["pages"].append({"url": url, "count": len(results), "total_reported": total})
            for work in results:
                works[work["id"]] = work
            if page == 1 and total > 10000:
                if not os.environ.get("OPENALEX_API_KEY"):
                    raise ValueError("More than 10,000 results require cursor paging and OPENALEX_API_KEY.")
                cursor = "*"
                page += 1
                continue
            if cursor is not None:
                next_cursor = payload["meta"].get("next_cursor")
                if not results or not next_cursor:
                    break
                if next_cursor == cursor:
                    raise ValueError("OpenAlex returned a repeated cursor")
                cursor = next_cursor
            elif len(results) < 100 or page * 100 >= total:
                break
            elif page == 100:
                raise ValueError("Basic paging limit reached; results incomplete. A cursor-based export is required.")
            page += 1
        manifest["reported_total"] = total
        manifest["unique_records"] = len(works)
        manifest["complete"] = len(works) == total and len({p["total_reported"] for p in manifest["pages"]}) == 1
        manifest["missing_doi"] = sum(not w.get("doi") for w in works.values())
        manifest["missing_title"] = sum(not w.get("title") for w in works.values())
        manifest["missing_author"] = sum(not w.get("authorships") for w in works.values())
        manifest["missing_year"] = sum(not w.get("publication_year") for w in works.values())
        write_new(args.output, "\n".join(bibtex(work) for work in works.values()))
        manifest["output"] = str(args.output)
        if not manifest["complete"]:
            manifest["warning"] = "Counts differ or changed during paging; results may be incomplete."
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        manifest["error"] = str(error)
    manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
    write_new(args.workdir / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0 if manifest["complete"] else 1


if __name__ == "__main__":
    sys.exit(main())
