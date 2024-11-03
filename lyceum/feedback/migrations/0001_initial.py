# Generated by Django 4.2.16 on 2024-11-03 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                    "name",
                    models.TextField(
                        blank=True,
                        help_text="Имя автора обращения",
                        null=True,
                        verbose_name="имя отправителя",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Текст обращения",
                        verbose_name="текстовое поле",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Дата и время создания обращения",
                        null=True,
                        verbose_name="дата и время создания",
                    ),
                ),
                (
                    "mail",
                    models.TextField(
                        help_text="Электронный адрес отправителя",
                        verbose_name="почта",
                    ),
                ),
            ],
        ),
    ]