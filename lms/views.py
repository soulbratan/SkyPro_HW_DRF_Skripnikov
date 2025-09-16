from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from lms.models import Course
from lms.serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    """Контроллер для модели курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
