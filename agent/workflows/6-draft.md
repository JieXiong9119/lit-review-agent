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

8. **Close out.** Append to `decisions.md`:

   ```
   phase=draft words=<N> citations=<C> bib_entries=<C> status=delivered
   ```

   Add a "Reproduction" footer to `lit-review.md` listing the date and the
   commands needed to regenerate `references.bib` from `catalog.json`.

---

## Definition of done

- [ ] `lit-review.md` is within ±20% of the target word count.
- [ ] Every `[@key]` resolves to an entry in `catalog.json`.
- [ ] `references.bib` parses cleanly (the build script validates this).
- [ ] No citation appears in the bib without appearing in the draft, and vice versa.
- [ ] `decisions.md` ends with a delivery entry.
- [ ] The user has explicitly accepted the draft.
