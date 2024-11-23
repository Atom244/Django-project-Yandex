import datetime

import django.conf
from django.contrib.auth.models import User
from django.core import mail
import django.test
from django.test import Client, override_settings
from django.urls import reverse
from freezegun import freeze_time
from parameterized import parameterized

import users.context_processors
from users.models import Profile

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
        self.profile = Profile.objects.create(user=self.user)
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


class BirthdayContextTests(django.test.TestCase):
    def setUp(self):
        self.factory = django.test.RequestFactory()

        self.user_with_birthday = User.objects.create_user(
            username="with_birthday",
            email="with_birthday@example.com",
            password="password",
        )
        self.user_with_birthday_profile = Profile.objects.create(
            user=self.user_with_birthday,
            birthday=datetime.datetime(year=1990, month=11, day=21),
        )

        self.user_without_birthday = User.objects.create_user(
            username="without_birthday",
            email="without_birthday@example.com",
            password="password",
        )

        self.user_without_birthday_profile = Profile.objects.create(
            user=self.user_without_birthday,
        )

    @freeze_time("2024-11-21")
    def test_birthday_context_no_timezone(self):
        request = self.factory.get(django.urls.reverse("homepage:home"))
        context = users.context_processors.birthday_context(request)
        self.assertIn("birthday_users", context)
        self.assertEqual(len(context["birthday_users"]), 1)
        self.assertEqual(
            context["birthday_users"][0]["username"],
            "with_birthday",
        )

    @freeze_time("2024-11-21")
    def test_birthday_context_with_valid_timezone(self):
        request = self.factory.get(django.urls.reverse("homepage:home"))
        request.COOKIES["timezone"] = "Europe/Moscow"
        context = users.context_processors.birthday_context(request)
        self.assertIn("birthday_users", context)
        self.assertEqual(len(context["birthday_users"]), 1)
        self.assertEqual(
            context["birthday_users"][0]["username"],
            "with_birthday",
        )

    @freeze_time("2024-11-21")
    def test_birthday_context_with_invalid_timezone(self):
        request = self.factory.get(django.urls.reverse("homepage:home"))
        request.COOKIES["timezone"] = "Invalid/Timezone"
        context = users.context_processors.birthday_context(request)
        self.assertIn("birthday_users", context)
        self.assertEqual(len(context["birthday_users"]), 1)
        self.assertEqual(
            context["birthday_users"][0]["username"],
            "with_birthday",
        )

    @freeze_time("2024-11-21")
    def test_birthday_context_with_no_birthday_today(self):
        request = self.factory.get(django.urls.reverse("homepage:home"))
        self.user_with_birthday_profile.birthday = datetime.datetime(
            year=1870,
            month=4,
            day=22,
        )
        self.user_with_birthday_profile.save()
        context = users.context_processors.birthday_context(request)
        self.assertIn("birthday_users", context)
        self.assertEqual(len(context["birthday_users"]), 0)
