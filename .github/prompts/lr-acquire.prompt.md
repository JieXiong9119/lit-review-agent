---
description: Run phase 4 (acquire + index + summarize) for the active project
mode: agent
---

Run [phase 4 — acquire & index](../../agent/workflows/4-acquire-index.md).

1. Confirm the project slug. Read `intake.md`, `existing-work.md`, and every
   cached `.cache/*.json` from phase 3.
2. Dedupe candidates; apply the inclusion/exclusion criteria strictly.
3. Use `tools/catalog.py add` to register included papers, then `tools/fetch_pdf.py`
   for open-access PDFs, then `tools/pdf_to_text.py` for extracted text.
4. Summarize each included paper into `projects/<slug>/papers/<key>.md` using
   [agent/templates/paper-summary.md](../../agent/templates/paper-summary.md)
   and the checklist in
   [agent/rubrics/paper-summary-rubric.md](../../agent/rubrics/paper-summary-rubric.md).
5. Update each catalog entry's `status` and `summary_path`.
6. Append an acquire-index entry to `decisions.md`, including the full exclusion
   list with reasons.
