# Literature Review — Retrieval-Augmented Generation and the Hallucination Frontier

> Worked example. ~330 words, three citations. Demonstrates the file shape;
> a real deliverable would be 5–10× longer.

## 1. Introduction

Retrieval-augmented generation (RAG) was proposed to address the chronic
weaknesses of parametric large language models — outdated knowledge,
hallucination, and opacity — by grounding outputs in external corpora at
inference time. As RAG systems have proliferated, the field has begun to
distinguish what RAG *does* well from where it still fails. This section
reviews the 2023–2024 literature along three threads: how RAG architectures
have stratified, how their evaluation has matured, and what those two
developments together reveal about the locus of RAG's remaining failure modes.

## 2. A paradigm hierarchy of RAG architectures

The 2023 survey literature converges on a three-tier taxonomy of RAG
systems — Naive (single-shot retrieve-then-generate), Advanced (pre- or
post-retrieval refinement), and Modular (multi-step retrieval interleaved with
reasoning) [@gao2023ragsurvey]. Concrete instances of the upper tiers have
followed: FLARE re-queries mid-generation whenever the LLM's own token
probabilities indicate uncertainty, improving long-form generation tasks where
the answer requires several distinct facts [@jiang2023active].

## 3. Evaluation that diagnoses, not merely scores

Surveys note that comparing RAG systems is hard because evaluation practice is
heterogeneous [@gao2023ragsurvey]. The RGB benchmark answers this by
decomposing RAG ability into four diagnosable capabilities — noise robustness,
negative rejection, information integration, and counterfactual
robustness — and finds that current LLMs cluster their failures on the latter
three even when they tolerate noisy context [@chen2024rgb].

## 4. Where RAG actually fails: the generator, not the retriever

Two independent lines converge on the same diagnosis. RGB localizes the
weakest links inside the generator [@chen2024rgb]; active retrieval delivers
its gains specifically when the generator's own uncertainty signals a fact it
cannot integrate [@jiang2023active]. Together they suggest that the lever for
the next wave of RAG improvements is *coordination* between retrieval and the
generator's internal state, not retrieval recall.

## 5. Gaps and outlook

Two specific gaps remain in this corpus. First, no benchmark in this survey
evaluates RAG capabilities on domain-restricted scientific corpora; results on
general-domain text may not transfer. Second, the interaction between active
retrieval [@jiang2023active] and the RGB capability axes [@chen2024rgb] is
unstudied: it is not yet known whether FLARE-style re-retrieval specifically
rescues integration failures, counterfactual failures, or both.

---

## Reproduction

This review was assembled on 2026-06-04 using the lit-review-agent. To
regenerate `references.bib` from the catalog:

```powershell
python tools/build_bib.py --project projects/_example `
    --only-cited projects/_example/lit-review.md `
    --out projects/_example/references.bib
```
