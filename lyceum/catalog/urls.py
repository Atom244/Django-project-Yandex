from django.urls import path

from . import views


urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
]
