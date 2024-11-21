from django.contrib.auth.models import User
from django.utils.timezone import now

__all__ = []


def birthday_context(request):
    today = now().date()
    user_timezone = request.COOKIES.get("timezone")

    if user_timezone:
        import pytz

        try:
            user_tz = pytz.timezone(user_timezone)
            today = now().astimezone(user_tz).date()
        except pytz.UnknownTimeZoneError:
            pass

    birthday_users = User.objects.filter(
        is_active=True,
        profile__birthday__day=today.day,
        profile__birthday__month=today.month,
    ).values("username", "email", "first_name")

    return {"birthday_users": birthday_users}
