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

        self.best_item = catalog.models.Item.objects.create(
            name="Лучший товар",
            text="Это описание товара, содержащее роскошно и превосходно.",
            category=category,
            is_on_main=True,
            is_published=True,
        )

        self.worst_item = catalog.models.Item.objects.create(
            name="Худший товар",
            text="Это описание товара, содержащее роскошно и превосходно.",
            category=category,
            is_on_main=True,
            is_published=True,
        )

        self.medium_item = catalog.models.Item.objects.create(
            name="Средненький товар",
            text="Это описание товара, содержащее роскошно и превосходно.",
            category=category,
            is_on_main=True,
            is_published=True,
        )

        self.best_item.tags.add(tag)
        self.worst_item.tags.add(tag)
        self.medium_item.tags.add(tag)

        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="correct_password",
        )

        self.min_user = User.objects.create_user(
            username="testminuser",
            email="testuser@example.com",
            password="correct_password",
        )

        Rating.objects.create(user=self.user, item=self.best_item, score=5)

        Rating.objects.create(user=self.min_user, item=self.best_item, score=1)

        Rating.objects.create(user=self.user, item=self.medium_item, score=3)

        Rating.objects.create(user=self.user, item=self.worst_item, score=1)

    def tearDown(self):
        User.objects.all().delete()
        catalog.models.Category.objects.all().delete()
        catalog.models.Tag.objects.all().delete()
        catalog.models.Item.objects.all().delete()
        Rating.objects.all().delete()


    def test_user_stats(self):
        self.client.login(username="testuser", password="correct_password")
        response = self.client.get(reverse("statistics:user_statistics"))

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

        self.assertEqual(response.context["user"], self.user)
        self.assertEqual(response.context["total_ratings"], 3)
        self.assertEqual(response.context["average_rating"], 3)
        self.assertEqual(response.context["best_item"], self.best_item)
        self.assertEqual(response.context["worst_item"], self.worst_item)

    def test_item_stats(self):
        self.client.login(username="testuser", password="correct_password")
        response = self.client.get(reverse("statistics:item_statistics"))

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

        rating = response.context["item_stats"][0]

        self.assertEqual(rating["item"], self.best_item)
        self.assertEqual(rating["avg_rating"], 3)
        self.assertEqual(rating["last_max_user"], self.user)
        self.assertEqual(rating["last_min_user"], self.min_user)
        self.assertEqual(rating["rating_count"], 2)

    def test_user_rated_item_stats(self):
        self.client.login(username="testuser", password="correct_password")
        response = self.client.get(reverse("statistics:user_rated_items"))

        self.assertEqual(len(response.context["ratings"]), 3)

    def test_anonymous_user_cant_open_stats(self):

        response = self.client.get(reverse("statistics:user_rated_items"))
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)

        response = self.client.get(reverse("statistics:user_statistics"))
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
