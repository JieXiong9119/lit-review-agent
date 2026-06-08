# Tools

Small, single-purpose Python helpers that the agent invokes during the literature
review workflow. Each script reads CLI args, hits an API or processes a file, and
emits JSON. No global state; no installed CLI; no framework.

## Install

```powershell
pip install -r tools/requirements.txt
```

Only two third-party deps: `requests` and `pypdf`.

## Optional environment variables

| Var | Purpose |
|---|---|
| `OPENALEX_EMAIL` | Enter OpenAlex's "polite pool" — higher rate limits. |
| `CROSSREF_EMAIL` | Same idea for CrossRef. |
| `SEMANTIC_SCHOLAR_API_KEY` | Higher S2 rate limits. |
| `SERPAPI_API_KEY` | Required for `search_scholar.py`. |

## The common record schema

Every `search_*.py` emits a JSON list of records with these fields:

```jsonc
{
  "source": "arxiv|openalex|semantic_scholar|crossref|scholar|user",
  "id": "backend-native id",       // arXiv id, OpenAlex W..., S2 paperId, DOI for crossref
  "doi": "lowercased doi or null",
  "title": "...",
  "authors": ["Last, First", ...],
  "year": 2020,
  "venue": "Conference / journal name or 'arXiv preprint' or null",
  "abstract": "...",
  "url": "canonical URL",
  "pdf_url": "open-access PDF URL or null",
  "extra": { ... backend-specific extras ... }
}
```

## Scripts

| Script | What it does |
|---|---|
| `search_arxiv.py` | arXiv Atom API. |
| `search_openalex.py` | OpenAlex Works endpoint. Reconstructs abstract from the inverted index. |
| `search_semantic_scholar.py` | Semantic Scholar graph search. |
| `search_crossref.py` | CrossRef. Supports both query and `--doi` single-record fetch. |
| `search_scholar.py` | Google Scholar via SerpAPI (requires key). |
| `fetch_pdf.py` | Download a PDF by catalog key (uses `catalog.json`) or direct URL. |
| `pdf_to_text.py` | Extract text from a PDF. Auto-selects the best available backend (PyMuPDF → pdfplumber → pypdf); force one with `--backend`. |
| `catalog.py` | `init / add / update / list / get / dedupe / validate` over `catalog.json`. Use `update` (not hand-edits) to change fields on an existing entry — e.g. mark a phase-6 cite-map retirement as `--status excluded --exclude-reason "..."`. |
| `build_bib.py` | Render `references.bib` from `catalog.json`; with `--only-cited`, only the keys that appear in a draft. Always drops entries with `status: excluded` so retirements never leak into the bib. |

## Conventions

- Every script accepts `--out` to write JSON to a path; without it, prints to stdout.
- Scripts write progress / errors to stderr, never to stdout, so stdout JSON is
  always pipeable.
- Network scripts honor `User-Agent: lit-review-agent/0.1` and a 30-second
  timeout, and never retry silently — failures bubble up so the agent can decide.
- Catalog writes are atomic (write temp file → `os.replace`).

## PDF extraction backends

`pdf_to_text.py` supports three backends and picks the first that imports
successfully (in this order):

| Backend | Why use it | License | Strength |
|---|---|---|---|
| `pymupdf` (`fitz`) | Default when installed. | AGPL | Best reading-order recovery for two-column scientific PDFs; fast. |
| `pdfplumber` | MIT alternative. | MIT | Decent layout, table-aware. |
| `pypdf` | Guaranteed fallback. | BSD-3 | Simple, but often scrambles two-column layouts. |

Force a specific backend with `--backend pymupdf|pdfplumber|pypdf`. The
script prints which backend it used to stderr so the choice is auditable.

If you want to stay MIT-only, remove `pymupdf` from `requirements.txt`,
uncomment `pdfplumber`, and re-install.

## Smoke test

```powershell
# Verify arXiv search works
python tools/search_arxiv.py --q "retrieval augmented generation" --max 3

# Round-trip: init catalog, add an entry from search, list it, render bib
python tools/catalog.py init --project projects/_smoketest
python tools/search_arxiv.py --q "lewis 2020 retrieval-augmented generation" --max 5 `
    --out projects/_smoketest/.cache/arxiv.json
python tools/catalog.py add --project projects/_smoketest --key lewis2020rag `
    --from-json projects/_smoketest/.cache/arxiv.json `
    --match-title "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" `
    --status summarized --tags retrieval rag
python tools/catalog.py list --project projects/_smoketest

# Retire an entry (mark as excluded with a reason)
python tools/catalog.py update --project projects/_smoketest --key lewis2020rag `
    --status excluded --exclude-reason "out of scope for smoketest demo"
python tools/catalog.py validate --project projects/_smoketest

python tools/build_bib.py --project projects/_smoketest --out projects/_smoketest/references.bib
```

Delete `projects/_smoketest/` when done.
