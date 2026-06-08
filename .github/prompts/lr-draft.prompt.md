---
description: Run phase 6 (draft prose + companion BibTeX) for the active project
mode: agent
---

Run [phase 6 — draft](../../agent/workflows/6-draft.md). Step numbering below
mirrors the workflow playbook.

1. Confirm the project slug. Refuse to proceed if `synthesis.md` has not been
   confirmed by the user.
2. Outline the draft first (one section per synthesis theme + intro + gaps).
   Show the outline to the user before writing prose.
3. Write `projects/<slug>/lit-review.md` from
   [agent/templates/lit-review.md](../../agent/templates/lit-review.md). Use
   Pandoc `[@key]` citation syntax. Do not introduce claims absent from
   `synthesis.md`.
4. Respect the target word count from `intake.md` (workflow step 3 / "No new
   claims" rule).
5. Generate `references.bib`:

   ```powershell
   python tools/build_bib.py --project projects/<slug> `
       --only-cited projects/<slug>/lit-review.md `
       --out projects/<slug>/references.bib
   ```

   If the script reports missing keys, fix the draft — do not paper over it by
   adding fake catalog entries.
6. Verify no-fabrication: every `[@key]` in the draft must resolve to a
   catalog entry (`build_bib --only-cited` enforces this; spot-check too).
7. Present `lit-review.md` and `references.bib` for user review. Apply one
   round of edits, then re-run step 5 if any citations changed.
8. After the draft is accepted, build the citation map.
   Write `projects/<slug>/cite-map.md` from
   [agent/templates/cite-map.md](../../agent/templates/cite-map.md): partition
   every catalog entry into "cited in lit-review" vs "deferred to another
   section" (§1 Intro, §3 Methodology, §4 Results, §5 Discussion,
   §6 Program landscape, appendix, figure caption) with a proposed home for
   each deferred row, plus an optional retirement bucket for entries that are
   out-of-scope on closer inspection. Also emit `projects/<slug>/cite-map.bib`
   covering every non-excluded entry:

   ```powershell
   python tools/build_bib.py --project projects/<slug> `
       --out projects/<slug>/cite-map.bib
   ```

   Present the map (and the companion bib's entry count) for user review.
9. If the user confirms any retirements, apply them via
   `tools/catalog.py update --status excluded --exclude-reason "..."` (do not
   hand-edit `catalog.json`). For more than 2–3 keys, wrap in
   `projects/<slug>/.cache/apply_retirements.py`. Re-run
   `tools/catalog.py validate`, `tools/build_bib.py --only-cited` (entry count
   should not change), and regenerate `cite-map.bib` so retirements drop out.
   Mark the retirement bucket in `cite-map.md` `[APPLIED <YYYY-MM-DD>]`. If
   nothing was flagged, skip and record `cite_map_excluded=0`.
10. Close out: append a single delivery entry to `decisions.md`:

    ```
    phase=draft words=<N> citations=<C> bib_entries=<C> cite_map_deferred=<D> cite_map_excluded=<E> status=delivered
    ```

    Add a "Reproduction" footer to `lit-review.md` with the date and the
    `build_bib.py` command needed to regenerate `references.bib`.
