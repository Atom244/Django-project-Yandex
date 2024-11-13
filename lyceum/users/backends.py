import django.conf
import django.contrib.auth.backends
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone

import users.models

__all__ = []


class LoginBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None):
        user = None

        try:
            validate_email(username)
            is_email = True
        except ValidationError:
            is_email = False

        if is_email:
            try:
                user = users.models.ProxyUser.objects.by_mail(username)
            except users.models.ProxyUser.DoesNotExist:
                return None
        else:
            try:
                user = users.models.ProxyUser.objects.get(username=username)
            except users.models.ProxyUser.DoesNotExist:
                return None

        if not hasattr(user, "profile"):
            user.profile = users.models.Profile.objects.create(user=user)

        if user.check_password(password):
            user.profile.attempts_count = 0
            user.profile.activation_sent_at = None
            user.profile.save()
            return user if self.user_can_authenticate(user) else None

        user.profile.attempts_count += 1
        user.profile.save()
        if (
            user.profile.attempts_count
            >= django.conf.settings.MAX_AUTH_ATTEMPTS
        ):
            user.is_active = False
            user.profile.activation_sent_at = timezone.now()
            user.save()
            user.profile.send_reactivation_email(request)

        return None

    def get_user(self, user_id):
        try:
            return users.models.ProxyUser.objects.get(pk=user_id)
        except users.models.ProxyUser.DoesNotExist:
            return None
