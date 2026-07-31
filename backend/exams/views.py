from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .grading import grade_attempt, recalculate_scores
from .models import Attempt, AttemptAnswer, Exam, GradedBy, Question, QuestionType
from .serializers import (
    AttemptCreateSerializer,
    AttemptResultSerializer,
    AttemptSummarySerializer,
    ExamDetailSerializer,
    ExamListSerializer,
    SelfGradeSerializer,
    SubmitSerializer,
)


def _truthy(value):
    return str(value).lower() in {"1", "true", "yes"}


class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    """시험 목록·상세. `?with_solutions=1`이면 정답과 해설을 함께 내려준다(열람 모드)."""

    def get_queryset(self):
        qs = Exam.objects.filter(is_published=True)
        if self.action == "list":
            return qs.annotate(
                question_count=Count("questions", distinct=True),
                mc_count=Count(
                    "questions",
                    filter=Q(questions__qtype=QuestionType.MULTIPLE_CHOICE),
                    distinct=True,
                ),
                short_count=Count(
                    "questions",
                    filter=Q(questions__qtype=QuestionType.SHORT_ANSWER),
                    distinct=True,
                ),
                essay_count=Count(
                    "questions", filter=Q(questions__qtype=QuestionType.ESSAY), distinct=True
                ),
            )
        return qs.prefetch_related("questions__choices", "questions__solution")

    def get_serializer_class(self):
        return ExamListSerializer if self.action == "list" else ExamDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["with_solutions"] = _truthy(self.request.query_params.get("with_solutions", ""))
        return context


class AttemptViewSet(viewsets.GenericViewSet):
    """익명 응시. 브라우저가 만든 token으로 본인 이력을 조회한다."""

    queryset = Attempt.objects.select_related("exam")

    def get_serializer_class(self):
        if self.action == "create":
            return AttemptCreateSerializer
        if self.action == "list":
            return AttemptSummarySerializer
        return AttemptResultSerializer

    def _result_queryset(self):
        return self.queryset.prefetch_related(
            Prefetch(
                "answers",
                queryset=AttemptAnswer.objects.select_related(
                    "question", "question__solution"
                ).prefetch_related("question__choices"),
            )
        )

    def list(self, request):
        """GET /api/attempts/?token=… — 내 응시 이력."""
        token = request.query_params.get("token")
        if not token:
            return Response({"detail": "token 쿼리 파라미터가 필요합니다."}, status=400)
        attempts = self.queryset.filter(token=token, submitted_at__isnull=False)
        return Response(AttemptSummarySerializer(attempts, many=True).data)

    def retrieve(self, request, pk=None):
        attempt = self.get_object()
        attempt = self._result_queryset().get(pk=attempt.pk)
        return Response(AttemptResultSerializer(attempt).data)

    def create(self, request):
        serializer = AttemptCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attempt = serializer.save()
        return Response(AttemptCreateSerializer(attempt).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        if attempt.submitted_at:
            return Response({"detail": "이미 제출된 응시입니다."}, status=400)

        serializer = SubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        valid_ids = set(Question.objects.filter(exam=attempt.exam).values_list("id", flat=True))
        rows = [
            AttemptAnswer(
                attempt=attempt,
                question_id=item["question"],
                selected_choice=item.get("selected_choice"),
                text_answer=item.get("text_answer", ""),
            )
            for item in payload["answers"]
            if item["question"] in valid_ids
        ]
        AttemptAnswer.objects.filter(attempt=attempt).delete()
        AttemptAnswer.objects.bulk_create(rows)

        attempt.submitted_at = timezone.now()
        attempt.elapsed_sec = payload.get("elapsed_sec", 0)
        attempt.save(update_fields=["submitted_at", "elapsed_sec"])
        grade_attempt(attempt)

        attempt = self._result_queryset().get(pk=attempt.pk)
        return Response(AttemptResultSerializer(attempt).data)


class AttemptAnswerViewSet(viewsets.GenericViewSet):
    """자기채점 — 서술형 부분점수 부여, 주관식 자동채점 오판 보정."""

    queryset = AttemptAnswer.objects.select_related("question", "attempt")
    serializer_class = SelfGradeSerializer

    def partial_update(self, request, pk=None):
        answer = self.get_object()
        serializer = SelfGradeSerializer(answer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        answer = serializer.save(graded_by=GradedBy.SELF)
        attempt = recalculate_scores(answer.attempt)
        return Response(
            {
                "id": answer.id,
                "is_correct": answer.is_correct,
                "awarded_points": answer.awarded_points,
                "graded_by": answer.graded_by,
                "auto_score": attempt.auto_score,
                "self_score": attempt.self_score,
                "total_points": attempt.total_points,
            }
        )
