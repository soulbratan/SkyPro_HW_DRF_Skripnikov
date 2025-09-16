from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Контроллер для модели пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer