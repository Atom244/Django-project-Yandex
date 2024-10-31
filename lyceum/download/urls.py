from django.urls import path

from download import views

__all__ = []

app_name = "download"

urlpatterns = [
    path("<path:file_path>/", views.download_image, name="download-image"),
]
