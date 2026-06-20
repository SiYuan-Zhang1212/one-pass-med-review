from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal

Outcome = Literal["correct", "wrong", "unknown"]
EvidenceKind = Literal["prompt", "answer", "explanation", "other"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(slots=True)
class SessionRecord:
    id: int | None = None
    title: str = ""
    source: str = ""
    notes: str = ""
    created_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class QuestionRecord:
    id: int | None = None
    session_id: int | None = None
    stem: str = ""
    options: list[str] = field(default_factory=list)
    selected_answer: str | None = None
    correct_answer: str | None = None
    outcome: Outcome = "unknown"
    explanation: str = ""
    ai_summary: str = ""
    tags: list[str] = field(default_factory=list)
    question_hash: str = ""
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class EvidenceRecord:
    id: int | None = None
    question_id: int | None = None
    kind: EvidenceKind = "other"
    path: str = ""
    sha256: str = ""
    created_at: str = field(default_factory=utc_now)
