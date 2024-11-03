from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import NoReverseMatch, reverse
from parameterized import parameterized

import catalog.models

__all__ = []


class StaticURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = catalog.models.Category.objects.create(
            name="Тестовая категория",
            slug="test-category",
            weight=10,
        )

        tag = catalog.models.Tag.objects.create(
            name="Тестовый тег",
            slug="test-tag",
        )

        cls.item = catalog.models.Item.objects.create(
            name="Тестовый товар",
            text="Это описание товара, содержащее роскошно и превосходно.",
            category=category,
            is_on_main=True,
        )

        cls.item.tags.add(tag)

        cls.client = Client()

    def test_catalog_page_endpoint(self):
        norm_url = reverse("catalog:item-list")
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
            (-0, HTTPStatus.NOT_FOUND),
            ("1FH#@KKl", HTTPStatus.NOT_FOUND),
            ("0lff9", HTTPStatus.NOT_FOUND),
            ("&hge59", HTTPStatus.NOT_FOUND),
            ("$h78", HTTPStatus.NOT_FOUND),
            (1, HTTPStatus.OK),
            (10, HTTPStatus.NOT_FOUND),
            (100, HTTPStatus.NOT_FOUND),
            (0, HTTPStatus.NOT_FOUND),
            ("01", HTTPStatus.OK),
            ("010", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog(self, parameter, code):
        try:
            url = reverse("catalog:item-detail", kwargs={"pk": parameter})
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
