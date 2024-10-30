import re

import django.core.exceptions
import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from sorl.thumbnail import get_thumbnail

from catalog.validators import ValidateMustContain
from core.models import AbstractImage, AbstractModel


__all__ = []


def normalize_name(name):
    name = name.lower()

    translation_table = str.maketrans(
        {
            "а": "a",
            "о": "o",
            "е": "e",
            "р": "p",
            "с": "c",
            "у": "y",
            "х": "x",
            "k": "к",
            "A": "a",
            "O": "o",
            "E": "e",
            "P": "p",
            "C": "c",
            "Y": "y",
            "X": "x",
            "K": "к",
        },
    )

    return re.sub(r"[^\w]", "", name.translate(translation_table))


def validate_unique_normalized_name(value):
    normalized_value = normalize_name(value)

    if Tag.objects.filter(normalized_name=normalized_value).exists():
        raise django.core.exceptions.ValidationError(
            "Тег с похожим именем " f"{value} уже существует.",
        )

    if Category.objects.filter(normalized_name=normalized_value).exists():
        raise django.core.exceptions.ValidationError(
            "Категория с похожим именем " f"{value} уже существует.",
        )


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category", "main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=Tag.objects.published().defer("is_published"),
                ),
            )
            .only(
                "name",
                "text",
                "category__name",
                "main_image__image",
            )
        )

    def on_main(self):
        return self.published().filter(is_on_main=True).order_by("name")


class PublishedTagManager(django.db.models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True)


class Tag(AbstractModel):
    objects = PublishedTagManager()

    slug = django.db.models.SlugField(
        verbose_name="слаг",
        help_text="Напишите слаг (макс кол-во символов 200)",
        max_length=200,
        unique=True,
    )
    name = django.db.models.TextField(
        max_length=150,
        verbose_name="название",
        help_text="Напишите название тега (макс кол-во символов 150, "
        "название должно быть уникальным)",
        unique=True,
        validators=[validate_unique_normalized_name],
    )
    normalized_name = django.db.models.CharField(
        max_length=150,
        editable=False,
        null=True,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)


class Category(AbstractModel):
    slug = django.db.models.SlugField(
        verbose_name="слаг",
        help_text="Напишите слаг (макс кол-во символов 200)",
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.MinLengthValidator(2),
        ],
    )
    weight = django.db.models.PositiveSmallIntegerField(
        verbose_name="вес",
        default=100,
        help_text="Напишите Вес товара (минимум 1, максимум 32767)",
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
    )
    name = django.db.models.TextField(
        max_length=150,
        verbose_name="название",
        help_text="Напишите название категории (макс кол-во символов 150, "
        "название должно быть уникальным)",
        unique=True,
        validators=[validate_unique_normalized_name],
    )
    normalized_name = django.db.models.CharField(
        max_length=150,
        editable=False,
        null=True,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name[:15]

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)


class Item(AbstractModel):
    objects = ItemManager()
    text = CKEditor5Field(
        verbose_name="текст",
        help_text="Напишите описание товара (должно содержать 'роскошно' или "
        "'превосходно')",
        validators=[
            ValidateMustContain("роскошно", "превосходно"),
        ],
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        null=True,
        verbose_name="категория",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="тег",
    )

    is_on_main = django.db.models.BooleanField(
        default=False,
        verbose_name="показывать на главной",
    )

    created_at = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
        null=True,
    )
    updated_at = django.db.models.DateTimeField(
        "время последнего изменения",
        auto_now=True,
        null=True,
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]

    def get_main_image_300x300(self):
        if self.main_image and self.main_image.image:
            return get_thumbnail(self.main_image.image, "300x300", quality=51)
        return "Нет изображения"

    def main_image_tmb(self):
        if self.main_image and self.main_image.image:
            return mark_safe(
                f"<img src='{self.main_image.image.url}' width='50'>",
            )
        return "Нет изображения"

    main_image_tmb.short_description = "Превью"
    main_image_tmb.allow_tags = True


class MainImage(AbstractImage):
    item = django.db.models.OneToOneField(
        Item,
        verbose_name="товар",
        on_delete=django.db.models.deletion.CASCADE,
        null=True,
        related_name="main_image",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class GalleryImage(AbstractImage):
    item = django.db.models.ForeignKey(
        Item,
        verbose_name="товар",
        on_delete=django.db.models.deletion.CASCADE,
        related_name="images",
        related_query_name="image",
    )

    class Meta:
        verbose_name = "доп. изображение"
        verbose_name_plural = "галерея"
