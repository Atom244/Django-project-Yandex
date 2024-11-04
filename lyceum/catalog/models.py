import django.core.exceptions
import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from sorl.thumbnail import get_thumbnail

from catalog.managers import (
    ItemManager,
    PublishedCategoryManager,
    PublishedTagManager,
)
from catalog.validators import ValidateMustContain
from core.models import (
    AbstractImage,
    AbstractModel,
    AbstractModelNormalizedName,
)

__all__ = []


class Tag(AbstractModel, AbstractModelNormalizedName):
    objects = PublishedTagManager()

    slug = django.db.models.SlugField(
        verbose_name="слаг",
        help_text="Напишите слаг (макс. кол-во символов 200)",
        max_length=200,
        unique=True,
    )
    name = django.db.models.TextField(
        max_length=150,
        verbose_name="название",
        help_text="Напишите название тега (макс. кол-во символов 150, "
        "название должно быть уникальным)",
        unique=True,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class Category(AbstractModel, AbstractModelNormalizedName):
    objects = PublishedCategoryManager()

    slug = django.db.models.SlugField(
        verbose_name="слаг",
        help_text="Напишите слаг (макс. кол-во символов 200)",
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
        help_text="Напишите название категории (макс. кол-во символов 150, "
        "название должно быть уникальным)",
        unique=True,
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name[:15]


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

    def __str__(self):
        return f"Главное изображение для {self.item.name}"


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

    def __str__(self):
        return f"Доп. изображение для {self.item.name}"
