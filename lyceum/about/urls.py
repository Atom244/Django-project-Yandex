from django.urls import path

from about import views


urlpatterns = [path("", views.description, name="about")]
