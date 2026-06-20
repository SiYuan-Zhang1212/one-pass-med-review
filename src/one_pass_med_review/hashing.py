from __future__ import annotations

import hashlib
import re
import unicodedata


_SPACE_RE = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    """Normalize OCR text enough for deduplication without changing meaning."""
    normalized = unicodedata.normalize("NFKC", value or "")
    normalized = normalized.strip().lower()
    return _SPACE_RE.sub(" ", normalized)


def question_hash(stem: str, options: list[str] | tuple[str, ...] = ()) -> str:
    parts = [normalize_text(stem)]
    parts.extend(normalize_text(option) for option in options)
    payload = "\n".join(part for part in parts if part)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
