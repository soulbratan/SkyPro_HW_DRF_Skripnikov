from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """Сериализатор для платежей"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ('stripe_session_id', 'stripe_payment_url', 'payment_status', 'payment_date')


class UserSerializer(ModelSerializer):
    """Сериализатор для пользователя"""

    payments = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class PublicUserSerializer(ModelSerializer):
    """Сериализатор для публичного просмотра профиля пользователя"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "phone",
            "country",
            "avatar",
            "date_joined",
            "last_login",
        ]
        read_only_fields = fields
