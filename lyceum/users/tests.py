import django.conf
from django.contrib.auth.models import User
import django.test
import django.urls
import parameterized


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
        django.test.Client().post(
            django.urls.reverse("users:signup"),
            data=self.signup_data,
            follow=True,
        )
        self.assertEqual(
            count + 1,
            User.objects.count(),
        )

    @parameterized.parameterized.expand(
        [
            ("active_user",),
            ("test2@mail.com",),
        ],
    )
    def test_login(self, username):
        login_data_by_mail = {
            "username": username,
            "password": "passwoo231231",
        }
        self.client.post(
            django.urls.reverse("users:login"),
            data=login_data_by_mail,
            follow=True,
        )

        user_context = self.client.get(
            django.urls.reverse("homepage:home"),
        ).context["user"]

        self.assertEqual(user_context.username, "active_user")
