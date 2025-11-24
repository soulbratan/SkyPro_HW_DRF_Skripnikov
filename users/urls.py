from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    CoursePaymentAPIView,
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    PaymentSuccessAPIView,
    UserCreateAPIView,
    UserDestroyAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name


urlpatterns = [
    # payment
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path(
        "payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment-retrieve"
    ),
    path("payment/", PaymentListAPIView.as_view(), name="payment-list"),
    path(
        "payment/course/<int:course_id>/",
        CoursePaymentAPIView.as_view(),
        name="course-payment",
    ),
    path("payment/success/", PaymentSuccessAPIView.as_view(), name="payment-success"),
    # users_token
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "login/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="login_refresh",
    ),
    # users
    path("register/", UserCreateAPIView.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("", UserListAPIView.as_view(), name="user-list"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),
]
