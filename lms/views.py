from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер для модели курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModer,)
        elif self.action in ["retrieve", "list", "update"]:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, ~IsModer | IsOwner,)
        return super().get_permissions()


    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name='moders').exists():
            qs = qs.filter(owner=self.request.user)
        return qs


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ~IsModer,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра конкретного урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]


class LessonListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name='moders').exists():
            qs = qs.filter(owner=self.request.user)
        return qs


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока"""

    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        ~IsModer | IsOwner,
    ]
