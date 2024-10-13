from django.core.cache import cache
from django.test import Client, TestCase
from django.test.utils import override_settings
from lyceum import middleware


class StaticURLTests(TestCase):

    @override_settings(ALLOW_REVERSE=True)
    def test_allow_reverse_true_coffee(self):
        client = Client()
        cache.clear()

        for _ in range(9):
            response = client.get("/coffee/")

        response = client.get("/coffee/")
        response_text = response.content.decode("utf-8")

        self.assertEqual(
            response_text,
            "Я кинйач",
            "Ни один запрос не вернул перевёрнутую строку 'Я кинйач'"
            "при ALLOW_REVERSE=True",
        )

    @override_settings(ALLOW_REVERSE=False)
    def test_allow_reverse_false_coffee(self):
        client = Client()
        cache.clear()

        for _ in range(10):
            response = client.get("/coffee/")
            response_text = response.content.decode("utf-8")
            self.assertEqual(
                response_text,
                "Я чайник",
                f"Перевёрнутый текст не должен был появиться, "
                f"но получено: {response_text}",
            )

    def test_reverse_russian_words(self):
        test_middleware = middleware.ReverseWordMiddleware(None)
        reversed_word = test_middleware.reverse_russian_words("Привет Hello")
        self.assertEqual(
            reversed_word,
            "тевирП Hello",
            f"Тест провалился, результат функции был: {reversed_word}",
        )
        reversed_word_1 = test_middleware.reverse_russian_words("1-ая машiна")
        self.assertEqual(
            reversed_word_1,
            "1-яа машiна",
            f"Тест провалился, результат функции был: {reversed_word_1}",
        )
