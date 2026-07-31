import uuid

from django.db import models


class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = "MC", "객관식"
    SHORT_ANSWER = "SHORT", "주관식"
    ESSAY = "ESSAY", "서술형"


class Difficulty(models.TextChoices):
    BASIC = "BASIC", "기초"
    APPLIED = "APPLIED", "응용"
    ADVANCED = "ADVANCED", "심화"


class Exam(models.Model):
    """모의고사 한 세트(예: 2차 Version 1)."""

    title = models.CharField("제목", max_length=200)
    round = models.PositiveSmallIntegerField("차수", default=1)
    version = models.PositiveSmallIntegerField("버전")
    scope = models.TextField("출제 범위", blank=True)
    time_limit_min = models.PositiveSmallIntegerField("권장 시간(분)", default=60)
    total_score = models.PositiveSmallIntegerField("총점", default=100)
    is_published = models.BooleanField("공개", default=True)
    order = models.PositiveSmallIntegerField("정렬 순서", default=0)
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "시험"
        verbose_name_plural = "시험"
        ordering = ["round", "version"]
        constraints = [
            models.UniqueConstraint(fields=["round", "version"], name="uniq_round_version"),
        ]

    def __str__(self):
        return self.title or f"{self.round}차 V{self.version}"


class Question(models.Model):
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="questions", verbose_name="시험"
    )
    number = models.PositiveSmallIntegerField("문항 번호")
    qtype = models.CharField("유형", max_length=10, choices=QuestionType.choices)
    difficulty = models.CharField(
        "난이도", max_length=10, choices=Difficulty.choices, default=Difficulty.BASIC
    )
    body = models.TextField("지문 (마크다운)")
    points = models.DecimalField("배점", max_digits=4, decimal_places=1, default=3)

    class Meta:
        verbose_name = "문항"
        verbose_name_plural = "문항"
        ordering = ["exam", "number"]
        constraints = [
            models.UniqueConstraint(fields=["exam", "number"], name="uniq_exam_number"),
        ]

    def __str__(self):
        return f"[{self.exam}] {self.number}번"

    @property
    def correct_choice_number(self):
        choice = next((c for c in self.choices.all() if c.is_correct), None)
        return choice.number if choice else None


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices", verbose_name="문항"
    )
    number = models.PositiveSmallIntegerField("번호")  # 1~4 (①~④)
    text = models.TextField("선택지 (마크다운)")
    is_correct = models.BooleanField("정답", default=False)

    class Meta:
        verbose_name = "선택지"
        verbose_name_plural = "선택지"
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(fields=["question", "number"], name="uniq_question_choice"),
        ]

    def __str__(self):
        return f"{self.number}. {self.text[:30]}"


class Solution(models.Model):
    """정답·해설. 문항과 1:1이며 응시 중에는 절대 직렬화되지 않는다."""

    question = models.OneToOneField(
        Question, on_delete=models.CASCADE, related_name="solution", verbose_name="문항"
    )
    explanation = models.TextField("해설 (마크다운)", blank=True)
    accepted_answers = models.JSONField(
        "정답 후보 (주관식)",
        default=list,
        blank=True,
        help_text='정규화 후 완전 일치하면 정답. 예: ["RouterLink / RouterView"]',
    )
    required_keywords = models.JSONField(
        "키워드 규칙 (주관식)",
        default=list,
        blank=True,
        help_text='한 그룹의 키워드를 모두 포함하면 정답. 예: [["routerlink", "routerview"]]',
    )
    model_answer = models.TextField("모범 답안 (서술형)", blank=True)
    rubric = models.JSONField(
        "채점 기준표 (서술형)",
        default=list,
        blank=True,
        help_text='[{"points": 2, "criteria": "…"}] 형태',
    )
    needs_review = models.BooleanField(
        "채점 규칙 검토 필요",
        default=False,
        help_text="자동 추출한 주관식 정답 규칙을 손볼 필요가 있는 문항",
    )

    class Meta:
        verbose_name = "정답·해설"
        verbose_name_plural = "정답·해설"

    def __str__(self):
        return f"{self.question} 해설"

    @property
    def rubric_total(self):
        return sum(float(item.get("points", 0)) for item in self.rubric or [])


class Attempt(models.Model):
    """익명 응시 기록. 브라우저가 생성한 token으로 본인 이력을 조회한다."""

    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name="attempts", verbose_name="시험"
    )
    token = models.UUIDField("브라우저 토큰", default=uuid.uuid4, db_index=True)
    started_at = models.DateTimeField("시작 시각", auto_now_add=True)
    submitted_at = models.DateTimeField("제출 시각", null=True, blank=True)
    elapsed_sec = models.PositiveIntegerField("소요 시간(초)", default=0)
    auto_score = models.DecimalField("자동 채점 점수", max_digits=5, decimal_places=1, default=0)
    self_score = models.DecimalField("자기채점 점수", max_digits=5, decimal_places=1, default=0)

    class Meta:
        verbose_name = "응시 기록"
        verbose_name_plural = "응시 기록"
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.exam} — {self.started_at:%Y-%m-%d %H:%M}"

    @property
    def is_submitted(self):
        return self.submitted_at is not None

    @property
    def total_points(self):
        return self.auto_score + self.self_score


class GradedBy(models.TextChoices):
    AUTO = "AUTO", "자동 채점"
    SELF = "SELF", "자기 채점"


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(
        Attempt, on_delete=models.CASCADE, related_name="answers", verbose_name="응시 기록"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="문항")
    selected_choice = models.PositiveSmallIntegerField("선택한 번호", null=True, blank=True)
    text_answer = models.TextField("작성한 답", blank=True)
    is_correct = models.BooleanField("정답 여부", null=True, blank=True)  # null = 미채점(서술형)
    awarded_points = models.DecimalField("획득 점수", max_digits=4, decimal_places=1, default=0)
    graded_by = models.CharField(
        "채점 방식", max_length=10, choices=GradedBy.choices, default=GradedBy.AUTO
    )

    class Meta:
        verbose_name = "제출 답안"
        verbose_name_plural = "제출 답안"
        ordering = ["question__number"]
        constraints = [
            models.UniqueConstraint(fields=["attempt", "question"], name="uniq_attempt_question"),
        ]

    def __str__(self):
        return f"{self.attempt_id} — {self.question.number}번"
