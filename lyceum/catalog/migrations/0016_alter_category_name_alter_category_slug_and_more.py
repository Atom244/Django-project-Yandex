# Generated by Django 4.2.16 on 2024-10-30 12:49

import catalog.models
import catalog.validators
import django.core.validators
from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0015_galleryimage_alter_mainimage_image_delete_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.TextField(
                help_text="Напишите название категории (макс кол-во символов 150, название должно быть уникальным)",
                max_length=150,
                unique=True,
                validators=[catalog.models.validate_unique_normalized_name],
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Напишите слаг (макс кол-во символов 200)",
                max_length=200,
                unique=True,
                validators=[django.core.validators.MinLengthValidator(2)],
                verbose_name="слаг",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="weight",
            field=models.PositiveSmallIntegerField(
                default=100,
                help_text="Напишите Вес товара (минимум 1, максимум 32767)",
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(32767),
                ],
                verbose_name="вес",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="text",
            field=django_ckeditor_5.fields.CKEditor5Field(
                help_text="Напишите описание товара (должно содержать 'роскошно' или 'превосходно')",
                validators=[
                    catalog.validators.ValidateMustContain(
                        "роскошно", "превосходно"
                    )
                ],
                verbose_name="текст",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.TextField(
                help_text="Напишите название тега (макс кол-во символов 150, название должно быть уникальным)",
                max_length=150,
                unique=True,
                validators=[catalog.models.validate_unique_normalized_name],
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
                help_text="Напишите слаг (макс кол-во символов 200)",
                max_length=200,
                unique=True,
                verbose_name="слаг",
            ),
        ),
    ]
