from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

__all__ = []


class StaticURLTests(TestCase):
    def test_home_page_endpoint(self):
        response = Client().get(reverse("homepage:home"))
        self.assertEqual(response.status_code, 200)

    def test_coffee(self):
        cache.clear()
        coffee_content_check = Client().get(reverse("homepage:coffee"))
        self.assertEqual(
            coffee_content_check.content.decode(),
            "Я чайник",
            "coffee_content_check down",
        )

        coffee_status_check = Client().get(reverse("homepage:coffee"))
        self.assertEqual(
            coffee_status_check.status_code,
            HTTPStatus.IM_A_TEAPOT,
            "coffee_status_check down",
        )
