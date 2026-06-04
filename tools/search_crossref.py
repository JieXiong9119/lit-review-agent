"""Query CrossRef (https://api.crossref.org/) for works.

Two modes:

1. Free-text search:
       python tools/search_crossref.py --q "retrieval augmented generation" --max 25
2. Single-DOI metadata enrichment:
       python tools/search_crossref.py --doi 10.48550/arXiv.2005.11401
"""
from __future__ import annotations

import argparse
import os
import sys

from _common import PaperRecord, emit_records, http_get, normalize_doi, safe_int

CROSSREF_WORKS = "https://api.crossref.org/works"


def search(query: str, max_results: int = 25) -> list[PaperRecord]:
    params = {"query": query, "rows": min(max_results, 100)}
    email = os.environ.get("CROSSREF_EMAIL")
    if email:
        params["mailto"] = email
    resp = http_get(CROSSREF_WORKS, params=params)
    items = (resp.json().get("message") or {}).get("items") or []
    return [_parse_item(item) for item in items[:max_results]]


def fetch_doi(doi: str) -> PaperRecord | None:
    doi_norm = normalize_doi(doi)
    if not doi_norm:
        return None
    resp = http_get(f"{CROSSREF_WORKS}/{doi_norm}")
    msg = (resp.json() or {}).get("message")
    return _parse_item(msg) if msg else None


def _parse_item(item: dict) -> PaperRecord:
    title_list = item.get("title") or []
    title = title_list[0] if title_list else ""

    authors = []
    for a in item.get("author", []) or []:
        given = a.get("given", "")
        family = a.get("family", "")
        name = f"{family}, {given}".strip(", ")
        if name:
            authors.append(name)

    year = None
    issued = item.get("issued") or {}
    date_parts = issued.get("date-parts") or [[]]
    if date_parts and date_parts[0]:
        year = safe_int(date_parts[0][0])

    venue = None
    for k in ("container-title", "publisher"):
        v = item.get(k)
        if isinstance(v, list) and v:
            venue = v[0]
            break
        if isinstance(v, str) and v:
            venue = v
            break

    pdf_url = None
    for link in item.get("link", []) or []:
        if link.get("content-type", "").startswith("application/pdf"):
            pdf_url = link.get("URL")
            break

    return PaperRecord(
        source="crossref",
        id=item.get("DOI"),
        doi=normalize_doi(item.get("DOI")),
        title=title,
        authors=authors,
        year=year,
        venue=venue,
        abstract=item.get("abstract"),  # may contain JATS XML tags
        url=item.get("URL"),
        pdf_url=pdf_url,
        extra={"type": item.get("type")},
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Search CrossRef or fetch by DOI.")
    p.add_argument("--q", help="Free-text search query.")
    p.add_argument("--doi", help="Fetch metadata for a single DOI.")
    p.add_argument("--max", type=int, default=25)
    p.add_argument("--out")
    args = p.parse_args(argv)

    if not args.q and not args.doi:
        p.error("Provide either --q or --doi.")

    try:
        if args.doi:
            rec = fetch_doi(args.doi)
            records = [rec] if rec else []
        else:
            records = search(args.q, max_results=args.max)
    except Exception as exc:
        sys.stderr.write(f"CrossRef call failed: {exc}\n")
        return 1
    emit_records(records, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
