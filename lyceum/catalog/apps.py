from django.apps import AppConfig

__all__ = ["CatalogConfig"]


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
    verbose_name = "Каталог"
