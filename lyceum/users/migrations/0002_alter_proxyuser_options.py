# Generated by Django 4.2.16 on 2024-11-11 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="proxyuser",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
    ]