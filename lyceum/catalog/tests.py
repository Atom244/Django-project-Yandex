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

    @parameterized.expand([(-1), (1.5), (0)])
    def test_catalog_pages(self, parameter):

        normal_catalog_check = Client().get("/catalog/1/")
        self.assertEqual(
            normal_catalog_check.status_code, 200, "normal_catalog_check down."
        )

        normal_catalog_re_check = Client().get("/catalog/re/1/")
        self.assertEqual(
            normal_catalog_re_check.status_code,
            200,
            "normal_catalog_re_check down",
        )

        normal_catalog_converter_check = Client().get("/catalog/converter/1/")
        self.assertEqual(
            normal_catalog_converter_check.status_code,
            200,
            "normal_catalog_convrter_check down",
        )

        negative_catalog_re_check = Client().get("/catalog/re/{paramter}/")
        self.assertEqual(
            negative_catalog_re_check.status_code,
            404,
            f"negative_catalog_re_check down. Parameter: {parameter}",
        )

        negative_catalog_converter_check = Client().get(
            f"/catalog/converter/{parameter}/"
        )
        self.assertEqual(
            negative_catalog_converter_check.status_code,
            404,
            f"negative_catalog_converter_check down. Parameter: {parameter}",
        )
        if parameter == 0:
            self.skipTest(
                "Следующий тест пропущен, "
                "тк по адресу /catalog/<param> допустим 0"
            )
        negative_catalog_check = Client().get(f"/catalog/{parameter}/")
        self.assertEqual(
            negative_catalog_check.status_code,
            404,
            "negative_catalog_check down",
        )
