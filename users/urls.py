from rest_framework.routers import SimpleRouter
from users.views import (
    UserViewSet,
    PaymentCreateAPIView,
    PaymentRetrieveAPIView,
    PaymentListAPIView,
)
from django.urls import path
from users.apps import UsersConfig

app_name = UsersConfig.name

router_user = SimpleRouter()
router_user.register("", UserViewSet)

urlpatterns = [
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path(
        "payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment-retrieve"
    ),
    path("payment/", PaymentListAPIView.as_view(), name="payment-list"),
] + router_user.urls
