from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .models import QuestionRecord
from .report import render_session_report
from .storage import ReviewStore, validate_outcome
from .summarizer import RuleBasedSummarizer


def default_db_path() -> Path:
    return Path(".onepass-med-review") / "review.sqlite3"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="onepass")
    parser.add_argument(
        "--db",
        default=str(default_db_path()),
        help="SQLite database path. Defaults to .onepass-med-review/review.sqlite3.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the local SQLite database.")

    new_session = subparsers.add_parser("new-session", help="Create a practice session.")
    new_session.add_argument("--title", required=True)
    new_session.add_argument("--source", default="")
    new_session.add_argument("--notes", default="")

    add_question = subparsers.add_parser("add-question", help="Add or update a question record.")
    add_question.add_argument("--session-id", required=True, type=int)
    add_question.add_argument("--stem")
    add_question.add_argument("--stem-file")
    add_question.add_argument("--options-json", default="[]")
    add_question.add_argument("--selected-answer")
    add_question.add_argument("--correct-answer")
    add_question.add_argument("--outcome", choices=["correct", "wrong", "unknown"], default="unknown")
    add_question.add_argument("--explanation")
    add_question.add_argument("--explanation-file")
    add_question.add_argument("--summary")
    add_question.add_argument("--tags", default="", help="Comma-separated tags.")
    add_question.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="Optional evidence file path. Can be provided more than once.",
    )

    report = subparsers.add_parser("report", help="Render a Markdown report for a session.")
    report.add_argument("--session-id", required=True, type=int)
    report.add_argument("--output")

    subparsers.add_parser("demo", help="Create a temporary demo session and print a report.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = ReviewStore(args.db)

    if args.command == "init":
        store.initialize()
        print(f"Initialized {store.db_path}")
        return 0

    if args.command == "new-session":
        store.initialize()
        session_id = store.create_session(args.title, source=args.source, notes=args.notes)
        print(session_id)
        return 0

    if args.command == "add-question":
        store.initialize()
        question = _question_from_args(args)
        summarizer = RuleBasedSummarizer()
        if not question.ai_summary:
            question.ai_summary = summarizer.summarize(question)
        question_id = store.upsert_question(question)
        for evidence_path in args.evidence:
            store.add_evidence(question_id, evidence_path)
        print(question_id)
        return 0

    if args.command == "report":
        store.initialize()
        session = store.get_session(args.session_id)
        questions = store.list_questions(args.session_id)
        rendered = render_session_report(session, questions)
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
            print(output_path)
        else:
            print(rendered, end="")
        return 0

    if args.command == "demo":
        return _run_demo(store)

    parser.error(f"unknown command: {args.command}")
    return 2


def _question_from_args(args: argparse.Namespace) -> QuestionRecord:
    stem = _read_text_arg(args.stem, args.stem_file)
    explanation = _read_text_arg(args.explanation, args.explanation_file)
    options = _parse_options(args.options_json)
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    return QuestionRecord(
        session_id=args.session_id,
        stem=stem,
        options=options,
        selected_answer=args.selected_answer,
        correct_answer=args.correct_answer,
        outcome=validate_outcome(args.outcome),
        explanation=explanation,
        ai_summary=args.summary or "",
        tags=tags,
    )


def _read_text_arg(value: str | None, file_path: str | None) -> str:
    if value is not None:
        return value
    if file_path:
        return Path(file_path).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def _parse_options(value: str) -> list[str]:
    parsed = json.loads(value)
    if not isinstance(parsed, list) or not all(isinstance(item, str) for item in parsed):
        raise ValueError("--options-json must be a JSON array of strings")
    return parsed


def _run_demo(store: ReviewStore) -> int:
    store.initialize()
    session_id = store.create_session("Demo session", source="manual demo")
    summarizer = RuleBasedSummarizer()

    questions = [
        QuestionRecord(
            session_id=session_id,
            stem="患者突发胸痛，心电图提示ST段抬高，首要处理是什么？",
            options=["观察随访", "尽快再灌注治疗", "单纯止痛", "抗过敏治疗"],
            selected_answer="观察随访",
            correct_answer="尽快再灌注治疗",
            outcome="wrong",
            explanation="ST段抬高型心肌梗死的核心处理是尽快恢复冠脉血流。",
            tags=["心血管", "急诊"],
        ),
        QuestionRecord(
            session_id=session_id,
            stem="缺铁性贫血最常见的血象特点是什么？",
            options=["小细胞低色素", "大细胞性贫血", "正细胞正色素", "红细胞增多"],
            selected_answer="小细胞低色素",
            correct_answer="小细胞低色素",
            outcome="correct",
            explanation="缺铁性贫血典型表现为小细胞低色素性贫血。",
            tags=["血液"],
        ),
    ]
    for question in questions:
        question.ai_summary = summarizer.summarize(question)
        store.upsert_question(question)

    session = store.get_session(session_id)
    rendered = render_session_report(session, store.list_questions(session_id))
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
