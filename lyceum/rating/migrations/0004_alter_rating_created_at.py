# Generated by Django 4.2.16 on 2024-11-24 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rating", "0003_rating_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="created_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
