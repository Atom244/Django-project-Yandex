from django.test import Client, TestCase

from parameterized import parameterized


class StaticURLTests(TestCase):
    def test_catalog_page_endpoint(self):
        normal_catalog_check = Client().get("/catalog/")
        self.assertEqual(
            normal_catalog_check.status_code, 200, "normal_catalog_check down"
        )

        wrong_catalog_check = Client().get("/catalogE/")
        self.assertEqual(
            wrong_catalog_check.status_code, 404, "wrong_catalog_check down"
        )

    @parameterized.expand([("",), ("/re",), ("/converter",)])
    def test_catalog(self, point):
        parameters = [-1, 1.5, 0]

        for parameter in parameters:
            normal_catalog_check = Client().get(f"/catalog{point}/1/")
            self.assertEqual(
                normal_catalog_check.status_code,
                200,
                f"normal_catalog_check down. Parameter: {point}",
            )

            if parameter == 0:
                self.skipTest(
                    "Следующий тест пропущен, "
                    "тк по адресу /catalog/<param> допустим 0"
                )

            negative_catalog_check = Client().get(
                f"/catalog{point}/{parameter}/"
            )
            self.assertEqual(
                negative_catalog_check.status_code,
                404,
                f"negative_catalog_check down. Parameter: {parameter}",
            )

            negative_catalog_check = Client().get(f"/catalog/{parameter}/")
            self.assertEqual(
                negative_catalog_check.status_code,
                404,
                f"negative_catalog_check down. Parameter: {parameter}",
            )
