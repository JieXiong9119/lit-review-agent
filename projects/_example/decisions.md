# Decisions log — `_example`

## 2026-06-04 — phase 1 (intake)
phase=intake status=complete summary="3-paper example on RAG and hallucination, 2023–2024."

## 2026-06-04 — phase 2 (existing-work)
phase=existing-work mode=B source="user summary" found="1 paper, 1 gap claim"

## 2026-06-04 — phase 3 (search)
phase=search backend=openalex query="retrieval augmented generation" n_hits=3 cached=.cache/openalex-rag.json
phase=search backend=arxiv status=skipped reason="rate-limited during smoke test; OpenAlex covered the same papers"
phase=search backend=crossref status=skipped reason="not needed; OpenAlex returned DOIs"

## 2026-06-04 — phase 4 (acquire-index)
phase=acquire-index n_candidates=3 n_included=3 n_excluded=0 n_deferred=0 n_summarized=0 n_metadata_only=3

All three example entries are intentionally `metadata-only` because the example
ships abstracts rather than full PDFs (per the agent's gitignore policy, PDFs
are only committed inside `_example/`, and even there we kept it abstract-only
to avoid bundling third-party PDFs in the repo).

## 2026-06-04 — phase 5 (synthesize)
phase=synthesize n_themes=3 n_conflicts=0 n_gaps=2 matrix_rows=3

## 2026-06-04 — phase 6 (draft)
phase=draft words=330 citations=3 bib_entries=3 status=delivered
