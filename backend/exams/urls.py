from rest_framework.routers import DefaultRouter

from .views import AttemptAnswerViewSet, AttemptViewSet, ExamViewSet

router = DefaultRouter()
router.register("exams", ExamViewSet, basename="exam")
router.register("attempts", AttemptViewSet, basename="attempt")
router.register("attempt-answers", AttemptAnswerViewSet, basename="attempt-answer")

urlpatterns = router.urls
