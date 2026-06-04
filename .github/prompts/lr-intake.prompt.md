---
description: Run phase 1 (intake) of the literature review workflow
mode: agent
---

Run [phase 1 — intake](../../agent/workflows/1-intake.md) of the literature review
workflow.

1. Read the playbook fully before starting.
2. If the user has not yet given you a project slug, ask for one.
3. Interview the user following the questions in the playbook. Do not skip
   questions or invent answers.
4. Write the result to `projects/<slug>/intake.md` using
   [agent/templates/intake.md](../../agent/templates/intake.md) verbatim.
5. Initialize `projects/<slug>/decisions.md` from
   [agent/templates/decisions.md](../../agent/templates/decisions.md).
6. Confirm the draft with the user before exiting.
