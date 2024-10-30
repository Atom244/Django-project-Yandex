# Generated by Django 4.2.16 on 2024-10-29 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0011_rename_id_category_item_id_rename_id_item_item_id_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="время создания"
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                null=True,
                verbose_name="время последнего изменения",
            ),
        ),
    ]