import django.contrib.auth.forms
from django.contrib.auth.models import User
import django.forms
import django.forms.fields

from users.models import Profile, ProxyUser


__all__ = []


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(
        required=True,
    )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = django.contrib.auth.models.User

        fields = [
            User.username.field.name,
            User.email.field.name,
        ]


class ProfileEditForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[Profile.coffee_count.field.name].disabled = True
        self.fields[Profile.birthday.field.name].widget = (
            django.forms.fields.TextInput(
                {
                    "type": "date",
                },
            )
        )

    class Meta:
        model = Profile

        fields = [
            Profile.birthday.field.name,
            Profile.image.field.name,
            Profile.coffee_count.field.name,
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data["email"].lower().strip()
        left_part = email.split("@")[0].replace("+", "")
        right_part = email.split("@")[1].replace("ya.ru", "yandex.ru")
        if right_part == "gmail.com":
            left_part = left_part.replace(".", "")
        elif right_part == "yandex.ru":
            left_part = left_part.replace(".", "-")

        cleaned_data["email"] = left_part + "@" + right_part
        if User.objects.filter(email=email).exists():
            raise django.forms.ValidationError("This mail already registered")

        return cleaned_data


class UserEditForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = ProxyUser

        fields = [
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        ]
