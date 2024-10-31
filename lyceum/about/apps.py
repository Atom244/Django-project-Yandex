from django.apps import AppConfig

__all__ = []


class AboutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "about"
    verbose_name = "О проекте"
