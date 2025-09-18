from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    """Сериализатор для платежей"""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""

    payments = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = User
        fields = "__all__"
