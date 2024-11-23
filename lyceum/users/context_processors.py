from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from django.db.models import Q

__all__ = []


def birthday_context(request):
    now = datetime.now(timezone.utc)

    earliest_time = now - timedelta(hours=12)
    latest_time = now + timedelta(hours=14)

    earliest_date = earliest_time.date()
    latest_date = latest_time.date()

    start_month, start_day = earliest_date.month, earliest_date.day
    end_month, end_day = latest_date.month, latest_date.day

    birthday_users = (User.objects.filter(
        Q(profile__birthday__month=start_month, profile__birthday__day=start_day) |
        Q(profile__birthday__month=end_month, profile__birthday__day=end_day),
        is_active=True
    ).values("username", "email"))

    return {'birthday_users':birthday_users}
