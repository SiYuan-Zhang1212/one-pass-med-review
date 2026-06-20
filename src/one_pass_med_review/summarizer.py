from __future__ import annotations

from .models import QuestionRecord


class RuleBasedSummarizer:
    """Small local fallback until an AI provider is configured."""

    def summarize(self, question: QuestionRecord) -> str:
        if question.ai_summary:
            return question.ai_summary

        key = _first_sentence(question.explanation) or _first_sentence(question.stem)
        if question.outcome == "wrong":
            return f"错题：{key}" if key else "错题：补充错因和正确思路。"
        if question.outcome == "correct":
            return f"掌握：{key}" if key else "掌握：保留一句话知识点。"
        return key or "待整理：补充题目结论。"


def _first_sentence(value: str) -> str:
    cleaned = " ".join((value or "").split())
    if not cleaned:
        return ""
    for separator in ("。", ".", "；", ";"):
        if separator in cleaned:
            return cleaned.split(separator, 1)[0].strip()
    return cleaned[:80].strip()
