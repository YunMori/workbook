from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from .models import Attempt, AttemptAnswer, Choice, Exam, Question, Solution


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    fields = ("number", "text", "is_correct")


class SolutionInline(admin.StackedInline):
    model = Solution
    extra = 0
    can_delete = False
    fieldsets = (
        (None, {"fields": ("explanation", "needs_review")}),
        ("주관식 채점 규칙", {"fields": ("accepted_answers", "required_keywords")}),
        ("서술형", {"fields": ("model_answer", "rubric")}),
    )


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "round", "version", "num_questions", "total_score", "time_limit_min", "is_published")
    list_editable = ("is_published",)
    list_filter = ("round", "is_published")
    search_fields = ("title", "scope")
    ordering = ("round", "version")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_num_questions=Count("questions"))

    @admin.display(description="문항", ordering="_num_questions")
    def num_questions(self, obj):
        url = reverse("admin:exams_question_changelist") + f"?exam__id__exact={obj.pk}"
        return format_html('<a href="{}">{}문항 보기</a>', url, obj._num_questions)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("exam", "number", "qtype", "difficulty", "points", "preview", "answer_summary")
    list_display_links = ("number", "preview")
    list_editable = ("difficulty", "points")
    list_filter = ("exam", "qtype", "difficulty")
    search_fields = ("body", "choices__text")
    ordering = ("exam", "number")
    list_per_page = 30
    inlines = [ChoiceInline, SolutionInline]
    fields = ("exam", "number", "qtype", "difficulty", "points", "body")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("exam", "solution")
            .prefetch_related("choices")
        )

    @admin.display(description="지문")
    def preview(self, obj):
        text = " ".join(obj.body.split())
        return text[:70] + ("…" if len(text) > 70 else "")

    @admin.display(description="정답")
    def answer_summary(self, obj):
        if obj.qtype == "MC":
            number = obj.correct_choice_number
            return "①②③④"[number - 1] if number else "⚠ 미지정"
        solution = getattr(obj, "solution", None)
        if not solution:
            return "⚠ 해설 없음"
        if obj.qtype == "SHORT":
            answers = solution.accepted_answers or []
            label = " / ".join(answers)[:40] or "(규칙 없음)"
            return format_html("{}{}", "🔧 " if solution.needs_review else "", label)
        return "서술형(자기채점)"


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    """주관식 채점 규칙을 몰아서 손볼 때 쓰는 화면."""

    list_display = ("question", "question_type", "needs_review", "accepted_answers")
    list_filter = ("needs_review", "question__exam", "question__qtype")
    search_fields = ("explanation", "model_answer")
    ordering = ("question__exam", "question__number")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("question", "question__exam")

    @admin.display(description="유형")
    def question_type(self, obj):
        return obj.question.get_qtype_display()


class AttemptAnswerInline(admin.TabularInline):
    model = AttemptAnswer
    extra = 0
    can_delete = False
    readonly_fields = ("question", "selected_choice", "text_answer", "is_correct", "awarded_points", "graded_by")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("exam", "started_at", "submitted_at", "auto_score", "self_score", "total_points")
    list_filter = ("exam",)
    readonly_fields = ("exam", "token", "started_at", "submitted_at", "elapsed_sec", "auto_score", "self_score")
    inlines = [AttemptAnswerInline]

    def has_add_permission(self, request):
        return False

    @admin.display(description="총점")
    def total_points(self, obj):
        return obj.total_points
