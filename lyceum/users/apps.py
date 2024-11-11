from django.apps import AppConfig

__all__ = []


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "пользователи"
