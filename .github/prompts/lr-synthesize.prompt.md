---
description: Run phase 5 (synthesize) for the active project
mode: agent
---

Run [phase 5 — synthesize](../../agent/workflows/5-synthesize.md).

1. Confirm the project slug. Refuse to proceed if any catalog entry still has
   `status: pending`.
2. Re-read every `papers/<key>.md` before synthesizing — do not rely on memory
   of phase 4.
3. Fill [agent/templates/synthesis.md](../../agent/templates/synthesis.md) using
   [agent/rubrics/synthesis-rubric.md](../../agent/rubrics/synthesis-rubric.md) as
   your checklist.
4. Every claim ends with `[key, ...]` citing catalog entries. No fabrication.
5. If a blind spot surfaces, loop back to `/lr-search` for a narrow follow-up
   rather than papering over it. Log the loop in `decisions.md`.
6. Show the draft to the user and confirm the theme structure before exiting.
