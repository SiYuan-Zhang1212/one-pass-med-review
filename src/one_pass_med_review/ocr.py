from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class OCRBlock:
    text: str
    confidence: float | None = None


@dataclass(frozen=True, slots=True)
class OCRResult:
    text: str
    blocks: list[OCRBlock] = field(default_factory=list)


class OCRProvider(Protocol):
    def extract_text(self, image_path: str | Path) -> OCRResult:
        ...


class NullOCRProvider:
    """Placeholder provider for the manual MVP."""

    def extract_text(self, image_path: str | Path) -> OCRResult:
        return OCRResult(text="", blocks=[])


def get_ocr_provider(name: str) -> OCRProvider:
    normalized = (name or "null").strip().lower()
    if normalized == "null":
        return NullOCRProvider()
    raise ValueError(f"unknown OCR provider: {name}")
