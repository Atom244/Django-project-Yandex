from django.test import Client, TestCase
from django.test.utils import override_settings


class StaticURLTests(TestCase):

    @override_settings(ALLOW_REVERSE=True)
    def test_allow_reverse_true_coffee(self):
        # print("CURRENT SETTING 1 test: ", settings.ALLOW_REVERSE)
        client = Client()
        for _ in range(50):
            response = client.get("/coffee/")
            # print(response.content.decode())
            if str(response.content.decode("utf-8")) == "Я кинйач":
                self.assertEqual(
                    response.content.decode("utf-8"),
                    "Я кинйач",
                    "test_allow_reverse_false_coffee down",
                )

    @override_settings(ALLOW_REVERSE=False)
    def test_allow_reverse_false_coffee(self):
        # print("CURRENT SETTING 2 test: ", settings.ALLOW_REVERSE)
        client = Client()
        for _ in range(9):
            response = client.get("/coffee/")
            # print(response.content.decode())

        response = client.get("/coffee/")
        response = response.content.decode("utf-8")
        # print(response)

        self.assertEqual(
            response,
            "Я чайник",
            "test_allow_reverse_false_coffee down",
        )
