from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course, Subscription
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

    def test_course_update(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"title": "Math", "description": "math2"}
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual("Math", data.get("title"))
        self.assertEqual("math2", data.get("description"))

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        data = response.json()
        print(data)

        result = {
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
        self.assertEqual(data, result)
