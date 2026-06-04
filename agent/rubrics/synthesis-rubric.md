# Rubric — synthesis

Use this checklist while filling `synthesis.md` from
[../templates/synthesis.md](../templates/synthesis.md). Phase 5 cannot be marked
complete until every box checks.

## Themes
- [ ] 3–6 themes (more than 6 usually means the synthesis is fragmented; fewer
      than 3 usually means it is too coarse).
- [ ] Each theme is phrased as a *claim or tension*, not a topic label.
      - Bad: "Retrieval methods."
      - Good: "Retrieval quality dominates generator size in scientific QA."
- [ ] Each theme cites ≥3 catalog keys.
- [ ] Every intake sub-question is addressed by at least one theme.

## Comparison matrix
- [ ] At least one matrix with rows = papers, columns = `{dataset, method, key
      result, limitation}` (adapt columns to the domain — e.g., for a theoretical
      review the columns might be `{assumption, technique, theorem, scope}`).
- [ ] ≤ 15 rows per matrix (split if larger).
- [ ] Every cell is grounded in the matching `papers/<key>.md`; no inferences
      that don't appear in a summary.

## Convergences and conflicts
- [ ] ≥1 convergence point identified (multiple papers reaching the same
      conclusion independently).
- [ ] ≥1 conflict identified (papers disagreeing on data, claims, or
      interpretation) — *or* an explicit statement that no meaningful conflicts
      exist in the corpus.

## Gaps
- [ ] Every claimed gap is *concrete* (a future paper could plausibly address it).
- [ ] Every claimed gap is *unfilled* by the catalog (re-checked before claiming).
- [ ] Every gap is consistent with the project's claimed contribution in
      `existing-work.md`, *or* the mismatch is explicitly flagged.
- [ ] No vague gaps ("more research is needed on X").

## Coverage
- [ ] Every `include`d catalog entry appears in at least one theme, matrix row,
      or gap discussion. If not, the synthesis explains why it stayed in the
      catalog (e.g., "background context, not synthesized").
- [ ] Every key cited in `synthesis.md` exists in `catalog.json`.
- [ ] No fabricated keys.

## Honesty
- [ ] Where the corpus is thin on a theme, the synthesis says so rather than
      overclaiming.
- [ ] Where two papers seem to disagree only because of different definitions or
      benchmarks, the synthesis notes that confound rather than presenting it as
      a substantive disagreement.
