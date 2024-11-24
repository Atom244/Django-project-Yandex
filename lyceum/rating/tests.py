import http

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

import catalog.models
from rating.models import Rating

__all__ = []


class RatingTests(TestCase):
    def setUp(self):
        category = catalog.models.Category.objects.create(
            name="Тестовая категория",
            slug="test-category",
            weight=10,
        )

        tag = catalog.models.Tag.objects.create(
            name="Тестовый тег",
            slug="test-tag",
        )

        self.item = catalog.models.Item.objects.create(
            name="Тестовый товар",
            text="Это описание товара, содержащее роскошно и превосходно.",
            category=category,
            is_on_main=True,
            is_published=True,
        )

        self.item.tags.add(tag)

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="correct_password",
        )

        self.another_user = User.objects.create_user(
            username="TestUser1",
            password="Qw123456#",
            is_active=True,
        )

        self.rating_url = reverse(
            "catalog:item-detail",
            kwargs={"pk": self.item.pk},
        )

    def test_response_object_adding(self):
        Rating.objects.create(user=self.user, item=self.item, score=4)

        Rating.objects.create(user=self.another_user, item=self.item, score=2)

        response = self.client.get(self.rating_url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_anonymous_user_cannot_rate_or_delete(self):
        headers = {"Authorization": "JWT <token>"}
        response = self.client.post(
            self.rating_url,
            {"score": 5},
            headers=headers,
        )
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertEqual(Rating.objects.count(), 0)

    def test_authenticated_user_can_rate(self):
        self.client.login(username="testuser", password="correct_password")
        response = self.client.post(self.rating_url, {"score": 5}, follow=True)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(Rating.objects.count(), 1)
        rating = Rating.objects.first()
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.score, 5)

    def test_authenticated_user_can_delete_rating(self):

        Rating.objects.create(user=self.user, item=self.item, score=3)

        self.client.login(username="testuser", password="correct_password")

        response = self.client.post(
            self.rating_url,
            {"delete": ""},
            follow=True,
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(Rating.objects.count(), 0)

    def test_context_avg_count(self):
        Rating.objects.create(user=self.user, item=self.item, score=2)
        Rating.objects.create(user=self.another_user, item=self.item, score=4)
        response = self.client.get(
            reverse("catalog:item-detail", kwargs={"pk": self.item.id}),
        )

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response.context["average_rating"], 3)
        self.assertEqual(response.context["total_ratings"], 2)
