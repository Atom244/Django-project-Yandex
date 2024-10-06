from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_home_page_endpoint(self):
        # Делаем запрос к главной странице и проверяем статус
        responde = Client().get("/")
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(responde.status_code, 200)
