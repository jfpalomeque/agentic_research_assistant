#!/usr/bin/env python3
"""Search Crossref or retrieve a DOI as compact JSON, without dependencies."""

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

API = "https://api.crossref.org/works"


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_endtag(self, tag):
        if tag.split(":")[-1] in ("p", "title", "sec", "abstract", "br"):
            self.parts.append(" ")


def plain_text(value):
    if not value:
        return None
    parser = TextExtractor()
    parser.feed(value)
    return re.sub(r"\s+", " ", "".join(parser.parts)).strip()


def normalize_doi(value):
    value = value.strip()
    if value.lower().startswith("doi:"):
        value = value[4:].strip()
    if value.lower().startswith(("https://", "http://")):
        url = urlsplit(value)
        if url.hostname not in ("doi.org", "dx.doi.org") or url.query or url.fragment:
            raise ValueError("Expected a DOI or a doi.org URL without query or fragment")
        from urllib.parse import unquote
        value = unquote(url.path.lstrip("/"))
    if not re.match(r"^10\.\d{4,9}/\S+$", value, re.IGNORECASE):
        raise ValueError("Expected a DOI such as 10.1007/s10816-022-09559-5")
    return value


def compact(item, full=False):
    authors = []
    for author in item.get("author", []):
        name = author.get("name") or " ".join(filter(None, (author.get("given"), author.get("family"))))
        if name:
            authors.append(name)
    result = {
        "doi": item.get("DOI"), "title": (item.get("title") or [None])[0],
        "authors": authors, "issued": item.get("issued", {}).get("date-parts"),
        "container": (item.get("container-title") or [None])[0],
        "type": item.get("type"), "url": item.get("URL"),
    }
    if full:
        result.update({
            "publisher": item.get("publisher"), "volume": item.get("volume"),
            "issue": item.get("issue"), "pages": item.get("page"),
            "article_number": item.get("article-number"), "issn": item.get("ISSN"),
            "published_print": item.get("published-print", {}).get("date-parts"),
            "published_online": item.get("published-online", {}).get("date-parts"),
            "abstract": plain_text(item.get("abstract")),
            "update_to": item.get("update-to"), "relation": item.get("relation"),
        })
    return result


def fetch(url):
    headers = {"User-Agent": "ARA-literature-lookup/1.0"}
    email = os.environ.get("CROSSREF_MAILTO", "").strip()
    if email:
        headers["User-Agent"] += f" (mailto:{email})"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def year(value):
    try:
        number = int(value)
        if not 1 <= number <= 9999:
            raise ValueError
        return number
    except ValueError:
        raise argparse.ArgumentTypeError("year must be between 1 and 9999")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    get = commands.add_parser("get", help="Look up a DOI or doi.org URL")
    get.add_argument("doi")
    search = commands.add_parser("search", help="Find candidate records")
    search.add_argument("--author", help="Author name (not an exact filter)")
    search.add_argument("--query", help="Title, topic or bibliographic clues")
    search.add_argument("--year", type=year, help="Filter by publication year")
    search.add_argument("--limit", type=int, default=5, help="Maximum candidates, 1–20 (default 5)")
    args = parser.parse_args(argv)
    try:
        if args.command == "get":
            doi = normalize_doi(args.doi)
            url = API + "/" + quote(doi, safe="")
            payload = fetch(url)
            result = {"record": compact(payload["message"], full=True)}
        else:
            if not args.author and not args.query:
                parser.error("search requires --author and/or --query")
            if not 1 <= args.limit <= 20:
                parser.error("--limit must be between 1 and 20")
            params = {"rows": args.limit}
            if args.author:
                params["query.author"] = args.author
            if args.query:
                params["query.bibliographic"] = args.query
            if args.year:
                params["filter"] = f"from-pub-date:{args.year:04d}-01-01,until-pub-date:{args.year:04d}-12-31"
            url = API + "?" + urlencode(params)
            message = fetch(url)["message"]
            items = message.get("items", [])
            result = {"total_results": message.get("total-results"), "returned": len(items),
                      "candidates": [compact(item) for item in items]}
        result["source"] = {"provider": "Crossref", "request_url": url,
                            "retrieved_at": datetime.now(timezone.utc).isoformat()}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Crossref lookup failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
