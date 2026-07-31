from django.contrib.auth.models import User
from django.test import TestCase

from exams.models import Attempt, Choice, Exam, Question, QuestionType, Solution


class AdminSmokeTests(TestCase):
    """관리자 화면이 열리고 문항 수정이 API에 반영되는지 확인한다."""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser("admin", "admin@example.com", "test-pass-1234")
        cls.exam = Exam.objects.create(title="2차 V9", round=9, version=1)
        cls.question = Question.objects.create(
            exam=cls.exam, number=1, qtype=QuestionType.MULTIPLE_CHOICE, body="원래 지문", points=3
        )
        for number in range(1, 5):
            Choice.objects.create(
                question=cls.question, number=number, text=f"보기{number}", is_correct=number == 2
            )
        Solution.objects.create(question=cls.question, explanation="해설")
        Attempt.objects.create(exam=cls.exam)

    def setUp(self):
        self.client.login(username="admin", password="test-pass-1234")

    def test_admin_pages_render(self):
        pages = [
            "/admin/",
            "/admin/exams/exam/",
            "/admin/exams/question/",
            "/admin/exams/solution/",
            "/admin/exams/attempt/",
            f"/admin/exams/question/{self.question.id}/change/",
            f"/admin/exams/exam/{self.exam.id}/change/",
        ]
        for page in pages:
            with self.subTest(page=page):
                self.assertEqual(self.client.get(page).status_code, 200)

    def test_editing_a_question_shows_up_in_the_api(self):
        self.question.body = "관리자가 고친 지문"
        self.question.save()
        response = self.client.get(f"/api/exams/{self.exam.id}/")
        self.assertEqual(response.json()["questions"][0]["body"], "관리자가 고친 지문")

    def test_unpublished_exam_is_hidden_from_the_api(self):
        self.exam.is_published = False
        self.exam.save()
        self.assertEqual(self.client.get("/api/exams/").json(), [])
