# GitHub Copilot instructions

The canonical agent spec for this repository is [AGENTS.md](../AGENTS.md).
Read it first; it defines your identity, workflow, output contract, tool-use
policy, and the no-fabrication rule.

Additional Copilot-specific notes:

- Slash commands `/lr-intake`, `/lr-search`, `/lr-acquire`, `/lr-synthesize`,
  `/lr-draft` are defined under [.github/prompts/](prompts/) and run the matching
  workflow playbook under [agent/workflows/](../agent/workflows/).
- The [.github/skills/lit-review/](skills/lit-review/) skill orchestrates the full
  6-phase pipeline end-to-end with user checkpoints.
- Scoped file instructions in [.github/instructions/](instructions/) apply only
  inside `projects/**` and keep code-completion-style suggestions on-topic
  without burning global context.
- When running Python helpers, prefer the terminal over describing the call.
