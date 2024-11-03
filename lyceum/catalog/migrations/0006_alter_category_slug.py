# Generated by Django 4.2.16 on 2024-11-03 12:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_alter_tag_name_alter_tag_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Напишите слаг (макс. кол-во символов 200)",
                max_length=200,
                unique=True,
                validators=[django.core.validators.MinLengthValidator(2)],
                verbose_name="слаг",
            ),
        ),
    ]