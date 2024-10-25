import re

import django.core.exceptions
import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from sorl.thumbnail import get_thumbnail

from catalog.validators import ValidateMustContain
from core.models import AbstractModel


__all__ = ["Tag", "Category", "Item", "MainImage"]


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
    name = name.translate(translation_table)

    name = re.sub(r"[^\w]", "", name)

    return name


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


class Tag(AbstractModel):
    slug = django.db.models.TextField(
        verbose_name="слаг",
        help_text="Напишите Слаг",
        max_length=200,
        unique=True,
    )
    name = django.db.models.TextField(
        max_length=150,
        verbose_name="название",
        help_text="Напишите название товара",
        unique=True,
        validators=[validate_unique_normalized_name],
    )
    normalized_name = django.db.models.CharField(
        max_length=150,
        editable=False,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    slug = django.db.models.TextField(
        verbose_name="слаг",
        help_text="Напишите Слаг",
        max_length=200,
        unique=True,
        validators=[
            django.core.validators.MinLengthValidator(2),
        ],
    )
    weight = django.db.models.PositiveSmallIntegerField(
        verbose_name="вес",
        default=100,
        help_text="Напишите Вес товара",
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
    )
    name = django.db.models.TextField(
        max_length=150,
        verbose_name="название",
        help_text="Напишите название товара",
        unique=True,
        validators=[validate_unique_normalized_name],
    )
    normalized_name = django.db.models.CharField(
        max_length=150,
        editable=False,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.normalized_name = normalize_name(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    text = CKEditor5Field(
        verbose_name="текст",
        help_text="Напишите описание товара",
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

    def get_main_image_300x300(self):
        if self.main_image and self.main_image.image:
            return get_thumbnail(self.main_image.image, "300x300", quality=51)
        else:
            return "Нет изображения"

    def main_image_tmb(self):
        if self.main_image and self.main_image.image:
            return mark_safe(
                f"<img src='{self.main_image.image.url}' width='50'>",
            )
        else:
            return "Нет изображения"

    main_image_tmb.short_description = "Превью"
    main_image_tmb.allow_tags = True

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class MainImage(django.db.models.Model):
    item = django.db.models.OneToOneField(
        Item,
        verbose_name="товар",
        on_delete=django.db.models.deletion.CASCADE,
        null=True,
        related_name="main_image",
    )

    image = django.db.models.ImageField(
        "главное изображение",
        upload_to="catalog/",
        blank=True,
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"


class Images(django.db.models.Model):
    item = django.db.models.ForeignKey(
        Item,
        verbose_name="товар",
        on_delete=django.db.models.deletion.CASCADE,
        related_name="images",
        related_query_name="image",
    )

    image = django.db.models.ImageField(
        "доп. изображение",
        upload_to="catalog/",
        blank=True,
    )

    class Meta:
        verbose_name = "доп. изображение"
        verbose_name_plural = "доп. изображения"
