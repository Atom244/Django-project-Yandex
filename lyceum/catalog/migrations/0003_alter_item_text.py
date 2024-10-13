# Generated by Django 4.2.16 on 2024-10-13 10:31

import catalog.models

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_category_tag_item_is_published_item_text_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                help_text="Напишите текст",
                validators=[catalog.models.custom_validator],
                verbose_name="Текст",
            ),
        ),
    ]
