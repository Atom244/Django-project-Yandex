import pathlib

import django.conf
import django.contrib.auth.models
from django.contrib.auth.models import User
import django.core.mail
from django.core.management import ManagementUtility
import django.db
from django.urls import reverse
import sorl


__all__ = []


utility = ManagementUtility()
command_args = utility.argv

if "makemigrations" not in command_args and "migrate" not in command_args:
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

    def normalize_email(self, email):
        if not email or "@" not in email:
            return None

        email = email.lower().strip()
        left_part, domain_part = email.split("@", 1)

        # Удаляем "+..." и нормализуем домен
        left_part = left_part.split("+", 1)[0]
        domain_part = domain_part.replace("ya.ru", "yandex.ru")

        # Особая обработка для доменов Gmail и Yandex
        if domain_part == "gmail.com":
            left_part = left_part.replace(".", "")
        elif domain_part == "yandex.ru":
            left_part = left_part.replace(".", "-")

        return f"{left_part}@{domain_part}"

    def by_mail(self, email):
        normalized_email = self.normalize_email(email)
        return self.get_queryset().get(email=normalized_email)


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

    attempts_count = django.db.models.PositiveIntegerField(default=0)
    activation_sent_at = django.db.models.DateTimeField(null=True, blank=True)

    def send_reactivation_email(self, request):
        activation_link = request.build_absolute_uri(
            reverse(
                "users:reactivate",
                kwargs={"username": self.user.username},
            ),
        )

        msg_text = (
            "Ваш аккаунт был заблокирован из-за слишком большого количества "
            "неудачных попыток входа. Для активации перейдите по ссылке, "
            "указанной в данном письме.\n"
            f"Ссылка для активации (действительна неделю): {activation_link}"
        )

        django.core.mail.send_mail(
            "Активация аккаунта",
            msg_text,
            django.conf.settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            fail_silently=False,
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

    class Meta(django.contrib.auth.models.User.Meta):
        proxy = True
