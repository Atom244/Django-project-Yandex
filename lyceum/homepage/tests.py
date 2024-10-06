from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_home_page_endpoint(self):
        # Делаем запрос к главной странице и проверяем статус
        response = Client().get("")
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

    def test_coffee(self):

        coffee_content_check = Client().get("/coffee/")
        self.assertEqual(
            (coffee_content_check.content).decode("utf-8"),
            "<body>Я чайник</body>",
            "coffee_content_check down",
        )

        coffee_status_check = Client().get("/coffee/")
        self.assertEqual(
            coffee_status_check.status_code, 418, "coffee_status_check down"
        )
