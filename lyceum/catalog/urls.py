from django.urls import path, re_path, register_converter

from . import converters
from . import views


register_converter(converters.PositiveNumConverter, "pos_num")


urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
    re_path(r"re/(?P<num>\d+)/", views.item_num),
    path("converter/<pos_num:number>/", views.item_converter_num),
]
