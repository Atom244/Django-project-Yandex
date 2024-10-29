from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404

__all__ = []


def download_image(request, file_path):
    file_path = Path(settings.MEDIA_ROOT) / file_path

    if file_path.exists() and file_path.is_file():
        response = FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            content_type="application/adminupload",
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{file_path.name}"'
        )
        return response

    raise Http404("Файл не найден")
