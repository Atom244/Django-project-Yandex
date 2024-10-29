from pathlib import Path

from django.conf import settings
from django.http import Http404, HttpResponse

__all__ = []


def download_image(request, file_path):
    file_path = Path(settings.MEDIA_ROOT) / file_path

    if file_path.exists():
        with file_path.open("rb") as file:
            response = HttpResponse(
                file.read(),
                content_type="application/adminupload",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{file_path.name}"'
            )
            return response
    else:
        raise Http404("Файл не найден")
