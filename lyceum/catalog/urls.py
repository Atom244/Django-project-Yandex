from django.urls import path

from catalog import views

app_name = "catalog"


urlpatterns = [
    path("", views.item_list, name="item-list"),
    path("<int:pk>/", views.item_detail, name="item-detail"),
    path("new/", views.catalog_new, name="new"),
    path("friday/", views.catalog_changed_on_friday, name="friday"),
    path("unverified/", views.catalog_unverified, name="unverified"),
]
