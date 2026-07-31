import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework.test import APIClient

from exams.grading import grade_short_answer, normalize
from exams.models import (
    Attempt,
    AttemptAnswer,
    Choice,
    Exam,
    GradedBy,
    Question,
    QuestionType,
    Solution,
)


class NormalizeTests(TestCase):
    def test_ignores_formatting_noise(self):
        self.assertEqual(normalize("`RouterLink`"), normalize("RouterLink"))
        self.assertEqual(normalize(" router link "), normalize("routerlink"))
        self.assertEqual(normalize("LIFO."), normalize("lifo"))


class ShortAnswerGradingTests(TestCase):
    def setUp(self):
        exam = Exam.objects.create(title="t", round=9, version=1)
        self.question = Question.objects.create(
            exam=exam, number=1, qtype=QuestionType.SHORT_ANSWER, body="q", points=4
        )
        self.solution = Solution.objects.create(
            question=self.question,
            accepted_answers=["RouterLink / RouterView"],
            required_keywords=[["RouterLink", "RouterView"]],
        )

    def test_exact_match_ignoring_formatting(self):
        self.assertTrue(grade_short_answer("`RouterLink` / `RouterView`", self.solution))

    def test_keyword_group_match_in_any_order(self):
        self.assertTrue(grade_short_answer("RouterView 와 RouterLink 입니다", self.solution))

    def test_partial_keyword_match_is_wrong(self):
        self.assertFalse(grade_short_answer("RouterLink", self.solution))

    def test_blank_is_wrong(self):
        self.assertFalse(grade_short_answer("   ", self.solution))


