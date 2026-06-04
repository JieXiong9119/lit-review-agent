# Phase 1 — Intake

**Goal.** Turn a vague user request ("do a lit review on X") into a precise,
written research brief that all subsequent phases anchor on.

**Inputs required.**
- A project slug (kebab-case).
- The user's initial topic statement, however rough.

**Output.** `projects/<slug>/intake.md` (template:
[agent/templates/intake.md](../templates/intake.md)).

---

## Steps

1. **Confirm or create the project folder.** Ensure `projects/<slug>/` exists. If it
   already contains files, read them and report what you found before continuing —
   the user may be resuming a previous session.

2. **Interview the user.** Ask the following questions, in order. Stop and wait for
   each answer. Do not invent answers. If the user is unsure on a question, write
   `TBD — to revisit after phase 3` in the intake doc and move on.

   1. **Primary research question.** One sentence. ("What is the user actually
      trying to know?")
   2. **Sub-questions.** 2–5 sharper questions that decompose the primary one.
   3. **Field(s) / discipline(s).** E.g., NLP, condensed-matter physics, health
      policy. This drives which search backends to favor in phase 3.
   4. **Scope boundaries.**
      - Time window (e.g., 2019–present).
      - Geographic / linguistic limits, if any.
      - Theoretical vs. applied vs. both.
   5. **Inclusion criteria.** What must a paper have for you to read it in full?
      (E.g., "empirical evaluation on ≥1 public benchmark", "peer-reviewed venue",
      "open-access PDF available".)
   6. **Exclusion criteria.** Hard rejects. (E.g., "no workshop papers without
      formal evaluation", "no purely theoretical work without experiments".)
   7. **Target output size.** Approximate word count for `lit-review.md` and number
      of papers to cite. Anchors phase 4 stopping criterion.
   8. **Citation key convention.** Default `authorYearShorttitle` (e.g.,
      `lewis2020rag`). Confirm or override.
   9. **Known seed papers.** Any papers the user already knows belong in the review.
      Capture title + author + year (or DOI / arXiv id). These become forward/backward
      citation roots in phase 3.

3. **Draft `intake.md`.** Fill the template verbatim. Quote the user's wording in
   the "Primary research question" field — do not paraphrase.

4. **Confirm with the user.** Show the draft and ask: "Anything to change before we
   move on?" Wait for explicit go-ahead.

5. **Initialize the audit log.** Create `projects/<slug>/decisions.md` from
   [agent/templates/decisions.md](../templates/decisions.md). Add a first entry:
   `phase=intake, status=complete, summary=<one line>`.

---

## Hand-off to phase 2

You may proceed to [2-existing-work.md](2-existing-work.md) once:

- [ ] `intake.md` exists and is fully populated (or fields marked `TBD` explicitly).
- [ ] The user has confirmed the draft.
- [ ] `decisions.md` exists with the intake entry.

If the user changes scope materially in any later phase, return here and update
`intake.md` rather than silently widening the search.
