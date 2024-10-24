from django.utils import timezone

__all__ = ["current_year"]


def current_year(request):
    return {
        "current_year": timezone.now().year,
    }
