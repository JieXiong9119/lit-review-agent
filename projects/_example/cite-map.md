# Citation map — `_example`

> Generated in phase 6, step 8. Purpose: partition every prior-art reference
> in `catalog.json` into (a) cited in `lit-review.md`, (b) deferred to other
> sections of the user's paper, (c) flagged for retirement to `status: excluded`.
>
> See [agent/templates/cite-map.md](../../agent/templates/cite-map.md) for the
> full template with all suggested buckets and the apply-retirements workflow.
>
> **Note for new users.** This example project is intentionally tiny (3 entries,
> all cited in `lit-review.md`), so the cite-map below is the simplest possible
> case. A realistic project will have many more entries distributed across
> Buckets 1–8 plus a retirement bucket; see
> [projects/df-commercial-stock/cite-map.md](../df-commercial-stock/cite-map.md)
> (if available in your workspace) for a worked example.

---

## Counts at draft time (2026-06-04)

- Catalog entries total: 3
- Cited in `lit-review.md`: 3
- Deferred to other sections: 0
- Excluded (status `excluded` in catalog): 0

`3 + 0 + 0 = 3` ✓

---

## Bucket 7 — Already cited in `lit-review.md` (no action)

| Key | Where it appears in `lit-review.md` |
|---|---|
| `gao2023ragsurvey` | §2.1 framing of RAG taxonomy; §2.2 retrieval-stage discussion |
| `jiang2023active` | §2.2 active-retrieval description; §2.4 outlook |
| `chen2024rgb` | §2.3 RGB benchmark; §2.4 generator-side weakness discussion |

## Bucket 8 — Out-of-scope retirements (apply via `tools/catalog.py update`)

*None for this example.* In a real project, list each retired key with a
one-line `exclude_reason`, then apply with:

```powershell
python tools/catalog.py update --project projects/<slug> `
    --key <key> `
    --status excluded `
    --exclude-reason "<reason>"
```

For more than 2–3 keys, wrap the calls in
`projects/<slug>/.cache/apply_retirements.py`. After apply, re-run
`tools/catalog.py validate` and `tools/build_bib.py --only-cited`, and mark
this bucket heading `[APPLIED <YYYY-MM-DD>]`.

---

## Checklist for non-§2 section writers

For larger projects, deferred rows in Buckets 1–6 should be walked through
when each non-§2 section is drafted; mark each `[cited in §<N>]`,
`[moved to §<N>]`, or `[dropped: <reason>]`. This example has no deferred
rows, so the checklist is empty.
