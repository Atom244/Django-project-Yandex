import pathlib
import sys

from django.contrib.auth.models import User
import django.db
import sorl


__all__ = []

if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    User._meta.get_field("email")._unique = True


class UserManager(django.contrib.auth.models.UserManager):
    def active(self):
        return (
            self.get_queryset().filter(is_active=True).only("id", "username")
        )

    def get_user_detail(self, pk):
        return (
            self.get_queryset()
            .filter(pk=pk)
            .select_related("profile")
            .only(
                "first_name",
                "last_name",
                "profile__image",
                "profile__birthday",
                "profile__coffee_count",
            )
        )

    def by_mail(self, email):
        return self.get_queryset().get(email=email)


class Profile(django.db.models.Model):
    def get_avatar_path(self, filename):
        return (
            pathlib.Path("users")
            / f"avatar_user_{str(self.user.id)}.{filename.split('.')[-1]}"
        )

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.deletion.CASCADE,
    )

    birthday = django.db.models.DateField(
        "дата рождения",
        blank=True,
        null=True,
    )

    image = django.db.models.ImageField(
        "аватарка",
        blank=True,
        null=True,
        upload_to=get_avatar_path,
    )

    coffee_count = django.db.models.PositiveIntegerField(
        "счётчик кофе",
        default=0,
    )

    def get_image_x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.get_image_x300().url}">',
            )

        return "изображения нет"

    image_tmb.short_description = "превью (300x300)"
    image_tmb.allow_tags = True

    class Meta:
        verbose_name = "дополнительное поле"
        verbose_name_plural = "дополнительные поля"


class ProxyUser(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True
