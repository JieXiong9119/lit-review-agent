"""Download a PDF for a catalog entry.

Usage:
    # By catalog key (uses pdf_url from catalog.json):
    python tools/fetch_pdf.py --key lewis2020rag --project projects/<slug>

    # Ad-hoc URL (does not touch catalog):
    python tools/fetch_pdf.py --url https://arxiv.org/pdf/2005.11401.pdf \
        --out /tmp/foo.pdf
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import requests

from _common import USER_AGENT, read_json, write_json

CHUNK_SIZE = 1 << 15  # 32 KB


def fetch(url: str, dest: Path, timeout: int = 60) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": USER_AGENT, "Accept": "application/pdf"}
    with requests.get(url, headers=headers, timeout=timeout, stream=True) as resp:
        resp.raise_for_status()
        ctype = resp.headers.get("Content-Type", "")
        if "pdf" not in ctype.lower() and not url.lower().endswith(".pdf"):
            sys.stderr.write(
                f"WARNING: response Content-Type is {ctype!r}, not PDF. "
                "Saving anyway; verify manually.\n"
            )
        size = 0
        with open(dest, "wb") as fh:
            for chunk in resp.iter_content(CHUNK_SIZE):
                if chunk:
                    fh.write(chunk)
                    size += len(chunk)
    return size


def fetch_by_key(project_dir: Path, key: str) -> int:
    catalog_path = project_dir / "catalog.json"
    if not catalog_path.exists():
        raise FileNotFoundError(f"No catalog at {catalog_path}")
    catalog = read_json(catalog_path)
    entries = catalog.get("entries", [])
    entry = next((e for e in entries if e.get("key") == key), None)
    if entry is None:
        raise KeyError(f"Key {key!r} not in {catalog_path}")
    url = entry.get("pdf_url") or entry.get("url")
    if not url:
        raise ValueError(f"Entry {key!r} has no pdf_url or url.")
    dest = project_dir / "papers" / f"{key}.pdf"
    size = fetch(url, dest)
    entry["pdf_path"] = f"papers/{key}.pdf"
    write_json(catalog_path, catalog)
    sys.stderr.write(f"Downloaded {size} bytes to {dest}\n")
    return size


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Download a PDF.")
    p.add_argument("--key", help="Catalog key (requires --project).")
    p.add_argument("--project", help="Project directory (e.g., projects/<slug>).")
    p.add_argument("--url", help="Direct PDF URL (with --out).")
    p.add_argument("--out", help="Output path for --url mode.")
    args = p.parse_args(argv)

    try:
        if args.key:
            if not args.project:
                p.error("--key requires --project")
            fetch_by_key(Path(args.project), args.key)
        elif args.url:
            if not args.out:
                p.error("--url requires --out")
            size = fetch(args.url, Path(args.out))
            sys.stderr.write(f"Downloaded {size} bytes to {args.out}\n")
        else:
            p.error("Provide either --key (+--project) or --url (+--out).")
    except Exception as exc:
        sys.stderr.write(f"Fetch failed: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
