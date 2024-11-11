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


class UserEditForm(django.contrib.auth.forms.UserChangeForm):
    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = ProxyUser

        fields = [
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        ]
