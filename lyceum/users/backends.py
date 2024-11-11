import django.contrib.auth
import django.contrib.auth.backends

import users.models


__all__ = []


class LoginBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username, password):
        try:
            user = users.models.ProxyUser.objects.get(email=username)
        except users.models.ProxyUser.DoesNotExist:
            try:
                user = users.models.ProxyUser.objects.get(username=username)
            except users.models.ProxyUser.DoesNotExist:
                return None

        return (
            user
            if user.check_password(password)
            and self.user_can_authenticate(user)
            else None
        )

    def get_user(self, user_id):
        try:
            return users.models.ProxyUser.objects.get(pk=user_id)
        except users.models.ProxyUser.DoesNotExist:
            return None
