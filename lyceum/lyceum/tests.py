from django.conf import settings
from django.test import Client, TestCase


class StaticURLTests(TestCase):
    if settings.ALLOW_REVERSE:

        def test_allow_reverse_true_coffee(self):
            client = Client()
            for _ in range(9):
                response = client.get("/coffee/")
                # print(response.content.decode())
            response = client.get("/coffee/")
            # print(response.content.decode())
            self.assertEqual(
                response.content.decode(),
                "Я кинйач",
                "test_allow_reverse_true_coffee down",
            )

    else:

        def test_allow_reverse_false_coffee(self):
            client = Client()
            for _ in range(9):
                response = client.get("/coffee/")
                print(response.content.decode())
            response = client.get("/coffee/")
            print(response.content.decode())
            self.assertEqual(
                response.content.decode(),
                "Я чайник",
                "test_allow_reverse_false_coffee down",
            )
