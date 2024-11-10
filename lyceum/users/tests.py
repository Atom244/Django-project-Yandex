from datetime import timedelta
from unittest import mock

from django.test import Client, override_settings, TestCase
from django.urls import reverse
from django.utils import timezone
from parameterized import parameterized

import users.forms
import users.models


__all__ = ("ActivationTests", "SignupTests")


class ActivationTests(TestCase):
    @override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_default_activation_true(self):
        old_len = users.models.User.objects.all().count()
        data = {
            "username": "testuser5",
            "email": "example@gmail.com",
            "password1": "P@ssqwerty",
            "password2": "P@ssqwerty",
        }

        self.assertTrue(users.forms.SignupForm(data).is_valid())
        self.client.post("/auth/signup/", data=data)
        self.assertEqual(users.models.User.objects.all().count(), old_len + 1)
        self.assertTrue(
            users.models.User.objects.get(
                username=data["username"],
            ).is_active,
        )

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_default_activation_false(self):
        old_len = users.models.User.objects.all().count()
        data = {
            "username": "testuser5",
            "email": "example@gmail.com",
            "password1": "P@ssqwerty",
            "password2": "P@ssqwerty",
        }

        self.assertTrue(users.forms.SignupForm(data).is_valid())
        self.client.post("/auth/signup/", data=data)
        self.assertEqual(users.models.User.objects.all().count(), old_len + 1)
        self.assertFalse(
            users.models.User.objects.get(
                username=data["username"],
            ).is_active,
        )


class SignupTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.valid_signup = {
            "email": "example@gmail.com",
            "username": "testuser3",
            "password1": "P@ssqwerty",
            "password2": "P@ssqwerty",
        }
        cls.inactive_now_user = users.models.User.objects.create_user(
            username="testuser4",
            email="example@gmail.com",
            password="P@ssqwerty",
            date_joined=timezone.now(),
            is_active=False,
        )

    @parameterized.expand(
        [
            ["ex@gmail.com", "ex@gmail.com"],
            ["ars.plmr@yandex.ru", "ars-plmr@yandex.ru"],
            ["example@yandex.ru", "example@ya.ru"],
        ],
    )
    def test_normalization_email(self, email1, email2):
        old_users = users.models.User.objects.count()
        Client().post(
            reverse("users:signup"),
            data={
                "username": "username7",
                "email": email1,
                "password1": "P@ssqwerty",
                "password2": "P@ssqwerty",
            },
        )
        Client().post(
            reverse("users:signup"),
            data={
                "username": "username7",
                "email": email2,
                "password1": "P@ssqwerty",
                "password2": "P@ssqwerty",
            },
        )
        self.assertEqual(old_users + 1, users.models.User.objects.count())

    def test_activation_positive_time(self):
        user = self.inactive_now_user
        self.assertFalse(user.is_active)
        Client().get(reverse("users:activate", args=[user.username]))
        user = users.models.User.objects.get(
            username=user.username,
        )
        self.assertTrue(user.is_active)

    @mock.patch("users.views.timezone")
    def test_activation_negative_time(self, mocked_datetime):
        mocked_datetime.now.return_value = timezone.now() + timedelta(hours=8)
        user = self.inactive_now_user
        self.assertFalse(user.is_active)
        Client().get(reverse("users:activate", args=[user.username]))
        self.assertFalse(user.is_active)
