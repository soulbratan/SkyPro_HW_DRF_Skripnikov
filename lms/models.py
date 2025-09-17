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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
