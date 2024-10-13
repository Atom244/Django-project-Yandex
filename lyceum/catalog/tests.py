from catalog.models import Category, Item

from django.core.exceptions import ValidationError
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

    @parameterized.expand(
        [
            (-1, 404),
            (1.5, 404),
            (1, 200),
            (0, 200),
        ]
    )
    def test_catalog(self, parameter, code):
        response = Client().get(f"/catalog/{parameter}/")
        self.assertEqual(
            response.status_code,
            code,
            f"catalog_check failed with parameter: {parameter}",
        )

    @parameterized.expand(
        [
            ("/re", -1, 404),
            ("/re", 1.5, 404),
            ("/re", 1, 200),
            ("/re", 0, 404),
            ("/converter", -1, 404),
            ("/converter", 1.5, 404),
            ("/converter", 1, 200),
            ("/converter", 0, 404),
        ]
    )
    def test_re_and_converter(self, path, parameter, code):
        response = Client().get(f"/catalog{path}/{parameter}/")
        self.assertEqual(
            response.status_code,
            code,
            f"Check failed. path: {path}, parameter: {parameter}",
        )


class ItemModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(slug="test-slug")

    def test_custom_validator_positive(self):
        item = Item.objects.create(
            text="Это превосходно", category=self.category
        )
        self.assertEqual(
            item.text, "Это превосходно", "test_custom_validator_positive down"
        )

    def test_custom_validator_negative(self):
        item = Item(text="Обычный текст", category=self.category)
        with self.assertRaises(
            ValidationError, msg="test_custom_validator_negative down"
        ):
            item.full_clean()
