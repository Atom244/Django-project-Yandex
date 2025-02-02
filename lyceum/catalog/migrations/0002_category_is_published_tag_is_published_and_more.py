# Generated by Django 4.2.16 on 2024-10-31 11:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="is_published",
            field=models.BooleanField(
                default=True, verbose_name="опубликовано"
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="is_published",
            field=models.BooleanField(
                default=True, verbose_name="опубликовано"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.TextField(
                help_text="Напишите название категории (макс кол-во символов 150, название должно быть уникальным)",
                max_length=150,
                unique=True,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="normalized_name",
            field=models.CharField(
                editable=False,
                max_length=150,
                null=True,
                verbose_name="нормализованное имя",
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
            model_name="tag",
            name="name",
            field=models.TextField(
                help_text="Напишите название тега (макс кол-во символов 150, название должно быть уникальным)",
                max_length=150,
                unique=True,
                verbose_name="название",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="normalized_name",
            field=models.CharField(
                editable=False,
                max_length=150,
                null=True,
                verbose_name="нормализованное имя",
            ),
        ),
    ]
