from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase

__all__ = ["StaticURLTests"]


class StaticURLTests(TestCase):
    def test_home_page_endpoint(self):
        # Делаем запрос к главной странице и проверяем статус
        response = Client().get("")
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

    def test_coffee(self):
        cache.clear()
        coffee_content_check = Client().get("/coffee/")
        self.assertEqual(
            coffee_content_check.content.decode(),
            "Я чайник",
            "coffee_content_check down",
        )

        coffee_status_check = Client().get("/coffee/")
        self.assertEqual(
            coffee_status_check.status_code,
            HTTPStatus.IM_A_TEAPOT,
            "coffee_status_check down",
        )
