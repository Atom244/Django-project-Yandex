# Generated by Django 4.2.16 on 2024-10-16 16:13

import catalog.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        help_text="Напишите название товара",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "slug",
                    models.TextField(
                        help_text="Напишите слаг",
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(2)
                        ],
                        verbose_name="слаг",
                    ),
                ),
                (
                    "weight",
                    models.PositiveSmallIntegerField(
                        default=100,
                        help_text="Напишите вес товара",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(32767),
                        ],
                        verbose_name="вес",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        help_text="Напишите название товара",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "slug",
                    models.TextField(
                        help_text="Напишите слаг",
                        max_length=200,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="id"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="опубликовано"
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        help_text="Напишите название товара",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Напишите описание товара",
                        validators=[catalog.models.custom_validator],
                        verbose_name="текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.category",
                        verbose_name="категория",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        to="catalog.tag", verbose_name="тег"
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
    ]
