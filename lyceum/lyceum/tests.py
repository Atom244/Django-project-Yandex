from django.test import Client, TestCase
from django.test.utils import override_settings


class StaticURLTests(TestCase):

    @override_settings(ALLOW_REVERSE=True)
    def test_allow_reverse_true_coffee(self):
        client = Client()

        for _ in range(5):
            response = client.get("/coffee/")

        for _ in range(4):
            response = client.get("/coffee/")

        response = client.get("/coffee/")
        response_text = response.content.decode("utf-8")
        if response_text == "Я кинйач":
            self.assertEqual(
                response_text,
                "Я кинйач",
                "Ни один запрос не вернул перевёрнутую строку 'Я кинйач'"
                "при ALLOW_REVERSE=True",
            )

    @override_settings(ALLOW_REVERSE=False)
    def test_allow_reverse_false_coffee(self):
        client = Client()

        for _ in range(10):
            response = client.get("/coffee/")
            response_text = response.content.decode("utf-8")
            self.assertEqual(
                response_text,
                "Я чайник",
                f"Перевёрнутый текст не должен был появиться, "
                f"но получено: {response_text}",
            )
