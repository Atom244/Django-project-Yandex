import django.conf
from django.contrib.auth.models import User
from django.core import mail
import django.test
from django.test import Client, override_settings
from django.urls import reverse
from parameterized import parameterized

import users.models

__all__ = []


class UsersTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.signup_data = {
            "email": "test@mail.ru",
            "username": "test_username_lol",
            "password1": "asdkl;u@MKF4",
            "password2": "asdkl;u@MKF4",
        }

        cls.active_user = User.objects.create_user(
            username="active_user",
            email="test2@mail.com",
            password="passwoo231231",
            is_active=True,
        )

        cls.nonactive_user = User.objects.create_user(
            username="nonactive_user",
            email="test3@mail.com",
            password="passwoo23231231",
            is_active=False,
        )

    def test_signup_successful(self):
        count = User.objects.count()
        Client().post(
            reverse("users:signup"),
            data=self.signup_data,
            follow=True,
        )
        self.assertEqual(count + 1, User.objects.count())

    @parameterized.expand(
        [
            ("active_user",),
            ("test2@mail.com",),
        ],
    )
    def test_login(self, username):
        login_data = {
            "username": username,
            "password": "passwoo231231",
        }
        self.client.post(
            reverse("users:login"),
            data=login_data,
            follow=True,
        )

        user_context = self.client.get(
            reverse("homepage:home"),
        ).context["user"]

        self.assertEqual(user_context.username, "active_user")

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


class UserLockoutTests(django.test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="correct_password",
        )
        self.profile = users.models.Profile.objects.create(user=self.user)
        self.profile.attempts_count = 0
        self.profile.save()

    @override_settings(DEBUG=False)
    def test_user_lockout_after_failed_attempts(self):
        self.assertTrue(self.user.is_active)

        for _ in range(django.conf.settings.MAX_AUTH_ATTEMPTS):
            self.client.post(
                reverse("users:login"),
                {
                    "username": "testuser",
                    "password": "wrong_password",
                },
            )
            self.user.refresh_from_db()

        self.assertFalse(self.user.is_active)
        self.assertEqual(
            self.user.profile.attempts_count,
            django.conf.settings.MAX_AUTH_ATTEMPTS,
        )

    def test_reactivation_email_sent_on_lockout(self):
        for _ in range(django.conf.settings.MAX_AUTH_ATTEMPTS):
            self.client.post(
                reverse("users:login"),
                {
                    "username": "testuser",
                    "password": "wrong_password",
                },
            )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Активация аккаунта", mail.outbox[0].subject)
        self.assertIn(self.user.email, mail.outbox[0].to)

    def test_successful_login_resets_attempt_count(self):
        self.client.post(
            reverse("users:login"),
            {
                "username": "testuser",
                "password": "wrong_password",
            },
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.attempts_count, 1)

        self.client.post(
            reverse("users:login"),
            {
                "username": "testuser",
                "password": "correct_password",
            },
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.attempts_count, 0)
