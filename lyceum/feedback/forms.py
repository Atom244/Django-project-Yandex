import django.core.validators
import django.forms

import feedback.models


__all__ = []


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]

        return result


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

    file_field = MultipleFileField(
        label="Загрузить файлы",
        help_text="Вы можете загрузить несколько файлов",
    )

    class Meta:
        model = feedback.models.Feedback
        exclude = [
            "name",
            "text",
            "mail",
            "files",
            "created_on",
            "status",
            "personal_data",
        ]
