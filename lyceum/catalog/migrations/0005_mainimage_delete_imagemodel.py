# Generated by Django 4.2.16 on 2024-10-22 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_remove_item_images_imagemodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="MainImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "images",
                    models.ImageField(
                        blank=True,
                        upload_to="catalog/",
                        verbose_name="изображения",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="изображения",
                        to="catalog.item",
                        verbose_name="товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение",
                "verbose_name_plural": "изображения",
            },
        ),
        migrations.DeleteModel(
            name="ImageModel",
        ),
    ]