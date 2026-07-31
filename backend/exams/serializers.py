"""직렬화.

응시 중에는 정답이 새어 나가면 안 되므로 시리얼라이저를 두 벌로 나눈다.
- ChoiceSerializer / QuestionSerializer          → is_correct·solution 없음
- ChoiceWithAnswerSerializer / QuestionWithSolutionSerializer → 열람·결과 화면용
"""

from rest_framework import serializers

from .models import Attempt, AttemptAnswer, Choice, Exam, Question, Solution


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "number", "text")


class ChoiceWithAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "number", "text", "is_correct")


class SolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ("explanation", "accepted_answers", "model_answer", "rubric")


class QuestionSerializer(serializers.ModelSerializer):
    """응시 모드용 — 정답 정보를 일절 포함하지 않는다."""

    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "number", "qtype", "difficulty", "body", "points", "choices")


class QuestionWithSolutionSerializer(serializers.ModelSerializer):
    choices = ChoiceWithAnswerSerializer(many=True, read_only=True)
    solution = SolutionSerializer(read_only=True)
    correct_choice = serializers.IntegerField(source="correct_choice_number", read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "number",
            "qtype",
            "difficulty",
            "body",
            "points",
            "choices",
            "correct_choice",
            "solution",
        )


class ExamListSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True)
    mc_count = serializers.IntegerField(read_only=True)
    short_count = serializers.IntegerField(read_only=True)
    essay_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = (
            "id",
            "title",
            "round",
            "version",
            "scope",
            "time_limit_min",
            "total_score",
            "question_count",
            "mc_count",
            "short_count",
            "essay_count",
        )


class ExamDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = (
            "id",
            "title",
            "round",
            "version",
            "scope",
            "time_limit_min",
            "total_score",
            "questions",
        )

    def get_questions(self, exam):
        with_solutions = self.context.get("with_solutions", False)
        serializer_cls = QuestionWithSolutionSerializer if with_solutions else QuestionSerializer
        return serializer_cls(exam.questions.all(), many=True).data


class AttemptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attempt
        fields = ("id", "exam", "token", "started_at")
        read_only_fields = ("id", "started_at")


class SubmittedAnswerSerializer(serializers.Serializer):
    """제출 payload의 한 문항."""

    question = serializers.IntegerField()
    selected_choice = serializers.IntegerField(required=False, allow_null=True)
    text_answer = serializers.CharField(required=False, allow_blank=True, default="")


class SubmitSerializer(serializers.Serializer):
    answers = SubmittedAnswerSerializer(many=True)
    elapsed_sec = serializers.IntegerField(required=False, default=0, min_value=0)


class AttemptAnswerResultSerializer(serializers.ModelSerializer):
    question = QuestionWithSolutionSerializer(read_only=True)

    class Meta:
        model = AttemptAnswer
        fields = (
            "id",
            "question",
            "selected_choice",
            "text_answer",
            "is_correct",
            "awarded_points",
            "graded_by",
        )


class AttemptResultSerializer(serializers.ModelSerializer):
    answers = AttemptAnswerResultSerializer(many=True, read_only=True)
    exam_title = serializers.CharField(source="exam.title", read_only=True)
    total_points = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)

    class Meta:
        model = Attempt
        fields = (
            "id",
            "exam",
            "exam_title",
            "token",
            "started_at",
            "submitted_at",
            "elapsed_sec",
            "auto_score",
            "self_score",
            "total_points",
            "answers",
        )


class AttemptSummarySerializer(serializers.ModelSerializer):
    """이력 목록용 — 문항별 상세는 뺀다."""

    exam_title = serializers.CharField(source="exam.title", read_only=True)
    total_points = serializers.DecimalField(max_digits=5, decimal_places=1, read_only=True)

    class Meta:
        model = Attempt
        fields = (
            "id",
            "exam",
            "exam_title",
            "started_at",
            "submitted_at",
            "elapsed_sec",
            "auto_score",
            "self_score",
            "total_points",
        )


class SelfGradeSerializer(serializers.ModelSerializer):
    """결과 화면에서 서술형 자기채점 / 주관식 오판 보정."""

    class Meta:
        model = AttemptAnswer
        fields = ("id", "is_correct", "awarded_points")

    def validate_awarded_points(self, value):
        max_points = self.instance.question.points
        if value < 0 or value > max_points:
            raise serializers.ValidationError(f"0 ~ {max_points} 사이여야 합니다.")
        return value
