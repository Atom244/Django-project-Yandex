from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import set_language

urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("set-language/", set_language, name="set_language"),
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
