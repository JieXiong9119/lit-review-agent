---
key: chen2024rgb
doi: 10.1609/aaai.v38i16.29728
arxiv_id: null
title: "Benchmarking Large Language Models in Retrieval-Augmented Generation"
authors: ["Jiawei Chen", "Hongyu Lin", "Xianpei Han", "Le Sun"]
year: 2024
venue: "Proceedings of the AAAI Conference on Artificial Intelligence"
url: https://ojs.aaai.org/index.php/AAAI/article/view/29728
pdf_path: null
tags: [rag, evaluation, benchmark]
status: metadata-only
include_reason: "RGB benchmark isolating four RAG-specific capabilities; directly answers SQ2 on how RAG is evaluated."
---

# RGB: Benchmarking LLMs in RAG (Chen et al., AAAI 2024)

> **status:** metadata-only — this summary is built from the abstract alone; do
> not cite specific results from it.

## Problem
End-to-end RAG accuracy mixes too many factors (retrieval quality, generator
quality, integration ability) to diagnose where failures come from. The paper
asks: what are the *capabilities* an LLM must have to consume retrieved
context well, and how do current LLMs score on each?

## Method
The authors construct **RGB** (Retrieval-Augmented Generation Benchmark),
splitting RAG capability into four testbeds: **noise robustness**, **negative
rejection**, **information integration**, and **counterfactual robustness**.
RGB is bilingual (English / Chinese) and evaluates 6 representative LLMs.

## Key findings
- LLMs are reasonably noise-robust but struggle materially on negative
  rejection (admitting "I don't know" when retrieved context is irrelevant),
  information integration (combining facts across passages), and
  counterfactual robustness (resisting incorrect retrieved claims).
- These failures persist across both English and Chinese, suggesting the
  capability gaps are not artifacts of any single language's training mix.

## Limitations
- RGB tests LLM consumption of retrieved context but holds the retriever
  fixed; it does not diagnose retriever-side failure modes.
- The six evaluated LLMs are a 2023 snapshot; capability gaps may shift with
  newer models.

## Relevance to this project
Directly addresses **SQ2** (how is RAG evaluated, what does it expose) and
**SQ3** (when does retrieval hurt — specifically, when the LLM lacks negative
rejection or integration ability). For the hypothetical project, RGB suggests
the observed "hallucinations despite good retrieval" likely traces to
integration and counterfactual-robustness failures in the generator, not the
retriever.

## Quotable passages
> "We analyze the performance of different large language models in 4
> fundamental abilities required for RAG, including noise robustness, negative
> rejection, information integration, and counterfactual robustness." —
> abstract

## Open questions for synthesis
- Pair with `gao2023ragsurvey` to argue that the survey's
  "heterogeneous-evaluation" observation is partly addressed by RGB's
  capability-decomposition approach.
