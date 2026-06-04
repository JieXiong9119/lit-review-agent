"""Search arXiv via its Atom API.

Usage:
    python tools/search_arxiv.py --q "retrieval augmented generation" --max 25 \
        --out projects/<slug>/.cache/arxiv-q1.json

Atom API docs: https://info.arxiv.org/help/api/user-manual.html
"""
from __future__ import annotations

import argparse
import sys
from xml.etree import ElementTree as ET

from _common import PaperRecord, emit_records, http_get, normalize_doi, safe_int

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def search(query: str, max_results: int = 25, start: int = 0) -> list[PaperRecord]:
    params = {
        "search_query": f"all:{query}",
        "start": start,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    resp = http_get(ARXIV_API, params=params, headers={"Accept": "application/atom+xml"})
    root = ET.fromstring(resp.text)
    records: list[PaperRecord] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        records.append(_parse_entry(entry))
    return records


def _parse_entry(entry: ET.Element) -> PaperRecord:
    def text(path: str) -> str | None:
        el = entry.find(path, ATOM_NS)
        return el.text.strip() if el is not None and el.text else None

    raw_id = text("atom:id") or ""
    arxiv_id = raw_id.rsplit("/", 1)[-1] if raw_id else None
    if arxiv_id and "v" in arxiv_id:
        arxiv_id = arxiv_id.split("v")[0]

    title = (text("atom:title") or "").replace("\n", " ").strip()
    summary = (text("atom:summary") or "").strip()

    authors = []
    for a in entry.findall("atom:author/atom:name", ATOM_NS):
        if a.text:
            authors.append(a.text.strip())

    published = text("atom:published") or ""
    year = safe_int(published[:4]) if published else None

    doi = normalize_doi(text("arxiv:doi"))
    venue = text("arxiv:journal_ref") or "arXiv preprint"

    pdf_url = None
    for link in entry.findall("atom:link", ATOM_NS):
        if link.get("title") == "pdf":
            pdf_url = link.get("href")
            break
    if not pdf_url and arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    url = raw_id or (f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None)

    return PaperRecord(
        source="arxiv",
        id=arxiv_id,
        doi=doi,
        title=title,
        authors=authors,
        year=year,
        venue=venue,
        abstract=summary,
        url=url,
        pdf_url=pdf_url,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Search arXiv and emit normalized records.")
    p.add_argument("--q", required=True, help="Query string (free text).")
    p.add_argument("--max", type=int, default=25, help="Max results (default 25).")
    p.add_argument("--start", type=int, default=0, help="Result offset (default 0).")
    p.add_argument("--out", help="Output JSON path. Omit to print to stdout.")
    args = p.parse_args(argv)
    try:
        records = search(args.q, max_results=args.max, start=args.start)
    except Exception as exc:
        sys.stderr.write(f"arXiv search failed: {exc}\n")
        return 1
    emit_records(records, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
