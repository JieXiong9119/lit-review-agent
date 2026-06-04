"""Extract text from a downloaded PDF for agent reading.

Usage:
    python tools/pdf_to_text.py --key lewis2020rag --project projects/<slug>
    python tools/pdf_to_text.py --in foo.pdf --out foo.txt
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(
        "Missing dependency 'pypdf'. Install with: pip install -r tools/requirements.txt\n"
    )
    raise SystemExit(1) from exc


def extract(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:  # pragma: no cover
            text = f"[extraction error on page {i}: {exc}]"
        pages.append(f"\n\n===== page {i} =====\n\n{text}")
    return "".join(pages).strip() + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Extract text from a PDF.")
    p.add_argument("--key", help="Catalog key (requires --project).")
    p.add_argument("--project", help="Project directory.")
    p.add_argument("--in", dest="in_path", help="Input PDF path.")
    p.add_argument("--out", help="Output text path.")
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
        text = extract(pdf_path)
    except Exception as exc:
        sys.stderr.write(f"Extraction failed: {exc}\n")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    sys.stderr.write(f"Wrote {len(text)} chars to {out_path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
