# Rubric — per-paper summary

Use this checklist while filling `papers/<key>.md` from
[../templates/paper-summary.md](../templates/paper-summary.md). Every box should
be checkable before you mark the catalog entry as `status: summarized`.

## Sourcing
- [ ] You read the PDF text (or the abstract for `metadata-only` entries). You did
      not summarize from a third-party blog post, review article, or memory.
- [ ] Every direct quote in the summary has a section/page citation.
- [ ] If the paper is `metadata-only`, the summary explicitly says so at the top
      and avoids specific quantitative claims.

## Problem section
- [ ] One paragraph that names the gap the paper claims to fill.
- [ ] Includes the paper's own framing of why the problem matters.

## Method section
- [ ] Names the model class / algorithm / experimental design.
- [ ] Names the dataset(s) and evaluation metric(s).
- [ ] Notes the compute / scale (parameter count, training tokens, etc.) if
      relevant to the project's sub-questions.

## Findings section
- [ ] 3–5 bulleted findings, quantitative where the paper is.
- [ ] Headline number(s) included, with the baseline they are measured against.
- [ ] No findings that the paper does not actually claim.

## Limitations section
- [ ] Author-acknowledged limitations (from "Limitations" or "Discussion").
- [ ] At least one limitation YOU noticed (data leakage risks, generalization,
      reproducibility concerns, benchmark mismatch).
- [ ] If you noticed nothing, write "No additional limitations beyond those the
      authors acknowledge." — do not invent.

## Relevance section
- [ ] Names the intake sub-question(s) the paper bears on.
- [ ] States whether the paper supports, complicates, or contradicts a working
      claim of the project (per `existing-work.md`).
- [ ] Is honest about weak relevance — if the paper is borderline, say so and
      consider moving its status to `excluded`.

## Quotable passages
- [ ] 2–4 passages, ≤2 sentences each.
- [ ] Each has a section/page citation.
- [ ] Selected to be useful for phase 6 drafting (high-density claims, clean
      definitions, or memorable framings).

## Catalog hygiene
- [ ] Citation key matches the convention from `intake.md`.
- [ ] `tags` include at least one theme tag and one method tag.
- [ ] `status` updated to `summarized` (or `metadata-only`).
- [ ] `summary_path` points to this file.