class AttemptFlowTests(TestCase):
    """응시 → 채점 → 자기채점까지의 API 흐름."""

    def setUp(self):
        self.client = APIClient()
        self.exam = Exam.objects.create(title="2차 V9", round=9, version=1, total_score=10)

        self.mc = Question.objects.create(
            exam=self.exam, number=1, qtype=QuestionType.MULTIPLE_CHOICE, body="객관식", points=3
        )
        for number in range(1, 5):
            Choice.objects.create(
                question=self.mc, number=number, text=f"보기{number}", is_correct=number == 2
            )
        Solution.objects.create(question=self.mc, explanation="정답은 ②")

        self.short = Question.objects.create(
            exam=self.exam, number=2, qtype=QuestionType.SHORT_ANSWER, body="주관식", points=4
        )
        Solution.objects.create(
            question=self.short, accepted_answers=["state"], required_keywords=[["state"]]
        )

        self.essay = Question.objects.create(
            exam=self.exam, number=3, qtype=QuestionType.ESSAY, body="서술형", points=3
        )
        Solution.objects.create(
            question=self.essay,
            model_answer="모범 답안",
            rubric=[{"points": 3, "criteria": "핵심"}],
        )

    def test_exam_detail_hides_answers_by_default(self):
        response = self.client.get(f"/api/exams/{self.exam.id}/")
        payload = response.json()
        body = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("is_correct", body)
        self.assertNotIn("solution", body)
        self.assertNotIn("correct_choice", body)
        self.assertEqual(len(payload["questions"]), 3)

    def test_exam_detail_with_solutions_includes_answers(self):
        response = self.client.get(f"/api/exams/{self.exam.id}/?with_solutions=1")
        question = response.json()["questions"][0]
        self.assertEqual(question["correct_choice"], 2)
        self.assertEqual(question["solution"]["explanation"], "정답은 ②")

    def test_submit_grades_automatically(self):
        attempt = Attempt.objects.create(exam=self.exam)
        response = self.client.post(
            f"/api/attempts/{attempt.id}/submit/",
            {
                "elapsed_sec": 120,
                "answers": [
                    {"question": self.mc.id, "selected_choice": 2},
                    {"question": self.short.id, "text_answer": "`state`"},
                    {"question": self.essay.id, "text_answer": "제 답안입니다."},
                ],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()

        self.assertEqual(Decimal(payload["auto_score"]), Decimal("7.0"))  # 3 + 4
        self.assertEqual(Decimal(payload["self_score"]), Decimal("0.0"))
        results = {a["question"]["number"]: a for a in payload["answers"]}
        self.assertTrue(results[1]["is_correct"])
        self.assertTrue(results[2]["is_correct"])
        self.assertIsNone(results[3]["is_correct"])  # 서술형은 자기채점 대상
        self.assertEqual(results[3]["question"]["solution"]["model_answer"], "모범 답안")

    def test_wrong_mc_scores_zero(self):
        attempt = Attempt.objects.create(exam=self.exam)
        response = self.client.post(
            f"/api/attempts/{attempt.id}/submit/",
            {"answers": [{"question": self.mc.id, "selected_choice": 3}]},
            format="json",
        )
        self.assertEqual(Decimal(response.json()["auto_score"]), Decimal("0.0"))

    def test_self_grading_updates_total(self):
        attempt = Attempt.objects.create(exam=self.exam)
        self.client.post(
            f"/api/attempts/{attempt.id}/submit/",
            {"answers": [{"question": self.essay.id, "text_answer": "답안"}]},
            format="json",
        )
        answer = AttemptAnswer.objects.get(attempt=attempt, question=self.essay)

        response = self.client.patch(
            f"/api/attempt-answers/{answer.id}/",
            {"is_correct": True, "awarded_points": "2.0"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["graded_by"], GradedBy.SELF)
        self.assertEqual(Decimal(payload["self_score"]), Decimal("2.0"))
        self.assertEqual(Decimal(payload["total_points"]), Decimal("2.0"))

    def test_self_grading_rejects_points_above_max(self):
        attempt = Attempt.objects.create(exam=self.exam)
        self.client.post(
            f"/api/attempts/{attempt.id}/submit/",
            {"answers": [{"question": self.essay.id, "text_answer": "답안"}]},
            format="json",
        )
        answer = AttemptAnswer.objects.get(attempt=attempt, question=self.essay)
        response = self.client.patch(
            f"/api/attempt-answers/{answer.id}/", {"awarded_points": "99"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_history_requires_token_and_returns_own_attempts(self):
        attempt = Attempt.objects.create(exam=self.exam)
        self.client.post(
            f"/api/attempts/{attempt.id}/submit/",
            {"answers": [{"question": self.mc.id, "selected_choice": 2}]},
            format="json",
        )
        self.assertEqual(self.client.get("/api/attempts/").status_code, 400)

        response = self.client.get(f"/api/attempts/?token={attempt.token}")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(self.client.get(f"/api/attempts/?token={Attempt().token}").json(), [])

    def test_double_submit_is_rejected(self):
        attempt = Attempt.objects.create(exam=self.exam)
        payload = {"answers": [{"question": self.mc.id, "selected_choice": 2}]}
        self.client.post(f"/api/attempts/{attempt.id}/submit/", payload, format="json")
        second = self.client.post(f"/api/attempts/{attempt.id}/submit/", payload, format="json")
        self.assertEqual(second.status_code, 400)

    def test_answers_from_other_exams_are_ignored(self):
        other_exam = Exam.objects.create(title="다른 시험", round=9, version=2)
        foreign = Question.objects.create(
            exam=other_exam, number=1, qtype=QuestionType.MULTIPLE_CHOICE, body="x", points=3
        )
        attempt = Attempt.objects.create(exam=self.exam)
        response = self.client.post(
            f"/api/attempts/{attempt.id}/submit/",
            {
                "answers": [
                    {"question": self.mc.id, "selected_choice": 2},
                    {"question": foreign.id, "selected_choice": 1},
                ]
            },
            format="json",
        )
        self.assertEqual(len(response.json()["answers"]), 1)


class AdminSessionTests(TestCase):
    """배포 환경은 SPA와 admin이 같은 오리진이라 admin 세션 쿠키가 /api/에도 실려 온다.

    DRF가 그 쿠키로 로그인 상태를 인식하면 CSRF 토큰을 요구해 응시 시작이 403으로 막힌다.
    """

    def setUp(self):
        self.exam = Exam.objects.create(title="세션 시험", round=8, version=1)
        User.objects.create_superuser("admin", "admin@example.com", "pw-for-test-1234")

    def test_start_attempt_while_logged_into_admin(self):
        client = Client(enforce_csrf_checks=True)
        client.login(username="admin", password="pw-for-test-1234")
        response = client.post(
            "/api/attempts/",
            {"exam": self.exam.id, "token": str(uuid.uuid4())},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201, response.content)
