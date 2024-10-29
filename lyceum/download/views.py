import os

from django.conf import settings
from django.http import Http404, HttpResponse


def download_image(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            response = HttpResponse(
                file.read(),
                content_type="application/adminupload",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(file_path)}"'
            )
            return response
    else:
        raise Http404("Файл не найден")
