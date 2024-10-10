from django.urls import path, re_path, register_converter

from . import converters
from . import views


register_converter(converters.PositiveNumConverter, "posnum")


urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
    re_path(r"re/(?P<num>0*[1-9][0-9]*)/", views.item_num),
    path("converter/<posnum:num>/", views.item_num),
]
