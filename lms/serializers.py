from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import validate_youtube_only


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""

    video_link = serializers.URLField(validators=[validate_youtube_only])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    video_link = serializers.URLField(validators=[validate_youtube_only])

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_count(self, obj):
        """Метод для получения количества уроков в курсе"""
        return obj.lesson_set.count()
