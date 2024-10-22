from django.apps import AppConfig

__all__ = ["CoreConfig"]


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
