"""Extract text from a downloaded PDF for agent reading.

Usage:
    python tools/pdf_to_text.py --key lewis2020rag --project projects/<slug>
    python tools/pdf_to_text.py --in foo.pdf --out foo.txt
    python tools/pdf_to_text.py --in foo.pdf --out foo.txt --backend pymupdf

Backends (auto-selected in this order unless `--backend` forces one):

    1. pymupdf     — best on two-column scientific PDFs; fast. AGPL.
    2. pdfplumber  — table-aware; MIT.
    3. pypdf       — guaranteed fallback (always installed); MIT.

The first backend whose import succeeds is used. Install PyMuPDF for the best
results on most scientific papers:

    pip install pymupdf
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

BACKEND_ORDER = ("pymupdf", "pdfplumber", "pypdf")


def _extract_pymupdf(pdf_path: Path) -> str:
    import fitz  # type: ignore  # PyMuPDF imports as `fitz`

    pages = []
    with fitz.open(str(pdf_path)) as doc:
        for i, page in enumerate(doc, start=1):
            try:
                # sort=True reorders text blocks by reading order, which is the
                # single biggest improvement over pypdf for two-column layouts.
                text = page.get_text("text", sort=True) or ""
            except Exception as exc:  # pragma: no cover
                text = f"[extraction error on page {i}: {exc}]"
            pages.append(f"\n\n===== page {i} =====\n\n{text}")
    return "".join(pages).strip() + "\n"


def _extract_pdfplumber(pdf_path: Path) -> str:
    import pdfplumber  # type: ignore

    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception as exc:  # pragma: no cover
                text = f"[extraction error on page {i}: {exc}]"
            pages.append(f"\n\n===== page {i} =====\n\n{text}")
    return "".join(pages).strip() + "\n"


def _extract_pypdf(pdf_path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # pragma: no cover
            text = f"[extraction error on page {i}: {exc}]"
        pages.append(f"\n\n===== page {i} =====\n\n{text}")
    return "".join(pages).strip() + "\n"


_BACKENDS: dict[str, Callable[[Path], str]] = {
    "pymupdf": _extract_pymupdf,
    "pdfplumber": _extract_pdfplumber,
    "pypdf": _extract_pypdf,
}


_BACKEND_IMPORT_NAME = {
    "pymupdf": "fitz",
    "pdfplumber": "pdfplumber",
    "pypdf": "pypdf",
}


def _pick_backend(requested: str) -> tuple[str, Callable[[Path], str]]:
    """Return (name, extractor). 'auto' tries each in BACKEND_ORDER."""
    if requested != "auto":
        fn = _BACKENDS.get(requested)
        if fn is None:
            raise ValueError(f"Unknown backend {requested!r}; choose from {list(_BACKENDS)}.")
        try:
            __import__(_BACKEND_IMPORT_NAME[requested])
        except ImportError as exc:
            raise ImportError(
                f"Backend {requested!r} requested but its package is not installed: {exc}"
            ) from exc
        return requested, fn

    last_err: Exception | None = None
    for name in BACKEND_ORDER:
        try:
            __import__(_BACKEND_IMPORT_NAME[name])
            return name, _BACKENDS[name]
        except ImportError as exc:
            last_err = exc
            continue
    raise ImportError(
        "No PDF extraction backend is installed. Install at least one: "
        "`pip install pymupdf` (recommended), `pip install pdfplumber`, or "
        "`pip install pypdf` (already in requirements.txt). "
        f"Last import error: {last_err}"
    )


def extract(pdf_path: Path, backend: str = "auto") -> tuple[str, str]:
    """Extract text from `pdf_path`. Returns (text, backend_name_used)."""
    name, fn = _pick_backend(backend)
    return fn(pdf_path), name


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Extract text from a PDF.")
    p.add_argument("--key", help="Catalog key (requires --project).")
    p.add_argument("--project", help="Project directory.")
    p.add_argument("--in", dest="in_path", help="Input PDF path.")
    p.add_argument("--out", help="Output text path.")
    p.add_argument(
        "--backend",
        choices=["auto", *_BACKENDS.keys()],
        default="auto",
        help="Force a specific extraction backend (default: auto).",
    )
    args = p.parse_args(argv)

    if args.key:
        if not args.project:
            p.error("--key requires --project")
        proj = Path(args.project)
        pdf_path = proj / "papers" / f"{args.key}.pdf"
        out_path = proj / "papers" / ".text" / f"{args.key}.txt"
    else:
        if not args.in_path or not args.out:
            p.error("Provide --in and --out, or --key and --project.")
        pdf_path = Path(args.in_path)
        out_path = Path(args.out)

    if not pdf_path.exists():
        sys.stderr.write(f"PDF not found: {pdf_path}\n")
        return 1

    try:
        text, backend_used = extract(pdf_path, backend=args.backend)
    except ImportError as exc:
        sys.stderr.write(f"{exc}\n")
        return 2
    except Exception as exc:
        sys.stderr.write(f"Extraction failed: {exc}\n")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    sys.stderr.write(f"Wrote {len(text)} chars to {out_path} (backend: {backend_used})\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
