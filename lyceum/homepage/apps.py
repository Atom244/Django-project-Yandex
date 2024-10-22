from django.apps import AppConfig

__all__ = ["HomepageConfig"]


class HomepageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"
