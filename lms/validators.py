import re

from rest_framework.serializers import ValidationError


def validate_youtube_only(value):
    """
    Валидатор для проверки, что ссылка ведет только на youtube.com
    """
    if value:
        # Проверяем, что это URL
        if not re.match(r"^https?://", value):
            raise ValidationError("Некорректный формат ссылки")

        # Проверяем, что это youtube.com
        if "youtube.com" not in value and "youtu.be" not in value:
            raise ValidationError("Разрешены только ссылки на youtube.com")
