"""Manage the per-project catalog.json.

Subcommands:
    init       Create an empty catalog for a project.
    add        Add or update an entry, optionally pulling from a search result JSON.
    list       Print catalog entries (filterable).
    get        Print a single entry as JSON.
    dedupe     Merge duplicate entries by DOI / arXiv id / normalized title.
    validate   Check the catalog against catalog.schema.json (best-effort, no jsonschema dep).

Examples:
    python tools/catalog.py init --project projects/<slug>
    python tools/catalog.py add --project projects/<slug> --key lewis2020rag \\
        --from-json projects/<slug>/.cache/arxiv-q1.json --match-doi 10.48550/arXiv.2005.11401 \\
        --status pending --include-reason "Foundational RAG architecture."
    python tools/catalog.py list --project projects/<slug> --status summarized
    python tools/catalog.py dedupe --project projects/<slug>
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path
from typing import Any

from _common import normalize_doi, read_json, write_json

VALID_STATUS = {"pending", "summarized", "metadata-only", "pre-existing", "excluded"}


def _catalog_path(project_dir: Path) -> Path:
    return project_dir / "catalog.json"


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _load(project_dir: Path) -> dict[str, Any]:
    path = _catalog_path(project_dir)
    if not path.exists():
        return {"project": project_dir.name, "generated": _now(), "entries": []}
    return read_json(path)


def _save(project_dir: Path, catalog: dict[str, Any]) -> None:
    catalog["generated"] = _now()
    write_json(_catalog_path(project_dir), catalog)


def cmd_init(args: argparse.Namespace) -> int:
    proj = Path(args.project)
    proj.mkdir(parents=True, exist_ok=True)
    path = _catalog_path(proj)
    if path.exists() and not args.force:
        sys.stderr.write(f"{path} already exists. Use --force to overwrite.\n")
        return 1
    write_json(path, {"project": proj.name, "generated": _now(), "entries": []})
    sys.stderr.write(f"Initialized {path}\n")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    proj = Path(args.project)
    catalog = _load(proj)
    entries = catalog["entries"]

    entry: dict[str, Any] = {"key": args.key, "added": _now()}

    if args.from_json:
        records = read_json(args.from_json)
        if not isinstance(records, list):
            sys.stderr.write(f"{args.from_json} is not a list of records.\n")
            return 1
        match = _find_match(records, doi=args.match_doi, arxiv=args.match_arxiv, title=args.match_title)
        if match is None:
            sys.stderr.write("No record in --from-json matched the given filters.\n")
            return 1
        entry.update({
            "doi": normalize_doi(match.get("doi")),
            "arxiv_id": _arxiv_id_from(match),
            "title": match.get("title", ""),
            "authors": match.get("authors", []),
            "year": match.get("year"),
            "venue": match.get("venue"),
            "url": match.get("url"),
            "pdf_url": match.get("pdf_url"),
            "abstract": match.get("abstract"),
            "source": match.get("source"),
        })

    # Per-flag overrides
    for fld in ("doi", "arxiv_id", "title", "venue", "url", "pdf_url", "pdf_path", "summary_path", "include_reason", "exclude_reason", "source", "abstract"):
        val = getattr(args, fld, None)
        if val is not None:
            entry[fld] = normalize_doi(val) if fld == "doi" else val
    if args.year is not None:
        entry["year"] = args.year
    if args.authors:
        entry["authors"] = args.authors
    if args.tags:
        entry["tags"] = args.tags
    if args.status:
        if args.status not in VALID_STATUS:
            sys.stderr.write(f"Invalid status. Allowed: {sorted(VALID_STATUS)}\n")
            return 1
        entry["status"] = args.status
    entry.setdefault("status", "pending")

    existing_idx = next((i for i, e in enumerate(entries) if e.get("key") == args.key), None)
    if existing_idx is not None:
        merged = {**entries[existing_idx], **{k: v for k, v in entry.items() if v is not None}}
        if not merged.get("title"):
            sys.stderr.write("Merged entry has no title. Provide --title or --from-json.\n")
            return 1
        entries[existing_idx] = merged
        sys.stderr.write(f"Updated existing entry {args.key}.\n")
    else:
        if not entry.get("title"):
            sys.stderr.write("New entry missing required field 'title'. Provide --title or --from-json.\n")
            return 1
        entries.append(entry)
        sys.stderr.write(f"Added entry {args.key}.\n")

    _save(proj, catalog)
    return 0


def _arxiv_id_from(rec: dict) -> str | None:
    if rec.get("source") == "arxiv" and rec.get("id"):
        return rec["id"]
    return (rec.get("extra") or {}).get("arxiv_id")


def _find_match(records: list[dict], *, doi: str | None, arxiv: str | None, title: str | None) -> dict | None:
    doi_n = normalize_doi(doi)
    title_n = _norm_title(title) if title else None
    for r in records:
        if doi_n and normalize_doi(r.get("doi")) == doi_n:
            return r
        if arxiv and (r.get("id") == arxiv or (r.get("extra") or {}).get("arxiv_id") == arxiv):
            return r
        if title_n and _norm_title(r.get("title", "")) == title_n:
            return r
    if not (doi_n or arxiv or title_n) and records:
        return records[0]
    return None


def _norm_title(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"[^a-z0-9 ]+", "", s.lower()).strip()


def cmd_list(args: argparse.Namespace) -> int:
    proj = Path(args.project)
    catalog = _load(proj)
    rows = catalog["entries"]
    if args.status:
        rows = [e for e in rows if e.get("status") == args.status]
    if args.tag:
        rows = [e for e in rows if args.tag in (e.get("tags") or [])]
    if args.json:
        import json
        json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        for e in rows:
            authors = ", ".join(e.get("authors", [])[:3])
            if len(e.get("authors", [])) > 3:
                authors += " et al."
            print(f"{e.get('key', '?'):<28} {e.get('year', '----')} {e.get('status', '?'):<14} {e.get('title', '')[:80]}")
            if authors:
                print(f"  {authors}")
    sys.stderr.write(f"\n{len(rows)} entries.\n")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    import json
    proj = Path(args.project)
    catalog = _load(proj)
    e = next((x for x in catalog["entries"] if x.get("key") == args.key), None)
    if e is None:
        sys.stderr.write(f"Key {args.key!r} not found.\n")
        return 1
    json.dump(e, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def cmd_dedupe(args: argparse.Namespace) -> int:
    proj = Path(args.project)
    catalog = _load(proj)
    entries = catalog["entries"]
    seen_doi: dict[str, int] = {}
    seen_arxiv: dict[str, int] = {}
    seen_title: dict[tuple[str, int | None], int] = {}
    keep: list[dict] = []
    dropped = 0
    for e in entries:
        doi = normalize_doi(e.get("doi"))
        arxiv = e.get("arxiv_id")
        title_key = (_norm_title(e.get("title", "")), e.get("year"))
        dup_idx = None
        if doi and doi in seen_doi:
            dup_idx = seen_doi[doi]
        elif arxiv and arxiv in seen_arxiv:
            dup_idx = seen_arxiv[arxiv]
        elif title_key[0] and title_key in seen_title:
            dup_idx = seen_title[title_key]
        if dup_idx is not None:
            keep[dup_idx] = {**keep[dup_idx], **{k: v for k, v in e.items() if v is not None}}
            dropped += 1
            continue
        idx = len(keep)
        keep.append(e)
        if doi:
            seen_doi[doi] = idx
        if arxiv:
            seen_arxiv[arxiv] = idx
        if title_key[0]:
            seen_title[title_key] = idx
    catalog["entries"] = keep
    _save(proj, catalog)
    sys.stderr.write(f"Kept {len(keep)} entries, merged {dropped} duplicates.\n")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Lightweight validation without a jsonschema dependency."""
    proj = Path(args.project)
    catalog = _load(proj)
    errors: list[str] = []
    seen_keys: set[str] = set()
    for i, e in enumerate(catalog.get("entries", [])):
        ctx = f"entry[{i}]"
        for req in ("key", "title", "authors", "year", "status"):
            if e.get(req) in (None, "", []):
                errors.append(f"{ctx}: missing required field {req!r}")
        k = e.get("key", "")
        if k and not re.fullmatch(r"[a-z0-9]+", k):
            errors.append(f"{ctx}: key {k!r} must match ^[a-z0-9]+$")
        if k in seen_keys:
            errors.append(f"{ctx}: duplicate key {k!r}")
        seen_keys.add(k)
        if e.get("status") and e["status"] not in VALID_STATUS:
            errors.append(f"{ctx}: status {e['status']!r} not in {sorted(VALID_STATUS)}")
    if errors:
        for err in errors:
            sys.stderr.write(err + "\n")
        return 1
    sys.stderr.write(f"OK — {len(catalog.get('entries', []))} entries valid.\n")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Manage a lit-review project catalog.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("init", help="Create an empty catalog.")
    sp.add_argument("--project", required=True)
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("add", help="Add or update an entry.")
    sp.add_argument("--project", required=True)
    sp.add_argument("--key", required=True)
    sp.add_argument("--from-json", help="Search-result JSON to pull metadata from.")
    sp.add_argument("--match-doi", help="DOI to match within --from-json.")
    sp.add_argument("--match-arxiv", help="arXiv id to match within --from-json.")
    sp.add_argument("--match-title", help="Title to match within --from-json (loose).")
    sp.add_argument("--title")
    sp.add_argument("--authors", nargs="+")
    sp.add_argument("--year", type=int)
    sp.add_argument("--venue")
    sp.add_argument("--doi")
    sp.add_argument("--arxiv-id", dest="arxiv_id")
    sp.add_argument("--url")
    sp.add_argument("--pdf-url", dest="pdf_url")
    sp.add_argument("--pdf-path", dest="pdf_path")
    sp.add_argument("--summary-path", dest="summary_path")
    sp.add_argument("--status", choices=sorted(VALID_STATUS))
    sp.add_argument("--tags", nargs="+")
    sp.add_argument("--include-reason", dest="include_reason")
    sp.add_argument("--exclude-reason", dest="exclude_reason")
    sp.add_argument("--source")
    sp.add_argument("--abstract")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("list", help="List catalog entries.")
    sp.add_argument("--project", required=True)
    sp.add_argument("--status", choices=sorted(VALID_STATUS))
    sp.add_argument("--tag")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("get", help="Print one entry as JSON.")
    sp.add_argument("--project", required=True)
    sp.add_argument("--key", required=True)
    sp.set_defaults(func=cmd_get)

    sp = sub.add_parser("dedupe", help="Merge duplicate entries.")
    sp.add_argument("--project", required=True)
    sp.set_defaults(func=cmd_dedupe)

    sp = sub.add_parser("validate", help="Lightweight schema check.")
    sp.add_argument("--project", required=True)
    sp.set_defaults(func=cmd_validate)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
