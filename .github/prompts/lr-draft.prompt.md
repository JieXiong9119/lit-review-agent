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
6. Present both files for user review.
