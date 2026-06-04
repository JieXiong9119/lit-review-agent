"""Search Semantic Scholar (https://api.semanticscholar.org/) for papers.

Usage:
    python tools/search_semantic_scholar.py --q "retrieval augmented generation" \
        --max 25 --out projects/<slug>/.cache/ss-q1.json

Optional: set SEMANTIC_SCHOLAR_API_KEY for higher rate limits.
"""
from __future__ import annotations

import argparse
import os
import sys

from _common import PaperRecord, emit_records, http_get, normalize_doi, safe_int

S2_API = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = (
    "paperId,externalIds,title,abstract,authors,year,venue,"
    "openAccessPdf,url"
)


def search(query: str, max_results: int = 25, offset: int = 0) -> list[PaperRecord]:
    params = {
        "query": query,
        "limit": min(max_results, 100),
        "offset": offset,
        "fields": S2_FIELDS,
    }
    headers: dict[str, str] = {}
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    if key:
        headers["x-api-key"] = key
    resp = http_get(S2_API, params=params, headers=headers)
    data = resp.json()
    records: list[PaperRecord] = []
    for paper in (data.get("data") or [])[:max_results]:
        records.append(_parse_paper(paper))
    return records


def _parse_paper(paper: dict) -> PaperRecord:
    ext = paper.get("externalIds") or {}
    doi = normalize_doi(ext.get("DOI"))
    arxiv_id = ext.get("ArXiv")

    authors = [a.get("name") for a in (paper.get("authors") or []) if a.get("name")]

    oa = paper.get("openAccessPdf") or {}
    pdf_url = oa.get("url")

    return PaperRecord(
        source="semantic_scholar",
        id=paper.get("paperId"),
        doi=doi,
        title=paper.get("title") or "",
        authors=authors,
        year=safe_int(paper.get("year")),
        venue=paper.get("venue"),
        abstract=paper.get("abstract"),
        url=paper.get("url"),
        pdf_url=pdf_url,
        extra={"arxiv_id": arxiv_id} if arxiv_id else {},
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Search Semantic Scholar.")
    p.add_argument("--q", required=True)
    p.add_argument("--max", type=int, default=25)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--out")
    args = p.parse_args(argv)
    try:
        records = search(args.q, max_results=args.max, offset=args.offset)
    except Exception as exc:
        sys.stderr.write(f"Semantic Scholar search failed: {exc}\n")
        return 1
    emit_records(records, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
