# Literature Review — `<project title>`

> Drafted in phase 6. Citations use Pandoc syntax `[@key]`. `references.bib` is
> generated from `catalog.json` and contains only the entries cited here.

## 1. Introduction

<Open with the problem and why it matters. State the scope (time window, fields,
exclusions). End the introduction with a one-sentence preview of what the rest of
the section argues.>

## 2. <Theme 1 heading>

<Prose synthesis of theme 1, with inline citations like [@lewis2020rag;
@karpukhin2020dpr]. Use the comparison matrix from synthesis.md if a table reads
better than prose for a given subtopic.>

## 3. <Theme 2 heading>

...

## 4. <Theme 3 heading>

...

## 5. Gaps and outlook

<Closing section. State the concrete gaps from synthesis.md. Connect them to what
this project aims to contribute — but only at the level of "the literature has not
addressed X", not "we will solve X" (the project's own paper does that).>

---

## Reproduction

This review was assembled on <YYYY-MM-DD> using the lit-review-agent
(<https://github.com/...>). To regenerate `references.bib` from the catalog:

```powershell
python tools/build_bib.py --project projects/<slug> `
    --only-cited lit-review.md --out projects/<slug>/references.bib
```

Catalog version: `<git short SHA of catalog.json at draft time>`.
