"""Shared helpers for lit-review-agent tools.

Defines the common normalized record schema every search backend emits, plus
small utilities for safe HTTP, JSON I/O, and atomic file writes.

Kept deliberately small and dependency-light: only `requests` from third-party.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    import requests
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(
        "Missing dependency 'requests'. Install with: pip install -r tools/requirements.txt\n"
    )
    raise SystemExit(1) from exc

# Opportunistically use the OS certificate trust store so corporate
# SSL-intercepting proxies (which install their own root CA into the OS store)
# work without manual REQUESTS_CA_BUNDLE configuration. truststore is optional;
# if not installed we fall back to certifi's bundle (the requests default).
if os.environ.get("LIT_REVIEW_DISABLE_TRUSTSTORE") != "1":
    try:
        import truststore  # type: ignore

        truststore.inject_into_ssl()
    except ImportError:
        pass


USER_AGENT = "lit-review-agent/0.1 (+https://github.com/jxiong/lit-review-agent)"
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_SLEEP = 1.0  # seconds between paginated requests


@dataclass
class PaperRecord:
    """Normalized cross-backend paper record.

    Every search_*.py emits a list of these as JSON.
    """

    source: str  # arxiv | openalex | semantic_scholar | crossref | scholar | user
    id: str | None = None  # backend-native id (arxiv id, openalex W..., S2 paperId)
    doi: str | None = None
    title: str = ""
    authors: list[str] = field(default_factory=list)
    year: int | None = None
    venue: str | None = None
    abstract: str | None = None
    url: str | None = None
    pdf_url: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def http_get(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> requests.Response:
    """GET with sane defaults: User-Agent, timeout, raise_for_status."""
    merged_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        merged_headers.update(headers)
    resp = requests.get(url, params=params, headers=merged_headers, timeout=timeout)
    resp.raise_for_status()
    return resp


def write_json(path: str | os.PathLike[str], data: Any) -> None:
    """Atomic JSON write: write to a temp file in the same dir, then rename."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=p.name + ".", dir=str(p.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, p)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def read_json(path: str | os.PathLike[str]) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def emit_records(records: Iterable[PaperRecord], out_path: str | None) -> None:
    """Write records to `out_path` if given, else pretty-print to stdout."""
    payload = [r.to_dict() for r in records]
    if out_path:
        write_json(out_path, payload)
        sys.stderr.write(f"Wrote {len(payload)} records to {out_path}\n")
    else:
        json.dump(payload, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")


def polite_sleep(seconds: float = DEFAULT_SLEEP) -> None:
    if seconds > 0:
        time.sleep(seconds)


def normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = doi.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi or None


def safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
