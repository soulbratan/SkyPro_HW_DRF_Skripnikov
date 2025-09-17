from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для урока"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """Сериализатор для курса"""

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        """Метод для получения количества уроков в курсе"""
        return obj.lesson_set.count()

