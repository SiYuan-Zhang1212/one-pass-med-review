from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .hashing import file_sha256, question_hash
from .models import EvidenceKind, EvidenceRecord, Outcome, QuestionRecord, SessionRecord, utc_now


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT '',
  notes TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  stem TEXT NOT NULL,
  options_json TEXT NOT NULL DEFAULT '[]',
  selected_answer TEXT,
  correct_answer TEXT,
  outcome TEXT NOT NULL CHECK (outcome IN ('correct', 'wrong', 'unknown')),
  explanation TEXT NOT NULL DEFAULT '',
  ai_summary TEXT NOT NULL DEFAULT '',
  tags_json TEXT NOT NULL DEFAULT '[]',
  question_hash TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(session_id, question_hash)
);

CREATE TABLE IF NOT EXISTS evidence (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
  kind TEXT NOT NULL CHECK (kind IN ('prompt', 'answer', 'explanation', 'other')),
  path TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  created_at TEXT NOT NULL
);
"""


class ReviewStore:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)

    def connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)

    def create_session(self, title: str, source: str = "", notes: str = "") -> int:
        if not title.strip():
            raise ValueError("session title is required")

        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO sessions (title, source, notes, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (title.strip(), source.strip(), notes.strip(), utc_now()),
            )
            return int(cursor.lastrowid)

    def get_session(self, session_id: int) -> SessionRecord:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM sessions WHERE id = ?",
                (session_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"session not found: {session_id}")
        return _session_from_row(row)

    def upsert_question(self, record: QuestionRecord) -> int:
        if record.session_id is None:
            raise ValueError("session_id is required")
        if not record.stem.strip():
            raise ValueError("question stem is required")

        now = utc_now()
        q_hash = record.question_hash or question_hash(record.stem, record.options)
        created_at = record.created_at or now

        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO questions (
                  session_id,
                  stem,
                  options_json,
                  selected_answer,
                  correct_answer,
                  outcome,
                  explanation,
                  ai_summary,
                  tags_json,
                  question_hash,
                  created_at,
                  updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(session_id, question_hash) DO UPDATE SET
                  stem = excluded.stem,
                  options_json = excluded.options_json,
                  selected_answer = excluded.selected_answer,
                  correct_answer = excluded.correct_answer,
                  outcome = excluded.outcome,
                  explanation = excluded.explanation,
                  ai_summary = excluded.ai_summary,
                  tags_json = excluded.tags_json,
                  updated_at = excluded.updated_at
                """,
                (
                    record.session_id,
                    record.stem.strip(),
                    json.dumps(record.options, ensure_ascii=False),
                    record.selected_answer,
                    record.correct_answer,
                    record.outcome,
                    record.explanation.strip(),
                    record.ai_summary.strip(),
                    json.dumps(record.tags, ensure_ascii=False),
                    q_hash,
                    created_at,
                    now,
                ),
            )
            row = connection.execute(
                """
                SELECT id FROM questions
                WHERE session_id = ? AND question_hash = ?
                """,
                (record.session_id, q_hash),
            ).fetchone()

        if row is None:
            raise RuntimeError("question upsert failed")
        return int(row["id"])

    def add_evidence(
        self,
        question_id: int,
        path: str | Path,
        kind: EvidenceKind = "other",
    ) -> int:
        evidence_path = Path(path)
        if not evidence_path.exists():
            raise FileNotFoundError(evidence_path)

        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO evidence (question_id, kind, path, sha256, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    question_id,
                    kind,
                    str(evidence_path),
                    file_sha256(str(evidence_path)),
                    utc_now(),
                ),
            )
            return int(cursor.lastrowid)

    def list_questions(self, session_id: int) -> list[QuestionRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM questions
                WHERE session_id = ?
                ORDER BY created_at, id
                """,
                (session_id,),
            ).fetchall()
        return [_question_from_row(row) for row in rows]

    def list_evidence(self, question_id: int) -> list[EvidenceRecord]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM evidence
                WHERE question_id = ?
                ORDER BY created_at, id
                """,
                (question_id,),
            ).fetchall()
        return [_evidence_from_row(row) for row in rows]


def _loads_list(value: str) -> list[Any]:
    loaded = json.loads(value or "[]")
    if not isinstance(loaded, list):
        return []
    return loaded


def _session_from_row(row: sqlite3.Row) -> SessionRecord:
    return SessionRecord(
        id=int(row["id"]),
        title=str(row["title"]),
        source=str(row["source"]),
        notes=str(row["notes"]),
        created_at=str(row["created_at"]),
    )


def _question_from_row(row: sqlite3.Row) -> QuestionRecord:
    return QuestionRecord(
        id=int(row["id"]),
        session_id=int(row["session_id"]),
        stem=str(row["stem"]),
        options=[str(item) for item in _loads_list(str(row["options_json"]))],
        selected_answer=row["selected_answer"],
        correct_answer=row["correct_answer"],
        outcome=row["outcome"] if row["outcome"] in ("correct", "wrong", "unknown") else "unknown",
        explanation=str(row["explanation"]),
        ai_summary=str(row["ai_summary"]),
        tags=[str(item) for item in _loads_list(str(row["tags_json"]))],
        question_hash=str(row["question_hash"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _evidence_from_row(row: sqlite3.Row) -> EvidenceRecord:
    return EvidenceRecord(
        id=int(row["id"]),
        question_id=int(row["question_id"]),
        kind=row["kind"] if row["kind"] in ("prompt", "answer", "explanation", "other") else "other",
        path=str(row["path"]),
        sha256=str(row["sha256"]),
        created_at=str(row["created_at"]),
    )


def validate_outcome(value: str) -> Outcome:
    if value not in ("correct", "wrong", "unknown"):
        raise ValueError("outcome must be correct, wrong, or unknown")
    return value  # type: ignore[return-value]
