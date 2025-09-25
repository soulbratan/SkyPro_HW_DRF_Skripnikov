from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Course, Subscription


@shared_task
def send_course_update_notification(course_id):
    """
    Асинхронная отправка уведомлений об обновлении курса подписанным пользователям
    """
    try:
        course = Course.objects.get(id=course_id)
        active_subscriptions = Subscription.objects.filter(
            course=course,
            is_active=True
        ).select_related('user')

        if not active_subscriptions:
            return f"No active subscriptions for course {course.title}"

        # Текстовое сообщение
        subject = f'Обновление материалов курса'
        message = f'Материалы курса "{course.title}" обновлены.'

        emails_sent = 0
        for subscription in active_subscriptions:
            user = subscription.user

            # Отправляем простое текстовое письмо
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            emails_sent += 1

        return f"Successfully sent {emails_sent} notifications for course {course.title}"

    except Course.DoesNotExist:
        return f"Course with id {course_id} does not exist"
    except Exception as e:
        return f"Error sending notifications: {str(e)}"
