from django.conf import settings
from django.db import models


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        blank=True, null=True, verbose_name="Картинка", help_text="Добавьте картинку"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите описание",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=500.00,  # Цена по умолчанию 500
        verbose_name="Цена курса",
        help_text="Укажите цену курса"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        blank=True,
        null=True,
        help_text="Укажите владельца",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока"""

    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="Курс", blank=True, null=True
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Введите описание",
    )
    preview = models.ImageField(
        blank=True, null=True, verbose_name="Картинка", help_text="Добавьте картинку"
    )
    video_link = models.URLField(
        verbose_name="Видео", blank=True, null=True, help_text="Укажите ссылку на видео"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        blank=True,
        null=True,
        help_text="Укажите владельца",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """Модель подписки на обновления курса"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания подписки"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления подписки"
    )
    is_active = models.BooleanField(default=True, verbose_name="Подписка активна")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ["user", "course"]  # Уникальная пара пользователь-курс

    def __str__(self):
        return f"{self.user} - {self.course} ({'активна' if self.is_active else 'неактивна'})"
