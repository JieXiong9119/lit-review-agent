---
description: Run phase 2 (existing-work scan) + phase 3 (search) for the active project
mode: agent
---

Run [phase 2 — existing-work scan](../../agent/workflows/2-existing-work.md) and
then [phase 3 — search](../../agent/workflows/3-search.md).

1. Confirm which project slug to operate on. Read `projects/<slug>/intake.md`
   first; do not proceed without it.
2. Phase 2: ask whether to use a local repo path or a pasted summary, then write
   `projects/<slug>/existing-work.md`.
3. Phase 3: draft a query plan from the sub-questions, show it to the user,
   then run the relevant `tools/search_*.py` scripts in a terminal. Cache results
   under `projects/<slug>/.cache/`.
4. Append a per-query entry to `projects/<slug>/decisions.md`.
5. Stop per the stop conditions in the search playbook; report unique candidate
   count to the user.
