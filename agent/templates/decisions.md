# Decisions log — `<project slug>`

> Chronological audit trail. Append-only. Every phase writes at least one entry.
> Format: free-form prose under dated headings; structured one-liners welcome.

## <YYYY-MM-DD> — phase 1 (intake)

phase=intake status=complete summary=<one line>

<Optional notes.>

## <YYYY-MM-DD> — phase 2 (existing-work)

phase=existing-work mode=A source=<path> found="N papers, M gap claims"

<Optional notes.>

## <YYYY-MM-DD> — phase 3 (search)

phase=search backend=arxiv query="..." n_hits=25 cached=.cache/arxiv-q1.json
phase=search backend=openalex query="..." n_hits=18 cached=.cache/openalex-q1.json
phase=search backend=semantic_scholar status=skipped reason="no API key"
...

## <YYYY-MM-DD> — phase 4 (acquire-index)

phase=acquire-index n_candidates=43 n_included=22 n_excluded=18 n_deferred=3 \
    n_summarized=20 n_metadata_only=2

Excluded:
- `keyX` — <exclude_reason>
- `keyY` — <exclude_reason>
- ...

## <YYYY-MM-DD> — phase 5 (synthesize)

phase=synthesize n_themes=4 n_conflicts=2 n_gaps=3 matrix_rows=22

## <YYYY-MM-DD> — phase 6 (draft)

phase=draft words=1180 citations=22 bib_entries=22 status=delivered
