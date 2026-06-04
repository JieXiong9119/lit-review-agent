# Synthesis — `_example`

> Worked example. Three papers cluster into three threads that mirror the three
> sub-questions in `intake.md`.

## Spine
1. **SQ1:** What are the dominant RAG architectures circa 2023–2024?
2. **SQ2:** How is RAG performance evaluated, and what does evaluation expose?
3. **SQ3:** When does retrieval *help* vs. *hurt* generation quality?

## Themes

### Theme 1 — RAG has stratified into a paradigm hierarchy (Naive → Advanced → Modular)
The 2023 survey literature is converging on a three-tier taxonomy: single-shot
retrieve-then-generate ("Naive"), pre/post-retrieval refinement ("Advanced"),
and orchestrated multi-step retrieval interleaved with reasoning
("Modular"). [gao2023ragsurvey]

Concrete instances of the Advanced/Modular tier have appeared: FLARE
re-queries mid-generation whenever the LLM's own token probabilities flag
uncertain spans, demonstrating measurable gains on long-form tasks where the
answer requires several distinct facts. [jiang2023active]

**Covers sub-questions:** SQ1.

### Theme 2 — Aggregate accuracy hides where RAG actually fails
Surveys repeatedly note that evaluation across RAG papers is
heterogeneous. [gao2023ragsurvey] RGB responds by decomposing "RAG ability"
into four diagnosable capabilities — noise robustness, negative rejection,
information integration, counterfactual robustness — and shows that current
LLMs cluster their failures on the latter three even when they handle noisy
context. [chen2024rgb]

**Covers sub-questions:** SQ2.

### Theme 3 — Retrieval is necessary but the generator is the binding constraint
Two independent threads point to the same conclusion. RGB localizes the
weakest links inside the generator (integration, counterfactual
robustness). [chen2024rgb] Active retrieval helps precisely when the
generator's own uncertainty signals a fact it cannot integrate, suggesting
the lever is *coordinating* retrieval with the generator's state, not simply
retrieving more. [jiang2023active]

**Covers sub-questions:** SQ3.

## Comparison matrix

| Paper | Setting | Contribution | Headline finding | Limitation |
|---|---|---|---|---|
| `gao2023ragsurvey` | Survey, 2023 | Naive / Advanced / Modular taxonomy | Provides a common vocabulary | No new experiments |
| `jiang2023active` | EMNLP 2023, long-form QA | FLARE, active token-level re-retrieval | Beats single-shot RAG on multi-hop tasks | Needs calibrated token probabilities; adds latency |
| `chen2024rgb` | AAAI 2024, bilingual benchmark | RGB capability decomposition | LLMs weak on negative rejection, integration, counterfactual robustness | Holds retriever fixed |

## Convergences
- Both `jiang2023active` and `chen2024rgb` independently locate the dominant
  RAG failure mode in the generator's handling of retrieved context, not in
  retrieval recall. [jiang2023active, chen2024rgb]

## Conflicts
- No substantive disagreements within this three-paper corpus. (In a real
  review, a thin corpus is itself a signal — either widen the search or scope
  the claims accordingly.)

## Gaps
- **Gap 1:** No paper in the corpus evaluates RAG capabilities on
  domain-restricted scientific corpora; benchmarks are general-domain.
  - *Why it's a gap:* not addressed by [gao2023ragsurvey, jiang2023active,
    chen2024rgb].
  - *Why it matters:* the hypothetical downstream project's corpus is
    materials-science PDFs, where retrieval quality may behave differently
    from open web sources.
- **Gap 2:** No paper evaluates the *interaction* between active retrieval
  and the RGB capability axes (does FLARE-style re-retrieval specifically
  rescue integration failures, or only counterfactual ones?).
  - *Why it's a gap:* both papers exist but the connection is unstudied.

## Coverage check
- [x] Every sub-question from intake is addressed by ≥1 theme.
- [x] Every included catalog entry appears in at least one theme, matrix, or
      gap discussion.
- [x] Every cited key in this file exists in `catalog.json`.

---

*Phase 5 completed on 2026-06-04 (example data).*
