import django.db.models

__all__ = []


class Feedback(django.db.models.Model):
    class StatusChoices(django.db.models.TextChoices):
        GOT = ("GT", "получено")
        IN_POCESSING = ("PR", "в обработке")
        DONE = ("OK", "ответ дан")

    name = django.db.models.TextField(
        "имя отправителя",
        help_text="Имя автора обращения",
        null=True,
        blank=True,
    )

    text = django.db.models.TextField(
        "текстовое поле",
        help_text="Текст обращения",
    )

    created_on = django.db.models.DateTimeField(
        "дата и время создания",
        help_text="Дата и время создания обращения",
        auto_now_add=True,
        null=True,
    )

    mail = django.db.models.EmailField(
        "почта",
        help_text="Электронный адрес отправителя",
    )

    status = django.db.models.CharField(
        "статус обработки",
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.GOT,
    )

    def __str__(self):
        return self.text[:15]


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        to=django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="user",
        help_text="пользователь",
        related_query_name="user",
    )

    timestamp = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )

    feedback = django.db.models.ForeignKey(
        to=Feedback,
        on_delete=django.db.models.CASCADE,
        related_name="feedback",
        related_query_name="feedback",
        help_text="фидбек",
    )

    from_status = django.db.models.CharField(
        "начальное состояние",
        max_length=2,
        db_column="from",
    )

    to = django.db.models.CharField(
        "новое состояние",
        max_length=2,
    )

    class Meta:
        verbose_name = "лог статусов"
        verbose_name_plural = "логи статусов"
