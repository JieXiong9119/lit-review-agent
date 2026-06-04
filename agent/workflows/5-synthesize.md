# Phase 5 — Synthesize

**Goal.** Move from a pile of per-paper summaries to a structured understanding:
themes, methodological lineages, points of disagreement, and — crucially — gaps
that frame why the project's contribution matters.

**Inputs required.**
- A complete `catalog.json` (no `pending` entries).
- Every included paper has a `papers/<key>.md` summary.
- `intake.md` (the sub-questions are the spine of the synthesis).
- `existing-work.md` (gaps the project already claims — verify or refute them).

**Output.** `projects/<slug>/synthesis.md` (template:
[agent/templates/synthesis.md](../templates/synthesis.md)). Use
[agent/rubrics/synthesis-rubric.md](../rubrics/synthesis-rubric.md) as your checklist.

---

## Steps

1. **Re-read every summary in one pass.** Do not synthesize from memory of phase 4.
   Open each `papers/<key>.md` and skim it. Note any that surprise you on second
   read — those often anchor themes.

2. **Cluster into themes.** Aim for 3–6 themes that collectively cover the
   sub-questions in `intake.md`. A theme is *not* a topic label; it's a claim or
   tension shared across multiple papers (e.g., "Retrieval quality dominates
   generator size in scientific QA" rather than "Retrieval methods"). Each theme
   must cite ≥3 catalog keys.

3. **Build a comparison matrix.** For methodological reviews, a small table of
   `paper × {dataset, method, key result, limitation}` is usually the most useful
   single artifact in the deliverable. Use Markdown table syntax; keep it under
   ~15 rows per table (split if larger).

4. **Surface conflicts and convergences.** Find at least one case where two papers
   disagree (different results on the same benchmark, contradictory claims) and at
   least one case of strong convergence (multiple independent papers reaching the
   same conclusion). Both are high-signal for the draft in phase 6.

5. **Identify gaps — carefully.** A real gap is one that:
   - Is *not* already filled by a paper in your catalog (re-check before claiming).
   - Is *consistent* with the project's claimed contribution from `existing-work.md`
     (or, if not, you explicitly flag the mismatch).
   - Is specific enough that a future paper could plausibly address it.

   Vague gaps ("more work is needed on X") are forbidden. Write concrete ones or
   none.

6. **Map every claim back to keys.** Every sentence in `synthesis.md` that asserts
   something about the literature must end with `[key1, key2, ...]` citing the
   catalog entries that support it. This is the input format phase 6 will convert
   into prose citations.

7. **Show & confirm.** Present the draft synthesis to the user and ask: "Do these
   themes match how you think about this space? Anything missing?" Iterate before
   moving on.

8. **Log.** Append to `decisions.md`:
   `phase=synthesize n_themes=<T> n_conflicts=<C> n_gaps=<G> matrix_rows=<R>`.

---

## When to loop back to phase 3

If, while synthesizing, you find a clear blind spot (e.g., "we have no papers on
evaluation methodology, only on architectures"), do not paper over it. Return to
[3-search.md](3-search.md), run a narrowly targeted search, and re-enter phase 4
for only the new candidates. Log the loop in `decisions.md`.

---

## Hand-off to phase 6

You may proceed to [6-draft.md](6-draft.md) once:

- [ ] `synthesis.md` has themes, comparison matrix, conflicts, convergences, and
      gaps — all populated.
- [ ] Every claim cites at least one catalog key, and every cited key exists in
      `catalog.json`.
- [ ] The user has signed off on the theme structure.
