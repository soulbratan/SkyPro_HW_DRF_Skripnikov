from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    SubscriptionAPIView,
    UserSubscriptionsAPIView,
)

app_name = LmsConfig.name

router = SimpleRouter()
router.register("course", CourseViewSet)


urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-retrieve"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson-list"),
    path(
        "lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"
    ),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"
    ),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscriptions"),
    path(
        "my-subscriptions/", UserSubscriptionsAPIView.as_view(), name="my-subscriptions"
    ),
] + router.urls
