import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_or_get_stripe_product(course):
    """Создает или получает продукт в Stripe для курса"""

    # Генерируем уникальный ID продукта на основе ID курса
    product_id = f"course_{course.id}"

    try:
        # Пытаемся получить существующий продукт
        product = stripe.Product.retrieve(product_id)
    except stripe.error.InvalidRequestError:
        # Если продукт не существует - создаем новый
        product = stripe.Product.create(
            id=product_id,
            name=course.title,
            description=course.description[:500] if course.description else f"Курс {course.title}",
        )

    return product


def create_stripe_price(product, amount):
    """Создает цену для продукта в Stripe"""

    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(amount * 100),  # Stripe требует сумму в копейках
        currency='rub',
    )

    return price


def create_stripe_session(payment):
    """Создает сессию оплаты в Stripe с созданием продукта"""

    course = payment.paid_course

    if not course:
        # Если оплачивается не курс, а урок - используем общий подход
        product_name = "Урок"
        if payment.paid_lesson:
            product_name = payment.paid_lesson.title
    else:
        # Для курса создаем/получаем продукт в Stripe
        product = create_or_get_stripe_product(course)
        price = create_stripe_price(product, payment.amount)

        # Создаем сессию с использованием product и price
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price.id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{settings.FRONTEND_URL}/payment/success/?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{settings.FRONTEND_URL}/payment/cancel/',
            metadata={
                'payment_id': payment.id,
                'user_id': payment.user.id if payment.user else None,
                'course_id': course.id if course else None,
                'lesson_id': payment.paid_lesson.id if payment.paid_lesson else None,
            }
        )

        return session