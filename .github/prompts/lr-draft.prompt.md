---
description: Run phase 6 (draft prose + companion BibTeX) for the active project
mode: agent
---

Run [phase 6 — draft](../../agent/workflows/6-draft.md).

1. Confirm the project slug. Refuse to proceed if `synthesis.md` has not been
   confirmed by the user.
2. Outline the draft first (one section per synthesis theme + intro + gaps).
   Show the outline to the user before writing prose.
3. Write `projects/<slug>/lit-review.md` from
   [agent/templates/lit-review.md](../../agent/templates/lit-review.md). Use
   Pandoc `[@key]` citation syntax. Do not introduce claims absent from
   `synthesis.md`.
4. Generate `references.bib`:

   ```powershell
   python tools/build_bib.py --project projects/<slug> `
       --only-cited projects/<slug>/lit-review.md `
       --out projects/<slug>/references.bib
   ```

   If the script reports missing keys, fix the draft — do not paper over it by
   adding fake catalog entries.
5. Append a `phase=draft … status=delivered` entry to `decisions.md`.
6. Present `lit-review.md` and `references.bib` for user review.
7. After the draft is accepted, build the citation map.
   Write `projects/<slug>/cite-map.md` from
   [agent/templates/cite-map.md](../../agent/templates/cite-map.md): partition
   every catalog entry into "cited in lit-review" vs "deferred to another
   section" (§1 Intro, §3 Methodology, §4 Results, §5 Discussion,
   §6 Program landscape, appendix, figure caption) with a proposed home for
   each deferred row, plus an optional retirement bucket for entries that are
   out-of-scope on closer inspection. Present the map for user review.
8. If the user confirms any retirements, apply them via
   `tools/catalog.py update --status excluded --exclude-reason "..."` (do not
   hand-edit `catalog.json`). For more than 2–3 keys, wrap in
   `projects/<slug>/.cache/apply_retirements.py`. Re-run
   `tools/catalog.py validate` and `tools/build_bib.py --only-cited`.
9. Re-append the `decisions.md` entry to include `cite_map_deferred=<D>`
   and `cite_map_excluded=<E>`.
