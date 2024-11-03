import django.forms


__all__ = []


class EchoForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control my-1"

    text = django.forms.CharField(
        widget=django.forms.Textarea(),
        help_text="Введите текст",
        label="Текст",
    )
