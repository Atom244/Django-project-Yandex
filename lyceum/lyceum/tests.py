from django.test import Client, TestCase
from django.test.utils import override_settings


class StaticURLTests(TestCase):

    @override_settings(ALLOW_REVERSE=True)
    def test_allow_reverse_true_coffee(self):
        client = Client()
        # Делаем 10 запросов и проверяем только 10-й
        counter = 0
        for i in range(1, 200):
            response = client.get("/coffee/")
            response_text = response.content.decode("utf-8")
            counter += 1
            if counter == 10:
                counter = 0
                self.assertEqual(
                    response_text,
                    "Я кинйач",  # Ожидаем перевернутую строку на 10-й запрос
                    f"Ответ на 10-й запрос не соответствует 'Я кинйач'."
                    f"Получено: {response_text}",
                )
            else:
                # Проверяем, что до 10-го запроса ответы не изменяются
                self.assertNotEqual(
                    response_text,
                    "Я кинйач",
                    f"Перевернутый текст не должен был быть на запросе {i} "
                    f"Получено: {response_text}",
                )

    @override_settings(ALLOW_REVERSE=False)
    def test_allow_reverse_false_coffee(self):
        client = Client()
        # Делаем 10 запросов, но не должно быть переворота ни на одном из них
        for i in range(1, 200):
            response = client.get("/coffee/")
            response_text = response.content.decode("utf-8")
            # В каждом ответе ожидаем обычную строку
            self.assertEqual(
                response_text,
                "Я чайник",  # Ожидаем обычную строку без переворота
                f"Ответ на запрос {i} не соответствует 'Я чайник'."
                f"Получено: {response_text}",
            )
