from django.apps import AppConfig

__all__ = []


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Базовые сущности"
