from django.conf import settings
from django.test import Client, TestCase
from django.test.utils import override_settings


class StaticURLTests(TestCase):
    if settings.ALLOW_REVERSE:

        @override_settings(ALLOW_REVERSE=True)
        def test_allow_reverse_true_coffee(self):
            client = Client()
            for _ in range(9):
                response = client.get("/coffee/")

                # print(response.content.decode())

            response = client.get("/coffee/")
            # print(response.content.decode())
            self.assertEqual(
                response.content.decode("utf-8"),
                "Я кинйач",
                "test_allow_reverse_true_coffee down",
            )

    else:

        @override_settings(ALLOW_REVERSE=False)
        def test_allow_reverse_false_coffee(self):
            client = Client()
            for _ in range(9):
                response = client.get("/coffee/")
                # print(response.content.decode())

            response = client.get("/coffee/")
            # print(response.content.decode())
            self.assertEqual(
                response.content.decode("utf-8"),
                "Я чайник",
                "test_allow_reverse_false_coffee down",
            )
