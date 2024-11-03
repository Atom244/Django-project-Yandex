# Generated by Django 4.2.16 on 2024-11-03 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("feedback", "0003_feedback_status_statuslog"),
    ]

    operations = [
        migrations.AddField(
            model_name="statuslog",
            name="feedback",
            field=models.ForeignKey(
                help_text="фидбек",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedback",
                related_query_name="feedback",
                to="feedback.feedback",
            ),
        ),
    ]
