"""Search OpenAlex (https://docs.openalex.org/) for works.

Usage:
    python tools/search_openalex.py --q "retrieval augmented generation" --max 25 \
        --out projects/<slug>/.cache/openalex-q1.json

Set OPENALEX_EMAIL env var to enter the "polite pool" with better rate limits.
"""
from __future__ import annotations

import argparse
import os
import sys

from _common import PaperRecord, emit_records, http_get, normalize_doi, safe_int

OPENALEX_API = "https://api.openalex.org/works"


def search(query: str, max_results: int = 25) -> list[PaperRecord]:
    params = {
        "search": query,
        "per-page": min(max_results, 200),
    }
    email = os.environ.get("OPENALEX_EMAIL")
    if email:
        params["mailto"] = email
    resp = http_get(OPENALEX_API, params=params)
    data = resp.json()
    records: list[PaperRecord] = []
    for work in data.get("results", [])[:max_results]:
        records.append(_parse_work(work))
    return records


def _parse_work(work: dict) -> PaperRecord:
    authors = []
    for a in work.get("authorships", []) or []:
        name = (a.get("author") or {}).get("display_name")
        if name:
            authors.append(name)

    venue = None
    pl = work.get("primary_location") or {}
    src = pl.get("source") or {}
    if src.get("display_name"):
        venue = src["display_name"]

    pdf_url = pl.get("pdf_url")
    if not pdf_url:
        for loc in work.get("locations", []) or []:
            if loc.get("pdf_url"):
                pdf_url = loc["pdf_url"]
                break

    abstract = None
    inv = work.get("abstract_inverted_index")
    if isinstance(inv, dict):
        abstract = _reconstruct_abstract(inv)

    return PaperRecord(
        source="openalex",
        id=work.get("id"),
        doi=normalize_doi(work.get("doi")),
        title=work.get("title") or work.get("display_name") or "",
        authors=authors,
        year=safe_int(work.get("publication_year")),
        venue=venue,
        abstract=abstract,
        url=work.get("id"),
        pdf_url=pdf_url,
        extra={"cited_by_count": work.get("cited_by_count")},
    )


def _reconstruct_abstract(inv: dict) -> str:
    """OpenAlex returns an inverted index {word: [positions]}; rebuild the text."""
    positions: dict[int, str] = {}
    for word, idxs in inv.items():
        for i in idxs:
            positions[i] = word
    if not positions:
        return ""
    ordered = [positions[i] for i in sorted(positions) if i in positions]
    return " ".join(ordered)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Search OpenAlex and emit normalized records.")
    p.add_argument("--q", required=True)
    p.add_argument("--max", type=int, default=25)
    p.add_argument("--out")
    args = p.parse_args(argv)
    try:
        records = search(args.q, max_results=args.max)
    except Exception as exc:
        sys.stderr.write(f"OpenAlex search failed: {exc}\n")
        return 1
    emit_records(records, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
