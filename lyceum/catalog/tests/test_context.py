from django.db.models.query import QuerySet
from django.test import Client, TestCase
from django.urls import reverse
import freezegun
from parameterized import parameterized

from catalog import models


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
