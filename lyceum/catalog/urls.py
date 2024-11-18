from django.urls import path

from catalog import views

app_name = "catalog"


urlpatterns = [
    path("", views.ItemListView.as_view(), name="item-list"),
    path("<int:pk>/", views.ItemDetailView.as_view(), name="item-detail"),
    path("new/", views.CatalogNewView.as_view(), name="new"),
    path("friday/", views.CatalogChangedOnFridayView.as_view(), name="friday"),
    path(
        "unverified/",
        views.CatalogUnverifiedView.as_view(),
        name="unverified",
    ),
]
