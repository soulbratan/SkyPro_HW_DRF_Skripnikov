from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите телефон",
    )
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Введите страну",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Добавьте аватар",
    )
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Модель платежей"""

    PAYMENT_METHOD_CHOICES = [
        ("card", "Картой"),
        ("transfer", "Перевод на счет"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('succeeded', 'Оплачено'),
        ('canceled', 'Отменено'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата платежа",
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        null=True,
        blank=True,
        related_name="payments",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        null=True,
        blank=True,
        related_name="payments",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    stripe_session_id = models.CharField(
        max_length=255,
        verbose_name="ID сессии Stripe",
        blank=True,
        null=True
    )
    stripe_payment_url = models.URLField(
        max_length=500,
        verbose_name="Ссылка на оплату Stripe",
        blank=True,
        null=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="Статус платежа"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Платеж {self.user} - {self.amount} руб. ({self.payment_date})"
