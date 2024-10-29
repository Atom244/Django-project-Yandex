from django.urls import path, re_path, register_converter

from catalog import converters, views

app_name = "catalog"

register_converter(converters.PositiveNumConverter, "posnum")


urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    re_path(r"re/(?P<num>0*[1-9][0-9]*)/", views.item_num, name="re"),
    path("converter/<posnum:num>/", views.item_num, name="converter"),
    path("new/", views.catalog_new, name="new"),
    path("friday/", views.catalog_changed_on_friday, name="friday"),
    path("unverified/", views.catalog_unverified, name="unverified"),
]
