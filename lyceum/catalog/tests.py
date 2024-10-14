from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from parameterized import parameterized

from catalog import models


class StaticURLTests(TestCase):
    def test_catalog_page_endpoint(self):
        normal_catalog_check = Client().get("/catalog/")
        self.assertEqual(
            normal_catalog_check.status_code,
            200,
            "normal_catalog_check down",
        )

        wrong_catalog_check = Client().get("/catalogE/")
        self.assertEqual(
            wrong_catalog_check.status_code,
            404,
            "wrong_catalog_check down",
        )

    @parameterized.expand(
        [
            (-1, 404),
            (1.5, 404),
            (1, 200),
            (0, 200),
        ],
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
        ],
    )
    def test_re_and_converter(self, path, parameter, code):
        response = Client().get(f"/catalog{path}/{parameter}/")
        self.assertEqual(
            response.status_code,
            code,
            f"Check failed. path: {path}, parameter: {parameter}",
        )


class ItemModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = models.Category.objects.create(
            is_published=True,
            name="test-name",
            slug="test-category-slug",
            weight=100,
        )
        cls.tag = models.Tag.objects.create(
            is_published=True,
            name="test-tag",
            slug="test-tag-slug",
        )

    @parameterized.expand(
        [
            ("РоСкоШно",),
            ("ПреВоСходно",),
            ("роскошно",),
            ("превосходно",),
            ("!РоСкоШно",),
            ("ПреВоСходно!",),
            ("!!роскошно",),
            ("?превосходно!?",),
            ("(роскошно)",),
            ("(превосходно!)",),
        ],
    )
    def test_custom_validator_positive(self, parameter):
        item_count = models.Item.objects.count()

        self.item = models.Item(
            name="Тестовый товар",
            text=parameter,
            category=self.category,
        )
        self.item.full_clean()
        self.item.save()

        self.item.tags.add(ItemModelTest.tag)

        self.assertEqual(
            models.Item.objects.count(),
            item_count + 1,
            f"test_custom_validator_positive down слово: {parameter}",
        )

    @parameterized.expand(
        [
            ("Другое",),
            ("нету слова",),
            ("Раскошно",),
        ],
    )
    def test_custom_validator_negative(self, parameter):
        item_count = models.Item.objects.count()

        with self.assertRaises(
            ValidationError,
            msg="test_custom_validator_negative down " f"слово: {parameter}",
        ):
            self.item = models.Item(
                name="Тестовый товар",
                text=parameter,
                category=self.category,
            )
            self.item.full_clean()
            self.item.save()

            self.item.tags.add(ItemModelTest.tag)

        self.assertEqual(
            models.Item.objects.count(),
            item_count,
            f"test_custom_validator_negative down слово: {parameter}",
        )
