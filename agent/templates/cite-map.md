# Citation map — `<project title>`

> Generated in phase 6, step 7. Purpose: partition every prior-art reference
> in `catalog.json` into two buckets — (a) cited in `lit-review.md`, (b) deferred
> to other sections of the user's paper/report (methodology, results,
> discussion, program-landscape, data-source notes, appendices). Each deferred
> entry gets a *proposed home* so the methodology writer (and any later section
> writer) starts from a checklist instead of re-deriving the partition.
>
> Scope: this file is about the user's **own** paper structure, not the
> literature review. It complements `lit-review.md` by ensuring no
> already-included literature is silently abandoned just because it does not
> fit the §2 Related-Work narrative.
>
> Maintenance rule: when any non-§2 section of the paper is drafted, check
> every deferred row and mark `[cited in §<N>]`, `[moved to §<N>]`, or
> `[dropped: <reason>]`. If any row stays unmarked, raise it for the user.

---

## Counts at draft time (<YYYY-MM-DD>)

- Catalog entries total: `<T>`
- Cited in `lit-review.md`: `<C_lit>`
- Deferred to other sections: `<C_def>`
- Excluded (status `excluded` in catalog): `<C_exc>`

`<C_lit>` + `<C_def>` + `<C_exc>` should equal `<T>` (sanity check).

**Companion BibTeX files.**
- `references.bib` (`<C_lit>` entries) — only the keys cited in `lit-review.md`;
  merge into the host paper's §2 bib.
- `cite-map.bib` (`<T> − <C_exc>` entries) — every non-excluded catalog entry
  (cited + deferred); use this when drafting §1 / §3 / §4 / §5 / §6 so any
  deferred row in the buckets below can be `\cite{...}`d without re-resolving
  metadata. Regenerate with
  `python tools/build_bib.py --project projects/<slug> --out projects/<slug>/cite-map.bib`
  (excluded entries are dropped automatically).

---

## Bucket organization

Use the buckets that make sense for the project. Suggested buckets to cover:

1. **Authors' own prior-art / immediate-predecessor reports** — cite cluster at
   the opening of §3 Methodology, and again wherever §4 Results reports a number
   that is directly comparable to one of these prior reports.
2. **Data-source / dataset references** — §3 Methodology data subsection;
   figure-caption / table-footer data-source notes. (E.g., national survey
   datasets, public-rate databases, scenario libraries.)
3. **Tool / software / framework references** — §3 Methodology or "Code and data
   availability" footnote. (E.g., GitHub repos, technical reference manuals.)
4. **National-context / aggregate statistics** — §1 Introduction (single-cite
   motivation); §5 Discussion when an aggregate-vs-bottom-up contrast is made.
5. **Program-landscape, regulatory, or vendor citations** — §5 Discussion or
   §6 Program/Policy landscape, typically as a single packed paragraph.
6. **Historical / pre-cutoff precedents** — §3 Methodology when a control
   strategy or analytical choice is directly inherited; otherwise §5 Discussion
   as historical context. Flag out-of-scope items (e.g., wrong domain) for
   possible drop.
7. **Already cited in `lit-review.md`** — listed for completeness; no action
   required from the section writer.
8. **Out-of-scope retirements** — entries that passed the phase-4 keyword sift
   but on closer inspection are out of scope for the lit-review. Each row
   gets a one-line `exclude_reason`. **Apply** to `catalog.json` via
   `tools/catalog.py update --status excluded --exclude-reason "..."`
   (workflow step 9). Once applied, mark this bucket `[APPLIED <date>]`.

---

## Bucket 1 — Authors' own prior-art (§3 Methodology + §4 Results)

| Key | Title | Proposed home |
|---|---|---|
| `<key>` | `<short title>` | `<§N + role>` |

Suggested cite pattern at the §3 opening:

> "This study reuses the <X> formulation previously documented in <N> prior
> reports [@<key1>; @<key2>; ...] and extends them by ..."

## Bucket 2 — Data-source / dataset references (§3 + caption footers)

| Key | Title | Proposed home |
|---|---|---|

## Bucket 3 — Tool / software / framework references (§3 or appendix)

| Key | Title | Proposed home |
|---|---|---|

## Bucket 4 — National-context / aggregate statistics (§1 or §5)

| Key | Title | Proposed home |
|---|---|---|

## Bucket 5 — Program-landscape / vendor / regulatory (§5 or §6)

| Key | Title | Proposed home |
|---|---|---|

Suggested single-paragraph cite pattern:

> "<Domain> participation is mediated by <type1> (e.g., [@key1; @key2]),
> <type2> [@key3; @key4], and <protocol/standard> [@key5]."

## Bucket 6 — Historical / pre-cutoff precedents (§3 or §5)

| Key | Title | Proposed home / drop-if |
|---|---|---|

## Bucket 7 — Already cited in `lit-review.md` (no action)

| Key | Where it appears in `lit-review.md` |
|---|---|

## Bucket 8 — Out-of-scope retirements (apply to `catalog.json` via `tools/catalog.py update`)

| Key | Title | Out-of-scope reason (becomes `exclude_reason`) |
|---|---|---|

Apply once the user confirms the retirements:

```powershell
python tools/catalog.py update --project projects/<slug> `
    --key <key> `
    --status excluded `
    --exclude-reason "<reason from table>"
# For >2–3 keys, wrap in projects/<slug>/.cache/apply_retirements.py
```

After apply: re-run `tools/catalog.py validate`, re-run
`tools/build_bib.py --only-cited` (entry count should not change), and mark
this bucket heading `[APPLIED <YYYY-MM-DD>]`.

---

## Checklist for non-§2 section writers

When drafting §1 / §3 / §4 / §5 / §6 / appendices, work through every deferred
row exactly once. Mark each:

- `[cited in §<N>]` — used as planned.
- `[moved to §<N>]` — landed in a different section than proposed.
- `[dropped: <reason>]` — explicitly excluded with a stated reason.

A row that is silently abandoned signals either a forgotten reference or an
implicit retirement decision; raise both for the user.
