from django.apps import AppConfig

__all__ = ["AboutConfig"]


class AboutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "about"
