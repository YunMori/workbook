"""채점 로직.

- 객관식: 선택 번호와 정답 번호 비교
- 주관식: 정규화 후 완전 일치 → 실패 시 키워드 그룹 매칭
- 서술형: 자동 채점하지 않음(is_correct=None). 사용자가 채점 기준표를 보고 자기채점한다.
"""

import re
import unicodedata
from decimal import Decimal

from .models import GradedBy, QuestionType

# 정규화 시 제거하는 문자: 백틱/따옴표/괄호/구두점 등 표기 흔들림
_STRIP_CHARS = re.compile(r"[`'\"“”‘’(){}\[\]<>.,!?;:·・…\-_/\\|]+")
_WHITESPACE = re.compile(r"\s+")


def normalize(text):
    """비교용 정규화: 전각→반각, 소문자화, 구두점·공백 제거."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", str(text)).lower()
    text = _STRIP_CHARS.sub(" ", text)
    return _WHITESPACE.sub("", text).strip()


def normalize_loose(text):
    """키워드 포함 검사용: 공백은 남겨 두고 구두점만 제거."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", str(text)).lower()
    text = _STRIP_CHARS.sub(" ", text)
    return _WHITESPACE.sub(" ", text).strip()


def grade_multiple_choice(selected_choice, question):
    return selected_choice is not None and selected_choice == question.correct_choice_number


def grade_short_answer(text_answer, solution):
    """정답 후보 완전 일치 또는 키워드 그룹 전부 포함이면 정답."""
    if not text_answer or not text_answer.strip() or solution is None:
        return False

    submitted = normalize(text_answer)
    if submitted and any(normalize(a) == submitted for a in (solution.accepted_answers or [])):
        return True

    loose = normalize_loose(text_answer)
    for group in solution.required_keywords or []:
        keywords = group if isinstance(group, (list, tuple)) else [group]
        if keywords and all(normalize_loose(k) in loose for k in keywords):
            return True
    return False


def grade_answer(answer):
    """AttemptAnswer 하나를 채점해 is_correct/awarded_points를 채운다(저장은 하지 않음)."""
    question = answer.question
    solution = getattr(question, "solution", None)

    if question.qtype == QuestionType.MULTIPLE_CHOICE:
        answer.is_correct = grade_multiple_choice(answer.selected_choice, question)
    elif question.qtype == QuestionType.SHORT_ANSWER:
        answer.is_correct = grade_short_answer(answer.text_answer, solution)
    else:  # 서술형 — 자기채점 대상
        answer.is_correct = None

    answer.awarded_points = question.points if answer.is_correct else Decimal("0")
    answer.graded_by = GradedBy.AUTO
    return answer


def recalculate_scores(attempt):
    """자동 채점 점수와 자기채점 점수를 다시 합산해 저장한다."""
    auto = Decimal("0")
    self_graded = Decimal("0")
    for answer in attempt.answers.all():
        if answer.graded_by == GradedBy.SELF:
            self_graded += answer.awarded_points
        else:
            auto += answer.awarded_points
    attempt.auto_score = auto
    attempt.self_score = self_graded
    attempt.save(update_fields=["auto_score", "self_score"])
    return attempt


def grade_attempt(attempt):
    """제출된 응시 전체를 채점한다."""
    answers = list(
        attempt.answers.select_related("question", "question__solution").prefetch_related(
            "question__choices"
        )
    )
    for answer in answers:
        grade_answer(answer)
    if answers:
        type(answers[0]).objects.bulk_update(
            answers, ["is_correct", "awarded_points", "graded_by"]
        )
    return recalculate_scores(attempt)
