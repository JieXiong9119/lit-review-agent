---
key: jiang2023active
doi: 10.18653/v1/2023.emnlp-main.495
arxiv_id: null
title: "Active Retrieval Augmented Generation"
authors: ["Zhengbao Jiang", "Frank F. Xu", "Luyu Gao", "Zhiqing Sun", "Qian Liu", "Jane Dwivedi-Yu", "Yiming Yang", "Jamie Callan", "Graham Neubig"]
year: 2023
venue: "EMNLP 2023"
url: https://aclanthology.org/2023.emnlp-main.495/
pdf_path: null
tags: [rag, active-retrieval]
status: metadata-only
include_reason: "Introduces active retrieval triggered by token-level uncertainty; concrete instance of Advanced/Modular RAG patterns."
---

# Active Retrieval Augmented Generation (Jiang et al., EMNLP 2023)

> **status:** metadata-only — this summary is built from the abstract alone; do
> not cite specific results from it.

## Problem
Single-shot retrieve-then-generate, the dominant pattern at the time, retrieves
once at the start and then generates the full answer. For long-form generation,
the information needed often changes mid-response. The paper asks: when and
what should the model re-retrieve, *during* generation?

## Method
The authors propose **FLARE** (Forward-Looking Active REtrieval), which lets
the LLM emit a draft of the next sentence, detects low-confidence spans via
token probabilities, and conditionally re-retrieves using those uncertain
spans as queries before committing to the sentence.

## Key findings
- Active retrieval improves long-form generation tasks (multi-hop QA,
  open-domain summarization, code generation, commonsense reasoning) over
  single-shot RAG and over fixed-interval re-retrieval baselines.
- The benefit is largest on tasks where the answer composition requires
  multiple distinct facts; tasks with a single retrieval target see smaller
  gains.

## Limitations
- Token-probability triggers depend on the LLM exposing calibrated
  probabilities; many production LLMs do not.
- Re-retrieval adds latency proportional to the number of triggered spans.
- Evaluation is on standard benchmarks; transfer to domain-restricted corpora
  (the project's case) is not directly evaluated.

## Relevance to this project
Addresses **SQ1** (architecture beyond Naive RAG) and **SQ3** (when retrieval
helps vs. hurts). The hypothetical project's prototype uses single-shot
retrieval; active retrieval is a concrete alternative when retrieval recall is
good but the generator still drifts.

## Quotable passages
> "We propose forward-looking active retrieval augmented generation, FLARE, a
> generic method which iteratively uses a prediction of the upcoming sentence
> to anticipate future content, which is then utilized as a query to retrieve
> relevant documents to regenerate the sentence if it contains low-confidence
> tokens." — abstract

## Open questions for synthesis
- Pair with `chen2024rgb` to ask whether RGB's noise-robustness axis predicts
  which spans active retrieval will trigger on.
