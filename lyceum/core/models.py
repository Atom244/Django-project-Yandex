import django.db.models


class AbstractModel(django.db.models.Model):
    id = django.db.models.AutoField(primary_key=True, verbose_name="id")
    is_published = django.db.models.BooleanField(
        default=True, verbose_name="Опубликовано"
    )
    name = django.db.models.TextField(
        max_length=150,
        verbose_name="Название",
        help_text="Напишите название товара",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
