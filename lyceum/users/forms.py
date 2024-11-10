from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import Profile, User

__all__ = ()


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Обязательно")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
            "password1",
            "password2",
        )


class UserChangeForm(UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
        )


class ProfileChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        self.fields["image"].widget.attrs["type"] = "file"

    class Meta:
        model = Profile
        fields = (
            Profile.birthday.field.name,
            Profile.image.field.name,
            Profile.coffee_count.field.name,
        )
        widgets = {
            Profile.coffee_count.field.name: (
                forms.NumberInput(attrs={"disabled": True})
            ),
        }
