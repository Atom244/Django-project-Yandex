from django.urls import path

from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("coffee/", views.CoffeeView.as_view(), name="coffee"),
    path("echo/", views.EchoView.as_view(), name="echo"),
    path("echo/submit/", views.EchoSubmitView.as_view(), name="echo-submit"),
]
