# Existing work — `_example`

> Worked example. In a real project this file would summarize an actual project
> repository; here we fabricate a plausible project context to demonstrate the
> file shape.

## Source
- **Mode:** B (user-pasted summary)
- **Path / origin:** chat
- **Scanned on:** 2026-06-04

## What the project does
The hypothetical downstream project builds a domain-restricted QA assistant for
materials-science researchers. The team has a working prototype that retrieves
passages from a curated PDF corpus and feeds them to an instruction-tuned LLM.
They notice hallucinations even when relevant passages are retrieved, and want
a literature review to ground their next design iteration.

## Already-cited works
- `gao2023ragsurvey` — Retrieval-Augmented Generation for Large Language Models:
  A Survey. Gao et al., 2023. arXiv:2312.10997. (Used as the primary background
  reference in the project's existing internal design doc.)

## Claimed gaps / open questions
- > "Retrieval recall is good but generation still hallucinates; we don't know
  > whether the bottleneck is the retriever, the generator, or the integration."
  > — internal design doc §3

## Apparent assumptions worth checking
- Assumes retrieval recall is the dominant lever (the project measures retrieval
  metrics in isolation). The literature may suggest other failure modes.
- Assumes a single-shot retrieve-then-generate pattern is adequate. Iterative or
  active retrieval may be relevant.

## User-provided summary (mode B only)
> "We're building a RAG system for materials-science Q&A. Retrieval works fine
> (high recall on a held-out set), but the model still fabricates citations and
> mixes up properties. Want to know: what's the state of the art on actually
> *measuring* RAG hallucination, and on architectures that reduce it."

---

*Phase 2 completed on 2026-06-04 (example data).*
