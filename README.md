# lit-review-agent

A **persistent, cross-platform AI agent** dedicated to literature review work.
One agent, many projects. The agent itself lives in this repo and is iterated here;
each project gets its own isolated folder under `projects/<slug>/` for inputs and
deliverables.

The canonical agent spec is [AGENTS.md](AGENTS.md). Everything else (Copilot,
Claude, Cursor configs) delegates to it.

## What you get per project

```
projects/<slug>/
├── intake.md         # topic, sub-questions, scope, inclusion/exclusion criteria
├── existing-work.md  # what the project already cites / claims as a gap
├── papers/           # per-paper Markdown summaries (and optional PDFs)
├── catalog.json      # indexed, queryable paper list
├── synthesis.md      # themes, gaps, comparison matrix
├── lit-review.md     # draft prose section
├── references.bib    # BibTeX companion
└── decisions.md      # audit trail
```

## Quickstart

### 1. Install the helper tools (one time)

```powershell
pip install -r tools/requirements.txt
```

### 2. Start a session in your AI tool of choice

All of these read the same canonical spec — pick the one you already use.

| Tool | How it discovers the agent |
|---|---|
| **GitHub Copilot (VS Code)** | `.github/copilot-instructions.md` → `AGENTS.md`. Slash commands `/lr-intake`, `/lr-search`, `/lr-acquire`, `/lr-synthesize`, `/lr-draft` are available. |
| **Claude Code** | `CLAUDE.md` → `AGENTS.md`. |
| **opencode / Codex CLI / any AGENTS.md-aware tool** | Reads `AGENTS.md` directly. |
| **Cursor** | `.cursor/rules/lit-review.mdc` → `AGENTS.md`. |
| **ChatGPT / web Claude / other chat** | Open `AGENTS.md` and paste it as a system / project instruction. |

### 3. Kick off a review

Tell the agent something like:

> "Start a new literature review. Slug: `rag-sci-qa`. Project repo at
> `C:\Users\me\Documents\GitHub\sci-qa`."

The agent will run phase 1 (intake), then proceed through the 6-phase workflow,
asking for confirmation at each handoff.

## Repository layout

```
lit-review-agent/
├── AGENTS.md                          # canonical spec
├── CLAUDE.md, .cursor/, .github/      # platform shims & VS Code primitives
├── agent/
│   ├── workflows/                     # 6 phase playbooks
│   ├── templates/                     # output file skeletons
│   └── rubrics/                       # reasoning checklists
├── tools/                             # Python helpers (search, fetch, catalog, bib)
└── projects/
    ├── _example/                      # worked reference (committed)
    └── <your-slug>/                   # your reviews (gitignored by default)
```

## Iterating the agent

When you notice a missing capability or a rough edge, improve the **agent**, not the
project. Edit files under `agent/` or `tools/`, commit, and every future project
benefits. Per-project notes stay inside `projects/<slug>/` and are never promoted
silently.
