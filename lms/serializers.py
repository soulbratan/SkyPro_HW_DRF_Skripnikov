from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_youtube_only


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""

    video_link = serializers.URLField(
        validators=[validate_youtube_only], allow_null=True, default=None
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    video_link = serializers.URLField(
        validators=[validate_youtube_only], read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    last_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ('last_updated',)

    def get_lessons_count(self, obj):
        """Метод для получения количества уроков в курсе"""
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        """Метод для проверки активной подписки текущего пользователя"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=obj, is_active=True
            ).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""

    class Meta:
        model = Subscription
        fields = "__all__"
