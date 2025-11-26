from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin2@example.com",
        )
        self.lesson = Lesson.objects.create(
            title="TEST", description="test", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.lesson.title, data.get("title"))
        self.assertEqual(self.lesson.description, data.get("description"))

    def test_lesson_create(self):
        url = reverse("lms:lesson-create")
        data = {
            "title": "Russian",
        }
        response = self.client.post(url, data)

        data_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual("Russian", data_json.get("title"))

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        data = {"title": "Math", "description": "math2"}
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual("Math", data.get("title"))
        self.assertEqual("math2", data.get("description"))

    def test_lesson_delete(self):
        url = reverse("lms:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_link": None,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": None,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin2@example.com",
        )
        self.course = Course.objects.create(
            title="TEST", description="test", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.course.title, data.get("title"))
        self.assertEqual(self.course.description, data.get("description"))

    def test_course_create(self):
        url = reverse("lms:course-list")
        data = {
            "title": "Russian",
        }
        response = self.client.post(url, data)

        data_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual("Russian", data_json.get("title"))

        self.assertEqual(Course.objects.all().count(), 2)

    # def test_course_update(self):
    #     url = reverse("lms:course-detail", args=(self.course.pk,))
    #     data = {"title": "Math", "description": "math2"}
    #     response = self.client.patch(url, data)
    #
    #     data = response.json()
    #
    #     self.assertEqual("Math", data.get("title"))
    #     self.assertEqual("math2", data.get("description"))

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        data = response.json()  # noqa

        result = {  # noqa
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "lessons_count": 0,
                    "lessons": [],
                    "is_subscribed": False,
                    "title": self.course.title,
                    "preview": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin2@example.com",
        )
        self.course = Course.objects.create(
            title="TEST2", description="test2", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        url = reverse("lms:subscriptions")
        data = {"course_id": self.course.pk}

        resp_st_code = []
        result = []

        for i in range(2):
            response = self.client.post(url, data)
            resp_st_code.append(response.status_code)
            result.append(response.json())

        self.assertEqual(resp_st_code[0], status.HTTP_201_CREATED)
        self.assertEqual(result[0].get("message"), "подписка добавлена")

        self.assertEqual(resp_st_code[1], status.HTTP_200_OK)
        self.assertEqual(result[1].get("message"), "подписка удалена")

    def test_subscription_list(self):
        url = reverse("lms:my-subscriptions")
        url_2 = reverse("lms:subscriptions")
        data = {"course_id": self.course.pk}

        response = self.client.get(url)
        self.assertEqual(len(response.json()), 0)

        self.client.post(url_2, data)
        response = self.client.get(url)

        self.assertEqual(len(response.json()), 1)
