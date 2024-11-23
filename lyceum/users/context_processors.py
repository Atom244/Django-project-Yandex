from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import CharField, Value
from django.db.models.functions import Concat, ExtractDay, ExtractMonth
from django.utils.timezone import now

__all__ = []


def birthday_context(request):

    current_time = now()
    start_date = (current_time - timedelta(hours=12)).date().strftime("%m-%d")
    end_date = (current_time + timedelta(hours=14)).date().strftime("%m-%d")

    birthday_users = (
        User.objects.annotate(
            birthday_md=Concat(
                ExtractMonth("profile__birthday", output_field=CharField()),
                Value("-"),
                ExtractDay("profile__birthday", output_field=CharField()),
            ),
        )
        .filter(
            is_active=True,
            birthday_md__gte=start_date,
            birthday_md__lte=end_date,
        )
        .values("username", "email", "first_name")
    )

    return {"birthday_users": birthday_users}
