from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status, response, views
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson, Subscription
from lms.paginations import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер для модели курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModer,)
        elif self.action in ["retrieve", "list", "update"]:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, ~IsModer | IsOwner,)
        return super().get_permissions()


    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name='moders').exists():
            qs = qs.filter(owner=self.request.user)
        return qs


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ~IsModer,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра конкретного урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]


class LessonListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка уроков"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name='moders').exists():
            qs = qs.filter(owner=self.request.user)
        return qs


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения урока"""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока"""

    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        ~IsModer | IsOwner,
    ]


class SubscriptionAPIView(views.APIView):
    """APIView для управления подписками на курсы"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return response.Response(
                {"error": "course_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course_item = get_object_or_404(Course, id=course_id)

        # Ищем подписку (активную или неактивную)
        subscription = Subscription.objects.filter(
            user=user,
            course=course_item
        ).first()

        # Если подписка существует
        if subscription:
            # Если подписка активна - деактивируем ее
            if subscription.is_active:
                subscription.is_active = False
                subscription.save()
                message = 'подписка удалена'
                status_code = status.HTTP_200_OK
            # Если подписка неактивна - активируем ее
            else:
                subscription.is_active = True
                subscription.save()
                message = 'подписка восстановлена'
                status_code = status.HTTP_200_OK
        # Если подписки нет - создаем новую активную
        else:
            Subscription.objects.create(user=user, course=course_item, is_active=True)
            message = 'подписка добавлена'
            status_code = status.HTTP_201_CREATED

        # Возвращаем ответ в API
        return response.Response({"message": message}, status=status_code)


class UserSubscriptionsAPIView(generics.ListAPIView):
    """APIView для получения всех подписок пользователя"""

    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(
            user=self.request.user,
            is_active=True  # Только активные подписки
        ).select_related('course')
