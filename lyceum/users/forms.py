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
        email = cleaned_data.get("email")

        normalized_email = User.objects.normalize_email(email)
        cleaned_data["email"] = normalized_email

        if User.objects.filter(email=normalized_email).exists():
            raise django.forms.ValidationError(
                "Этот email уже зарегистрирован",
            )

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
