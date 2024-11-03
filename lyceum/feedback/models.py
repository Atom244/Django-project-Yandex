import django.db.models


class Feedback(django.db.models.Model):
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

    mail = django.db.models.TextField(
        "почта",
        help_text="Электронный адрес отправителя",
    )

    def __str__(self):
        return self.text[:15]
