"""Search Google Scholar via SerpAPI (https://serpapi.com/google-scholar-api).

Requires `SERPAPI_API_KEY` env var. Without it, the script exits non-zero with
a clear message — by design, we do not ship a fragile scraper.

Usage:
    $env:SERPAPI_API_KEY = "..."
    python tools/search_scholar.py --q "retrieval augmented generation" --max 20 \
        --out projects/<slug>/.cache/scholar-q1.json
"""
from __future__ import annotations

import argparse
import os
import re
import sys

from _common import PaperRecord, emit_records, http_get, normalize_doi, safe_int

SERPAPI = "https://serpapi.com/search.json"


def search(query: str, max_results: int = 20) -> list[PaperRecord]:
    key = os.environ.get("SERPAPI_API_KEY")
    if not key:
        raise RuntimeError(
            "SERPAPI_API_KEY not set. Either set it and retry, or run the search "
            "manually in a browser and add results via tools/catalog.py."
        )
    params = {
        "engine": "google_scholar",
        "q": query,
        "num": min(max_results, 20),
        "api_key": key,
    }
    resp = http_get(SERPAPI, params=params)
    data = resp.json()
    return [_parse(item) for item in (data.get("organic_results") or [])[:max_results]]


_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def _parse(item: dict) -> PaperRecord:
    info = item.get("publication_info") or {}
    summary = info.get("summary") or ""

    year = None
    m = _YEAR_RE.search(summary)
    if m:
        year = safe_int(m.group(0))

    authors = []
    for a in info.get("authors", []) or []:
        name = a.get("name")
        if name:
            authors.append(name)
    if not authors and summary:
        head = summary.split(" - ")[0]
        authors = [s.strip() for s in head.split(",") if s.strip()]

    venue = None
    parts = summary.split(" - ")
    if len(parts) >= 2:
        venue = parts[1].strip()

    pdf_url = None
    for r in item.get("resources", []) or []:
        if (r.get("file_format") or "").upper() == "PDF":
            pdf_url = r.get("link")
            break

    doi = None
    snippet = item.get("snippet") or ""
    doi_m = re.search(r"10\.\d{4,9}/[^\s]+", snippet)
    if doi_m:
        doi = normalize_doi(doi_m.group(0))

    return PaperRecord(
        source="scholar",
        id=str(item.get("result_id") or ""),
        doi=doi,
        title=item.get("title") or "",
        authors=authors,
        year=year,
        venue=venue,
        abstract=snippet,
        url=item.get("link"),
        pdf_url=pdf_url,
        extra={"cited_by": (item.get("inline_links") or {}).get("cited_by", {}).get("total")},
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Search Google Scholar via SerpAPI.")
    p.add_argument("--q", required=True)
    p.add_argument("--max", type=int, default=20)
    p.add_argument("--out")
    args = p.parse_args(argv)
    try:
        records = search(args.q, max_results=args.max)
    except RuntimeError as exc:
        sys.stderr.write(f"{exc}\n")
        return 2
    except Exception as exc:
        sys.stderr.write(f"Scholar search failed: {exc}\n")
        return 1
    emit_records(records, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
