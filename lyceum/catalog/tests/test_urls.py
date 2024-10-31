from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import NoReverseMatch, reverse
from parameterized import parameterized


class StaticURLTest(TestCase):
    def test_catalog_page_endpoint(self):
        norm_url = reverse("catalog:item_list")
        normal_catalog_check = Client().get(norm_url)
        self.assertEqual(
            normal_catalog_check.status_code,
            HTTPStatus.OK,
            "normal_catalog_check down",
        )

        wrong_catalog_check = Client().get("/catalogE/")
        self.assertEqual(
            wrong_catalog_check.status_code,
            HTTPStatus.NOT_FOUND,
            "wrong_catalog_check down",
        )

    @parameterized.expand(
        [
            (-1, HTTPStatus.NOT_FOUND),
            (1.5, HTTPStatus.NOT_FOUND),
            (-0, HTTPStatus.OK),
            ("1FH#@KKl", HTTPStatus.NOT_FOUND),
            ("0lff9", HTTPStatus.NOT_FOUND),
            ("&hge59", HTTPStatus.NOT_FOUND),
            ("$h78", HTTPStatus.NOT_FOUND),
            (1, HTTPStatus.OK),
            (10, HTTPStatus.OK),
            (100, HTTPStatus.OK),
            (0, HTTPStatus.OK),
            ("01", HTTPStatus.OK),
            ("010", HTTPStatus.OK),
        ],
    )
    def test_catalog(self, parameter, code):
        try:
            url = reverse("catalog:item_detail", kwargs={"pk": parameter})
            response = Client().get(url)

            self.assertEqual(
                response.status_code,
                code,
                f"catalog_check failed with parameter: {parameter}",
            )
        except NoReverseMatch:
            self.assertEqual(
                code,
                HTTPStatus.NOT_FOUND,
                f"Ожидалось 404 по: {parameter}, но получили NoReverseMatch.",
            )
