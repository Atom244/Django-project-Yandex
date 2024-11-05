import django.conf
import django.db.models

__all__ = []


class PersonalData(django.db.models.Model):
    name = django.db.models.TextField(
        "имя отправителя",
        help_text="Имя автора обращения",
        null=True,
        blank=True,
    )
    mail = django.db.models.EmailField(
        "почта",
        help_text="Электронный адрес отправителя",
    )

    def __str__(self):
        return f"{self.name} ({self.mail})"

    class Meta:
        verbose_name = "персональная информация"
        verbose_name_plural = "персональные данные"


class Feedback(django.db.models.Model):
    class StatusChoices(django.db.models.TextChoices):
        GOT = ("GT", "получено")
        IN_PROCESSING = ("PR", "в обработке")
        DONE = ("OK", "ответ дан")

    personal_data = django.db.models.OneToOneField(
        PersonalData,
        on_delete=django.db.models.CASCADE,
        null=True,
        blank=True,
        related_name="feedbacks",
        verbose_name="персональная информация",
        help_text="Ссылка на персональные данные автора",
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

    status = django.db.models.CharField(
        "статус обработки",
        max_length=2,
        choices=StatusChoices.choices,
        default=StatusChoices.GOT,
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = "фидбек"
        verbose_name_plural = "фидбек"


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        to=django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="status_logs",
        verbose_name="пользователь",
        help_text="имя пользователя, отправившего фидбек",
    )

    timestamp = django.db.models.DateTimeField(
        "время создания",
        auto_now_add=True,
    )

    feedback = django.db.models.ForeignKey(
        to=Feedback,
        on_delete=django.db.models.CASCADE,
        related_name="status_logs",
        verbose_name="фидбек",
        help_text="фидбек пользователя",
    )

    from_status = django.db.models.CharField(
        "начальное состояние",
        max_length=2,
    )

    to = django.db.models.CharField(
        "новое состояние",
        max_length=2,
    )

    class Meta:
        verbose_name = "лог статусов"
        verbose_name_plural = "логи статусов"


class MultipleFile(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        related_name="files",
        verbose_name="файл",
        help_text="файл прикрепленный к фидбеку",
    )

    def get_upload_path(self, filename):
        return f"uploads/files_db/{self.feedback.id}/{filename}"

    file = django.db.models.FileField(
        upload_to=get_upload_path,
        null=True,
    )

    def __str__(self):
        return f"Файл для {self.feedback}"

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"
