# Phase 2 — Existing-work scan

**Goal.** Understand what the project already knows, has cited, or claims as a gap,
so that phase 3 searches focus on what is *missing* rather than re-discovering what
the user already has.

**Inputs required.**
- `projects/<slug>/intake.md` from phase 1.
- Either a local path to the project's own repository, or a pasted summary from the
  user.

**Output.** `projects/<slug>/existing-work.md` (template:
[agent/templates/existing-work.md](../templates/existing-work.md) — if missing, write
the four sections below by hand).

---

## Steps

1. **Locate the project context.** Per [AGENTS.md §3](../../AGENTS.md), ask:
   - "Do you have a local path to the project repository?" If yes → read mode A.
   - If no → ask for a pasted summary → mode B.

   **Mode A — local repo (read-only).**

   - Confirm the path exists and is a directory. Refuse to write to it.
   - Scan, in this order, and only if present:
     - `README*` at the root.
     - `docs/`, `documentation/` — Markdown / reStructuredText.
     - `notes/`, `notebooks/` — research notes, draft sections.
     - `paper/`, `manuscript/`, `writeup/`, `thesis/` — any existing prose.
     - `*.bib`, `references.bib`, `bibliography.bib` — already-cited works.
     - `proposal*`, `grant*` — funded statements of intent.
   - Skip `node_modules/`, `.venv/`, build artifacts, large data directories.
   - Limit total reading to a sane bound (e.g., ≤200 KB of text). If the repo is
     larger, summarize per-directory and ask the user which subset to deep-read.

   **Mode B — pasted summary.**

   - Ask the user for: problem being solved, current status, what's already been
     tried, what they believe the gap is, any known related work.
   - Save the raw text verbatim into `existing-work.md` under a
     "User-provided summary" heading. Do not paraphrase.

2. **Extract four things.** Write these into `existing-work.md`:

   - **What the project does / aims to do** (1 paragraph, neutral phrasing).
   - **Already-cited works** (bulleted list with as much metadata as you can find:
     title, authors, year, venue, DOI/URL). If a `.bib` file was found, list every
     entry. These will be pre-seeded into the catalog in phase 4.
   - **Claimed gaps / open questions** (verbatim quotes from the repo where
     possible, with file:line citations).
   - **Apparent assumptions worth checking** — things the project takes for
     granted that the literature review may confirm or challenge.

3. **Cross-check against intake.** If the existing-work scan reveals that the user's
   primary question is already substantially answered in their own notes, surface
   this immediately. Suggest narrowing the intake. Do not silently proceed with a
   redundant review.

4. **Log.** Append to `decisions.md`:
   `phase=existing-work, mode=A|B, source=<path or "user summary">, found=<N papers, M gap claims>`.

---

## Hand-off to phase 3

You may proceed to [3-search.md](3-search.md) once:

- [ ] `existing-work.md` exists with all four sections populated.
- [ ] Pre-existing citations are listed in a form ready to seed the catalog.
- [ ] The user has acknowledged the scan (a "looks right, continue" suffices).
