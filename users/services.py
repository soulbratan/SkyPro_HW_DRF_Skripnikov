import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(payment):
    """Создает сессию оплаты в Stripe и возвращает URL для оплаты"""

    course = payment.paid_course
    product_name = course.title if course else "Урок"

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': product_name,
                },
                'unit_amount': int(payment.amount * 100),  # Stripe требует сумму в копейках
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'{settings.FRONTEND_URL}/payment/success/?session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=f'{settings.FRONTEND_URL}/payment/cancel/',
        metadata={
            'payment_id': payment.id,
            'user_id': payment.user.id if payment.user else None,
        }
    )

    return session