from rest_framework.serializers import ModelSerializer

from lms.models import Course


class CourseSerializer(ModelSerializer):
    """Сериализатор для курса"""

    class Meta:
        model = Course
        fields = "__all__"
