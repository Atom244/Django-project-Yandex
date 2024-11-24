from django.contrib.auth.models import User
from django.db import models

from catalog.models import Item


__all__ = []


class Rating(models.Model):
    RATING_CHOICES = [
        (1, "Ненависть"),
        (2, "Неприязнь"),
        (3, "Нейтрально"),
        (4, "Обожание"),
        (5, "Любовь"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    score = models.IntegerField(choices=RATING_CHOICES)

    created_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
        unique_together = ("user", "item")

    def __str__(self):
        return (
            f"Оценка {self.score} для {self.item.name} от {self.user.username}"
        )
