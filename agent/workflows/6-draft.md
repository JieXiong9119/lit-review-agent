# Phase 6 — Draft

**Goal.** Produce a prose literature-review section the user can drop into a paper
or thesis, accompanied by a clean BibTeX file. Every citation must trace back to
an entry in `catalog.json`.

**Inputs required.**
- A confirmed `synthesis.md` (themes, matrix, conflicts, gaps, all with key
  citations).
- `catalog.json` with every cited key present.
- `intake.md` (target word count, primary question — the draft should answer it).

**Outputs.**
- `projects/<slug>/lit-review.md` (template:
  [agent/templates/lit-review.md](../templates/lit-review.md)).
- `projects/<slug>/references.bib` (generated, not hand-edited).
- `projects/<slug>/cite-map.md` (template:
  [agent/templates/cite-map.md](../templates/cite-map.md)) — partitions every
  catalog entry into "cited in lit-review" vs "deferred to another section of
  the user's paper," with a proposed home for each deferred entry. Prevents
  silent abandonment of catalogued literature that does not fit the §2
  Related-Work narrative.

---

## Steps

1. **Outline first, prose second.** Convert each synthesis theme into one section
   heading. Add an introduction (problem + scope) and a closing "gaps and outlook"
   section that points to the project's contribution. Show the outline to the user
   before writing prose.

2. **Write theme sections.** For each:
   - Open with a one-sentence claim that captures the theme.
   - Walk through 3–6 papers that support, complicate, or contradict it.
   - Use the comparison matrix from `synthesis.md` if a table reads better than
     prose for a given subtopic.
   - Cite as `[@key]` inline (Pandoc-style). Phase 6's BibTeX step assumes this.

3. **Respect the target length.** From intake step 7. Drafts that overshoot tend to
   lose focus — prefer cutting weak paragraphs over padding to a target.

4. **No new claims.** Every assertion in the draft must already appear (with
   citations) in `synthesis.md`. If you find yourself wanting to add something
   new, stop and update `synthesis.md` first.

5. **Generate `references.bib`.** From the repo root:

   ```powershell
   python tools/build_bib.py --project projects/<slug> `
       --only-cited lit-review.md `
       --out projects/<slug>/references.bib
   ```

   `--only-cited` reads the draft, extracts every `[@key]`, and emits only those
   BibTeX entries. This keeps the bib lean and catches missing-key errors.

6. **Verify no-fabrication.** Run a sanity check (the script does this, but verify
   manually too): grep every `[@...]` in `lit-review.md`, confirm each key exists
   in `catalog.json`. If any key is missing, the draft is wrong, not the catalog —
   fix the draft.

7. **Final review with user.** Present `lit-review.md` and `references.bib`. Ask
   for one round of feedback. Apply edits. Re-run step 5 if any citations were
   added or removed.

8. **Build the citation map.** Many catalogued papers belong in *other*
   sections of the user's paper (methodology, results, discussion, program
   landscape, data-source caption notes). Write
   `projects/<slug>/cite-map.md` from
   [agent/templates/cite-map.md](../templates/cite-map.md). Partition every
   catalog entry into:
   - **cited in `lit-review.md`** (the §2 Related-Work narrative);
   - **deferred to another section** with a proposed home (§1 Intro,
     §3 Methodology, §4 Results, §5 Discussion, §6 Program landscape,
     appendix, figure caption); record the rationale in one short line.

   Use the bucket structure in the template, but rename/merge buckets to fit
   the project (e.g., a pure-software-engineering project may not need a
   regulatory bucket). The goal is that every prior-art or newly-included
   entry has a named destination, so the user's methodology / results /
   discussion writers start from a checklist instead of re-deriving the
   partition.

   Validation: every key in `cite-map.md` should appear in `catalog.json`;
   the union of "cited in lit-review" + "deferred" + `status=excluded` keys
   should equal the catalog total.

9. **Apply any flagged retirements.** If step 8 surfaced entries that are
   out-of-scope on closer inspection (the cite-map template's retirement
   bucket — typically the last bucket), apply them to `catalog.json` via
   the sanctioned tool path. Do **not** hand-edit `catalog.json`.

   ```powershell
   python tools/catalog.py update --project projects/<slug> `
       --key <key> `
       --status excluded `
       --exclude-reason "<one-line reason>"
   ```

   For more than two or three keys, wrap the calls in a one-shot helper
   under `projects/<slug>/.cache/apply_retirements.py` (project-local, per
   AGENTS.md §8). After apply:

   - Re-run `python tools/catalog.py validate --project projects/<slug>`.
   - Re-run the `build_bib.py --only-cited` command from step 5 and confirm
     the bib entry count is unchanged (retired keys should not be cited).
   - Update the retirement bucket in `cite-map.md` to mark it `[APPLIED <date>]`.

   If nothing was flagged, skip this step and note `cite_map_excluded=0` in
   the close-out entry.

10. **Close out.** Append to `decisions.md`:

    ```
    phase=draft words=<N> citations=<C> bib_entries=<C> cite_map_deferred=<D> cite_map_excluded=<E> status=delivered
    ```

    Add a "Reproduction" footer to `lit-review.md` listing the date and the
    commands needed to regenerate `references.bib` from `catalog.json`.

---

## Definition of done

- [ ] `lit-review.md` is within ±20% of the target word count.
- [ ] Every `[@key]` resolves to an entry in `catalog.json`.
- [ ] `references.bib` parses cleanly (the build script validates this).
- [ ] No citation appears in the bib without appearing in the draft, and vice versa.
- [ ] `cite-map.md` accounts for every catalog entry (cited ∪ deferred ∪ excluded = catalog total).
- [ ] Every deferred entry in `cite-map.md` has a proposed home (§, role).
- [ ] Any retirement bucket in `cite-map.md` has been applied to `catalog.json` via `tools/catalog.py update` (or explicitly deferred with a written note in `decisions.md`).
- [ ] `decisions.md` ends with a delivery entry that includes `cite_map_deferred=<D>` and `cite_map_excluded=<E>`.
- [ ] The user has explicitly accepted the draft and the citation map.