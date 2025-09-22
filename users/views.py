from django.conf import settings
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Payment, User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import PaymentSerializer, PublicUserSerializer, UserSerializer
from users.services import create_stripe_session, get_payment_status, get_session_status


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа"""

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save(user=self.request.user)

        # Если оплачивается курс, используем цену курса
        if payment.paid_course and not payment.amount:
            payment.amount = payment.paid_course.price
            payment.save()

        # Создаем сессию Stripe
        session = create_stripe_session(payment)

        # Сохраняем ID сессии и ссылку на оплату в платеже
        payment.stripe_session_id = session.id
        payment.stripe_payment_url = session.url  # Сохраняем ссылку на оплату
        payment.save()

        # Возвращаем данные с ссылкой на оплату
        response_data = serializer.data
        response_data["stripe_payment_url"] = session.url

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр платежа"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if instance.stripe_session_id:
            stripe_status = get_payment_status(instance.stripe_session_id)
            data = serializer.data
            data["stripe_payment_status"] = stripe_status
            data["actual_status"] = get_session_status(instance.stripe_session_id)
            return Response(data)

        return Response(serializer.data)


class PaymentListAPIView(generics.ListAPIView):
    """Список платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ("payment_date",)
    filterset_fields = (
        "paid_lesson",
        "paid_course",
        "payment_method",
    )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # Получаем стандартный response
        response = super().list(request, *args, **kwargs)
        print(response.data)

        # Добавляем статус Stripe для каждого платежа
        for payment_data in response.data:
            payment_id = payment_data["id"]
            try:
                payment = Payment.objects.get(id=payment_id)
                if payment.stripe_session_id:
                    stripe_status = get_payment_status(payment.stripe_session_id)
                    payment_data["stripe_payment_status"] = stripe_status

                    # Дополнительная информация о сессии (опционально)
                    session_info = get_session_status(payment.stripe_session_id)
                    payment_data["stripe_session_status"] = session_info.get("status")
                    payment_data["stripe_amount_total"] = session_info.get(
                        "amount_total"
                    )
            except Payment.DoesNotExist:
                # Если платеж не найден, пропускаем
                continue

        return response


class CoursePaymentAPIView(APIView):
    """Создание платежа для курса"""

    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        from lms.models import Course

        course = get_object_or_404(Course, id=course_id)

        # Создаем запись о платеже
        payment = Payment.objects.create(
            user=request.user,
            paid_course=course,
            amount=course.price,
            payment_method="transfer",  # онлайн-оплата
        )

        # Создаем сессию Stripe
        session = create_stripe_session(payment)

        # Сохраняем ID сессии и ссылку на оплату
        payment.stripe_session_id = session.id
        payment.stripe_payment_url = session.url  # Сохраняем ссылку на оплату
        payment.save()

        return Response(
            {
                "payment_id": payment.id,
                "session_id": session.id,
                "stripe_payment_url": session.url,  # Возвращаем ссылку на оплату
                "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
                "redirect_url": session.url,
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentSuccessAPIView(APIView):
    """Обработка успешной оплаты"""

    permission_classes = [AllowAny]

    def get(self, request):
        session_id = request.GET.get("session_id")

        if session_id:
            try:
                payment = Payment.objects.get(stripe_session_id=session_id)
                payment.payment_status = "succeeded"
                payment.save()
            except Payment.DoesNotExist:
                pass

        return redirect("http://localhost:8000")  # Редирект на главную


class UserCreateAPIView(generics.CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр пользователя"""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserSerializer
        return PublicUserSerializer


class UserListAPIView(generics.ListAPIView):
    """Просмотр всех пользователей"""

    serializer_class = PublicUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Изменение пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class UserDestroyAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
