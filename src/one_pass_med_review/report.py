from __future__ import annotations

from collections import Counter

from .models import QuestionRecord, SessionRecord


def render_session_report(session: SessionRecord, questions: list[QuestionRecord]) -> str:
    counts = Counter(question.outcome for question in questions)
    wrong = [question for question in questions if question.outcome == "wrong"]
    correct = [question for question in questions if question.outcome == "correct"]
    unknown = [question for question in questions if question.outcome == "unknown"]

    lines: list[str] = [
        f"# {session.title}",
        "",
        f"- Source: {session.source or 'unspecified'}",
        f"- Created: {session.created_at}",
        f"- Total: {len(questions)}",
        f"- Correct: {counts['correct']}",
        f"- Wrong: {counts['wrong']}",
        f"- Unknown: {counts['unknown']}",
        "",
    ]

    if session.notes:
        lines.extend(["## Notes", "", session.notes, ""])

    lines.extend(["## Wrong Questions", ""])
    if wrong:
        for index, question in enumerate(wrong, start=1):
            lines.extend(_render_question(index, question, include_full=True))
    else:
        lines.extend(["No wrong questions recorded.", ""])

    lines.extend(["## Correct Question Summaries", ""])
    if correct:
        for index, question in enumerate(correct, start=1):
            summary = question.ai_summary or "No summary yet."
            tags = _format_tags(question.tags)
            lines.append(f"{index}. {summary}{tags}")
        lines.append("")
    else:
        lines.extend(["No correct questions recorded.", ""])

    if unknown:
        lines.extend(["## Unknown Outcome", ""])
        for index, question in enumerate(unknown, start=1):
            lines.extend(_render_question(index, question, include_full=False))

    return "\n".join(lines).rstrip() + "\n"


def _render_question(index: int, question: QuestionRecord, include_full: bool) -> list[str]:
    lines = [f"### {index}. {question.ai_summary or 'Untitled question'}", ""]

    if include_full:
        lines.extend(
            [
                "**Stem**",
                "",
                question.stem,
                "",
            ]
        )
        if question.options:
            lines.extend(["**Options**", ""])
            lines.extend(f"- {option}" for option in question.options)
            lines.append("")

    lines.extend(
        [
            f"- Selected: {question.selected_answer or 'unknown'}",
            f"- Correct: {question.correct_answer or 'unknown'}",
        ]
    )
    if question.tags:
        lines.append(f"- Tags: {', '.join(question.tags)}")
    if question.explanation:
        lines.extend(["", "**Explanation**", "", question.explanation])
    lines.append("")
    return lines


def _format_tags(tags: list[str]) -> str:
    if not tags:
        return ""
    return f" ({', '.join(tags)})"
