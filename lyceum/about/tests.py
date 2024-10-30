from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

__all__ = ["StaticURLTests"]


class StaticURLTests(TestCase):
    def test_about_page_endpoint(self):

        url = reverse("about:about")

        response = Client().get(url)

        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            "ERROR-WRONG RESPONSE!",
        )
