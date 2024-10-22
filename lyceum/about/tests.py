from django.test import Client, TestCase
from django.urls import reverse

__all__ = ["StaticURLTests"]


class StaticURLTests(TestCase):
    def test_about_page_endpoint(self):

        response = Client().get("/about/")

        self.assertEqual(response.status_code, 200, "ERROR-WRONG RESPONSE!")


class ReverseURLTests(TestCase):
    def test_about_page_endpoint(self):

        response = Client().get(reverse("about:about"))

        self.assertEqual(response.status_code, 200, "ERROR-WRONG RESPONSE!")
