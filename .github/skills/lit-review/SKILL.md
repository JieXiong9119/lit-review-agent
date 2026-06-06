---
name: lit-review
description: Orchestrate the full 6-phase literature review pipeline end-to-end for a project, with user confirmation at each phase handoff. Use when the user says "do a literature review", "start a lit review", or names this agent. Reads the canonical spec in AGENTS.md and the phase playbooks in agent/workflows/.
---

# Literature review — full pipeline orchestrator

You are running the persistent literature review agent defined in
[AGENTS.md](../../../AGENTS.md). Read it before starting if you have not already.

## Procedure

1. **Get the project slug.** Ask the user for a short kebab-case identifier.
   Create `projects/<slug>/` if it does not exist. If it does and is non-empty,
   read every file and report what you found before proceeding — the user may
   be resuming.

2. **Run each phase in order, stopping at every handoff for confirmation.**

   | # | Phase | Playbook | Output |
   |---|---|---|---|
   | 1 | Intake | [agent/workflows/1-intake.md](../../../agent/workflows/1-intake.md) | `intake.md` |
   | 2 | Existing work | [agent/workflows/2-existing-work.md](../../../agent/workflows/2-existing-work.md) | `existing-work.md` |
   | 3 | Search | [agent/workflows/3-search.md](../../../agent/workflows/3-search.md) | cached `.cache/*.json` + decisions log |
   | 4 | Acquire & index | [agent/workflows/4-acquire-index.md](../../../agent/workflows/4-acquire-index.md) | `catalog.json`, `papers/<key>.md` |
   | 5 | Synthesize | [agent/workflows/5-synthesize.md](../../../agent/workflows/5-synthesize.md) | `synthesis.md` |
   | 6 | Draft | [agent/workflows/6-draft.md](../../../agent/workflows/6-draft.md) | `lit-review.md`, `references.bib`, `cite-map.md` |

   Each playbook ends with a hand-off checklist. Do not advance until every box
   on that checklist is checked AND the user has said "continue" (or equivalent).

3. **Use the Python helpers in [tools/](../../../tools/)** for every
   deterministic operation (search APIs, PDF fetch, text extraction, catalog
   management, BibTeX rendering). Reasoning belongs in chat; deterministic I/O
   belongs in scripts.

4. **Honor the no-fabrication rule** ([AGENTS.md §6](../../../AGENTS.md)):
   - Every citation in `lit-review.md` MUST resolve to a `catalog.json` entry.
     `tools/build_bib.py --only-cited` enforces this.
   - For papers whose PDFs you could not obtain, mark them `metadata-only` and
     do not invent specific results.

5. **Log every decision** in `projects/<slug>/decisions.md` — every query run,
   every include / exclude judgement, every loop back to an earlier phase. This
   is the user's audit trail.

## Stopping early

The user may want to run only part of the pipeline. Slash-command equivalents
exist for each phase: `/lr-intake`, `/lr-search`, `/lr-acquire`,
`/lr-synthesize`, `/lr-draft`. If asked, jump to the matching playbook directly
instead of orchestrating from the top.

## On error

If a tool script fails (network error, missing PDF, API rate limit), do not
guess what it would have returned. Report the failure to the user, suggest a
retry or alternative backend, and only proceed once the failure is resolved or
the user explicitly asks you to skip.
