import django.core.validators
import django.forms

import feedback.models


__all__ = []


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control my-1"
            field.field.widget.attrs["placeholder"] = field.field.label

    name = django.forms.CharField(
        label="Имя",
        help_text="Имя автора письма",
        required=False,
    )
    text = django.forms.CharField(
        label="Текст отзыва",
        help_text="Оставьте отзыв",
        widget=django.forms.Textarea,
    )

    mail = django.forms.EmailField(
        label="Почта",
        help_text="Ваш электронный адрес",
        validators=[
            django.core.validators.EmailValidator(
                message="Некорректный e-mail адрес",
            ),
        ],
    )

    class Meta:
        model = feedback.models.Feedback
        exclude = ["name", "text", "mail", "created_on"]
