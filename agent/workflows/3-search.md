# Phase 3 — Search

**Goal.** For each sub-question from `intake.md`, run targeted searches against the
literature backends, collect candidate papers, and record exactly what was searched
for reproducibility.

**Inputs required.**
- `intake.md` (sub-questions, scope, inclusion/exclusion criteria).
- `existing-work.md` (so you don't re-list what the project already cites).

**Output.** Raw hits appended to `projects/<slug>/decisions.md`, ready for phase 4
to filter and acquire. No `catalog.json` writes happen yet — that is phase 4's job.

---

## Backends

All backend scripts live in [tools/](../../tools/) and emit a common normalized JSON
schema (one record per paper: `source`, `id`, `doi`, `title`, `authors`, `year`,
`venue`, `abstract`, `url`, `pdf_url`). Prefer free, keyless APIs first.

| Order | Backend | Script | Key required |
|---|---|---|---|
| 1 | arXiv | [tools/search_arxiv.py](../../tools/search_arxiv.py) | no |
| 2 | OpenAlex | [tools/search_openalex.py](../../tools/search_openalex.py) | no |
| 3 | Semantic Scholar | [tools/search_semantic_scholar.py](../../tools/search_semantic_scholar.py) | optional (`SEMANTIC_SCHOLAR_API_KEY`) |
| 4 | CrossRef (mainly enrichment, also search) | [tools/search_crossref.py](../../tools/search_crossref.py) | no |
| 5 | Google Scholar (fallback) | [tools/search_scholar.py](../../tools/search_scholar.py) | requires `SERPAPI_API_KEY` |
| 6 | Generic web fetch | use the chat tool's built-in `fetch_webpage` / MCP | n/a |

Skip a backend if its key is missing — log the skip, do not block.

---

## Steps

1. **Plan queries.** For each sub-question, draft 2–4 query strings. A good query:
   - Uses concrete technical terms over generic ones.
   - Combines a method term with a domain/task term (e.g.,
     `"retrieval augmented generation" scientific QA`).
   - Has at least one variant that swaps method-side and domain-side terms.

   Show the plan to the user before executing. They will often catch missing terms.

2. **Execute, one backend at a time.** From the repo root in a terminal:

   ```powershell
   python tools/search_arxiv.py --q "retrieval augmented generation scientific qa" `
       --max 25 --out projects/<slug>/.cache/arxiv-q1.json
   ```

   Cache raw output under `projects/<slug>/.cache/` (gitignored). Do not paste large
   raw JSON into chat — read it from disk when you need it.

3. **Per-backend pass.** After each backend run, append a compact summary to
   `decisions.md`:

   ```
   phase=search backend=arxiv query="..." n_hits=25 cached=.cache/arxiv-q1.json
   ```

4. **Backward & forward citation hops** (light touch, only for the most promising
   3–5 seeds or anything the user flagged in intake step 9):

   - Backward: pull the paper's references via OpenAlex or Semantic Scholar.
   - Forward: pull citers via the same.
   - Cache and log identically.

5. **Stop conditions.** Stop searching when *any* holds:
   - The last two query variants returned mostly duplicates of papers you've already
     seen.
   - You have ≥3× the target citation count from intake step 7 (gives phase 4 room
     to filter aggressively).
   - The user says stop.

   Searching forever is a failure mode. Bias toward stopping early and letting
   phase 4 pull more if needed.

---

## Hand-off to phase 4

You may proceed to [4-acquire-index.md](4-acquire-index.md) once:

- [ ] Every sub-question has at least one backend's results cached.
- [ ] `decisions.md` lists every query that was run, including ones with zero hits.
- [ ] You have a rough count of unique candidates (after eyeballing for obvious
      duplicates) and have shared it with the user.
