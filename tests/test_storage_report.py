from one_pass_med_review.models import QuestionRecord
from one_pass_med_review.report import render_session_report
from one_pass_med_review.storage import ReviewStore


def test_store_round_trip_and_report(tmp_path) -> None:
    store = ReviewStore(tmp_path / "review.sqlite3")
    store.initialize()
    session_id = store.create_session("Test run", source="unit test")
    question_id = store.upsert_question(
        QuestionRecord(
            session_id=session_id,
            stem="缺铁性贫血最常见的血象特点是什么？",
            options=["小细胞低色素", "大细胞性贫血"],
            selected_answer="小细胞低色素",
            correct_answer="小细胞低色素",
            outcome="correct",
            explanation="缺铁性贫血典型表现为小细胞低色素性贫血。",
            ai_summary="掌握：缺铁性贫血是小细胞低色素。",
            tags=["血液"],
        )
    )

    assert question_id > 0
    questions = store.list_questions(session_id)
    assert len(questions) == 1
    assert questions[0].outcome == "correct"

    report = render_session_report(store.get_session(session_id), questions)
    assert "# Test run" in report
    assert "掌握：缺铁性贫血是小细胞低色素。" in report
