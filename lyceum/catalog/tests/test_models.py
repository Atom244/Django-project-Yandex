from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized
from catalog import models


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
            ("Какое-то слово и ПреВоСходно да?",),
            ("роскошно",),
            ("превосходно",),
            ("!РоСкоШно",),
            ("ПреВоСходно! описание топ",),
            ("!!роскошно",),
            ("?превосходно!?",),
            ("(роскошно)",),
            ("(превосходно!)",),
            ("(ПрЕВосхоДно!)",),
            ("?превосходно%?",),
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

    @parameterized.expand(
        [
            (100, "test-slug"),
            (1.4, "test-slug-1"),
            (100.37, "test-slug-2"),
        ],
    )
    def test_category_validator_positive(
        self,
        parameter_weight,
        parameter_slug,
    ):
        item_count = models.Category.objects.count()

        self.item = models.Category(
            name="Тестовая категория",
            weight=parameter_weight,
            slug=parameter_slug,
            is_published=True,
        )
        self.item.full_clean()
        self.item.save()

        self.assertEqual(
            models.Category.objects.count(),
            item_count + 1,
            "test_category_validator_positive down params: "
            f"{parameter_weight} {parameter_slug}",
        )

    @parameterized.expand(
        [
            (0, "te"),
            (0.512, "no"),
            (-345, "4"),
        ],
    )
    def test_category_validator_negative(
        self,
        parameter_weight,
        parameter_slug,
    ):
        with self.assertRaises(ValidationError):
            category = models.Category(
                weight=parameter_weight,
                slug=parameter_slug,
                name="test category",
                is_published=True,
            )
            category.full_clean()


class NormalizeNameTests(TestCase):
    @parameterized.expand(
        [
            ("Тег", "тЕГ"),
            ("Яблоко", "ЯблOко"),
            ("Что-то", "чтO-то"),
        ],
    )
    def test_tag_normalization(self, param1, param2):
        models.Tag.objects.create(name=param1)
        tag = models.Tag(name=param2)

        with self.assertRaises(
            ValidationError,
            msg="test_tag_normalization down"
            f"param1: {param1} param2: {param2}",
        ):
            tag.full_clean()

    @parameterized.expand(
        [
            ("Тег", "тЕГ"),
            ("Яблоко", "ЯблOко"),
            ("Что-то", "чтO-то"),
        ],
    )
    def test_category_normalization(self, param1, param2):
        models.Category.objects.create(name=param1)
        tag = models.Category(name=param2)

        with self.assertRaises(
            ValidationError,
            msg="test_category_normalization down"
            f"param1: {param1} param2: {param2}",
        ):
            tag.full_clean()
