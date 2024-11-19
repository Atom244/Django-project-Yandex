from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth
import django.contrib.auth.urls
from django.urls import include, path
from django.views.i18n import set_language

import users.urls

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("catalog/", include("catalog.urls")),
    path("download/", include("download.urls")),
    path("feedback/", include("feedback.urls")),
    path("statistics/", include("Statistics.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include(users.urls)),
    path("auth/", include(django.contrib.auth.urls)),
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
