from django.apps import AppConfig

__all__ = []


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"
    verbose_name = "статистика"
