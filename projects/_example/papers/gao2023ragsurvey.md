---
key: gao2023ragsurvey
doi: 10.48550/arxiv.2312.10997
arxiv_id: 2312.10997
title: "Retrieval-Augmented Generation for Large Language Models: A Survey"
authors: ["Yunfan Gao", "Yun Xiong", "Xinyu Gao", "Kangxiang Jia", "Jinliu Pan", "Yuxi Bi", "Yi Dai", "Jiawei Sun", "Meng Wang", "Haofen Wang"]
year: 2023
venue: "arXiv preprint"
url: https://arxiv.org/abs/2312.10997
pdf_path: null
tags: [rag, survey]
status: metadata-only
include_reason: "Comprehensive 2023 survey covering Naive/Advanced/Modular RAG paradigms; provides the taxonomy used in this review."
---

# RAG for LLMs: A Survey (Gao et al., 2023)

> **status:** metadata-only — this summary is built from the abstract alone; do
> not cite specific results from it.

## Problem
LLMs hallucinate, have outdated parametric knowledge, and reason opaquely.
Retrieval-augmented generation aims to address all three by grounding outputs
in external corpora at inference time. The survey asks: what is the design
space of RAG systems in 2023, and which axes matter?

## Method
Taxonomic review. The authors partition existing RAG systems into three
paradigms — **Naive RAG** (retrieve-once, concatenate), **Advanced RAG**
(pre/post-retrieval refinement), and **Modular RAG** (orchestrated multi-step
retrieval and reasoning) — and examine each along three axes: retrieval,
generation, and augmentation.

## Key findings
- The survey proposes a three-paradigm taxonomy that has since become a common
  framing for RAG architectures.
- Each paradigm trades off latency, complexity, and grounding quality
  differently; no single design dominates.
- Evaluation practice is heterogeneous — different papers use incompatible
  benchmarks, complicating cross-system comparison.

## Limitations
- As a survey, the paper does not run new experiments; conclusions are
  organizational rather than empirical.
- Coverage stops in late 2023; rapid-moving subarea so the taxonomy may already
  be incomplete by the time the project's review concludes.

## Relevance to this project
Addresses **SQ1** ("dominant RAG architectures") directly. Provides the
vocabulary (Naive / Advanced / Modular) that the synthesis uses as its
backbone. The project's hypothetical prototype is best described as Naive RAG,
which contextualizes why iterative-retrieval work matters to them.

## Quotable passages
> "We trace the progression of RAG paradigms, encompassing the Naive RAG, the
> Advanced RAG, and the Modular RAG." — abstract

## Open questions for synthesis
- Pair with `jiang2023active` to show concrete movement from Naive toward
  Advanced/Modular paradigms.
- Pair with `chen2024rgb` to show what the survey's "heterogeneous evaluation"
  observation looks like in practice.
