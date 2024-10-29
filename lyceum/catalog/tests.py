from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.test import Client, TestCase
from django.urls import NoReverseMatch, reverse
import freezegun
from parameterized import parameterized

from catalog import models


__all__ = ["StaticURLTests", "ItemModelTest", "NormalizeNameTests"]


class StaticURLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = models.Category.objects.create(
            name="Тестовая категория",
            slug="test-category",
            weight=10,
        )

        tag = models.Tag.objects.create(
            name="Тестовый тег",
            slug="test-tag",
        )

        cls.item = models.Item.objects.create(
            name="Тестовый товар",
            text="Это описание товара, содержащее роскошно и превосходно.",
            category=category,
            is_on_main=True,
        )

        cls.item.tags.add(tag)

        cls.client = Client()

    def test_catalog_page_endpoint(self):
        norm_url = reverse("catalog:item_list")
        normal_catalog_check = Client().get(norm_url)
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
            (0, 404),
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
                404,
                f"Ожидалось 404 по: {parameter}, но получили NoReverseMatch.",
            )

    @parameterized.expand(
        [
            ("re", -1, 404),
            ("re", 1.5, 404),
            ("re", 1, 200),
            ("re", 0, 404),
            ("converter", -1, 404),
            ("converter", 1.5, 404),
            ("converter", 1, 200),
            ("converter", 0, 200),
        ],
    )
    def test_re_and_converter(self, path, parameter, code):
        try:
            url = reverse(f"catalog:{path}", kwargs={"num": parameter})
            response = Client().get(url)

            self.assertEqual(
                response.status_code,
                code,
                f"catalog_check failed with parameter: {parameter}",
            )
        except NoReverseMatch:
            self.assertEqual(
                code,
                404,
                f"Ожидалось 404 по: {parameter} путь: {path},"
                " но получили NoReverseMatch.",
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


class ContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.published_category = models.Category.objects.create(
            is_published=True,
            name="Опубликованная категория",
            slug="published-category",
            weight=100,
        )
        cls.unpublished_category = models.Category.objects.create(
            is_published=False,
            name="Неопубликованная категория",
            slug="unpublished-category",
            weight=100,
        )

        cls.published_tag = models.Tag.objects.create(
            is_published=True,
            name="Опубликованный тег",
            slug="published-tag",
        )
        cls.unpublished_tag = models.Tag.objects.create(
            is_published=True,
            name="Неопубликованный тег",
            slug="unpublished-tag",
        )

        cls.published_category.clean()
        cls.unpublished_category.clean()
        cls.published_tag.clean()
        cls.unpublished_tag.clean()

        cls.published_category.save()
        cls.unpublished_category.save()
        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.published_item_on_main = models.Item.objects.create(
            name="Published on main item",
            category=cls.published_category,
            text="роскошно",
            is_on_main=True,
        )

        cls.unpublished_item_on_main = models.Item.objects.create(
            name="Unpublished on main item",
            category=cls.unpublished_category,
            text="роскошно",
            is_on_main=True,
        )

        cls.published_item_on_main.clean()

        cls.unpublished_item_on_main.clean()

        cls.published_item_on_main.save()

        cls.unpublished_item_on_main.save()

        cls.published_item_on_main.tags.add(cls.published_tag)

        cls.unpublished_item_on_main.tags.add(cls.unpublished_tag)

        with freezegun.freeze_time("01-06-2023"):
            cls.published_item_friday = models.Item(
                name="Published item Friday",
                category=cls.published_category,
                text="роскошно fd",
            )
            cls.published_item_friday.clean()
            cls.published_item_friday.save()
            cls.published_item_friday.tags.add(cls.published_tag)

    def test_home_page_show_correct_context(self):
        response = Client().get(reverse("homepage:home"))
        self.assertIn("items", response.context)

    def test_home_count_item(self):
        response = Client().get(reverse("homepage:home"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_type_of_context(self):
        response = Client().get(reverse("homepage:home"))
        items = response.context["items"]
        self.assertIsInstance(items, QuerySet)

    @parameterized.expand(
        [
            ("homepage:home"),
            ("catalog:item_list"),
        ],
    )
    def test_excluding_bad_attributes_in_querysets(self, app_url):
        response = Client().get(reverse(app_url))
        items = response.context["items"]
        item_attributes = items[0].__dict__
        tag_attributes = item_attributes["_prefetched_objects_cache"]["tags"][
            0
        ].__dict__
        self.assertNotIn("is_published", item_attributes)
        self.assertNotIn("images", item_attributes)
        self.assertNotIn("is_published", tag_attributes)

    @parameterized.expand(
        [
            ("homepage:home", 1),
            ("catalog:item_list", 2),
        ],
    )
    def test_published_item_count(self, app_url, correct_count):
        response = Client().get(reverse(app_url))
        items = response.context["items"]
        self.assertEqual(len(items), correct_count)

    def test_context_new(self):
        response = Client().get(reverse("catalog:new"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_context_friday(self):
        response = Client().get(reverse("catalog:friday"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_context_unverified(self):
        response = Client().get(reverse("catalog:unverified"))
        items = response.context["items"]
        self.assertEqual(len(items), 2)
