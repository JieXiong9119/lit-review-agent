# Phase 4 — Acquire & index

**Goal.** Take the raw search hits from phase 3, filter them against the
inclusion/exclusion criteria, download the survivors, summarize each, and register
everything in a queryable catalog.

**Inputs required.**
- Cached raw search results under `projects/<slug>/.cache/*.json`.
- `intake.md` (inclusion/exclusion criteria, citation key convention, target count).
- `existing-work.md` (so pre-cited works are also added to the catalog).

**Outputs.**
- `projects/<slug>/catalog.json` (schema:
  [agent/templates/catalog.schema.json](../templates/catalog.schema.json)).
- `projects/<slug>/papers/<key>.md` per included paper (template:
  [agent/templates/paper-summary.md](../templates/paper-summary.md)).
- Optional `projects/<slug>/papers/<key>.pdf` — local copy, gitignored.

---

## Steps

1. **Dedupe.** Load every cached JSON, merge into one in-memory list, deduplicate by
   DOI → arXiv id → (lowercased title + year). Use
   [tools/catalog.py](../../tools/catalog.py) `dedupe` mode if it helps; otherwise
   do it inline.

2. **Apply filters.** Walk the deduped list and decide `include` / `exclude` /
   `defer` for each, against the criteria in `intake.md`. Be strict — phase 5 is
   much easier with 20 high-fit papers than 60 mediocre ones.

   For every decision, prepare an `include_reason` or `exclude_reason` string. The
   user must be able to audit your judgement.

3. **Seed pre-existing citations.** Add every entry from `existing-work.md`'s
   already-cited list to the catalog with `status: pre-existing` so phase 6 can
   integrate them coherently.

4. **Mint citation keys.** Use the convention from intake step 8 (default
   `authorYearShorttitle`, e.g., `lewis2020rag`). Lowercase, ASCII-only, no spaces.
   On collision, append `a`, `b`, ….

5. **Register in catalog.** For each `include`d paper, run:

   ```powershell
   python tools/catalog.py add `
       --project projects/<slug> `
       --key lewis2020rag `
       --from-json projects/<slug>/.cache/arxiv-q1.json `
       --match-doi 10.48550/arXiv.2005.11401 `
       --status pending `
       --include-reason "Foundational RAG architecture; cited by seed list."
   ```

   The script writes/updates `catalog.json` atomically.

6. **Download PDFs** (for `include`d, open-access papers only):

   ```powershell
   python tools/fetch_pdf.py --key lewis2020rag --project projects/<slug>
   ```

   If a PDF is paywalled or fetch fails, set the catalog entry's `status` to
   `metadata-only` and continue. Never fabricate content for a paper you cannot
   read.

7. **Extract text.** For each downloaded PDF:

   ```powershell
   python tools/pdf_to_text.py --key lewis2020rag --project projects/<slug>
   ```

   Writes `projects/<slug>/papers/.text/<key>.txt` (gitignored). You'll read from
   this when summarizing.

8. **Summarize each paper.** For each `include`d paper with text available, copy
   [agent/templates/paper-summary.md](../templates/paper-summary.md) to
   `projects/<slug>/papers/<key>.md` and fill it in using
   [agent/rubrics/paper-summary-rubric.md](../rubrics/paper-summary-rubric.md).
   Update the catalog entry's `status` to `summarized` and `summary_path` to the
   relative path.

   For `metadata-only` papers, write a short summary based purely on the abstract
   and mark it as such at the top of the file.

9. **Log.** Append to `decisions.md`:

   ```
   phase=acquire-index n_candidates=<N> n_included=<I> n_excluded=<X> `
       n_deferred=<D> n_summarized=<S> n_metadata_only=<M>
   ```

   Then list excluded papers with their `exclude_reason` (one per line). Auditability
   matters more than brevity here.

---

## Hand-off to phase 5

You may proceed to [5-synthesize.md](5-synthesize.md) once:

- [ ] `catalog.json` validates against `catalog.schema.json`.
- [ ] Every `include`d catalog entry has either `status: summarized` or
      `status: metadata-only` — no `pending` left.
- [ ] The exclusion list in `decisions.md` has been shown to the user and they have
      not asked to reinstate anything.
