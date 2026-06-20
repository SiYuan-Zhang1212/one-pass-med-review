from one_pass_med_review.hashing import normalize_text, question_hash


def test_normalize_text_collapses_space_and_width() -> None:
    assert normalize_text("  Ａ  B\nC  ") == "a b c"


def test_question_hash_is_stable_for_spacing() -> None:
    left = question_hash("患者 发热", ["A", "B"])
    right = question_hash(" 患者\n发热 ", [" A ", "B"])
    assert left == right
