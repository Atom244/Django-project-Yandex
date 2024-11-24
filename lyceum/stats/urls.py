from django.urls import path
from stats.views import (
    ItemStatisticsView,
    UserRatedItemsView,
    UserStatisticsView,
)

app_name = "statistics"

urlpatterns = [
    path("items/", ItemStatisticsView.as_view(), name="item_statistics"),
    path("user/", UserStatisticsView.as_view(), name="user_statistics"),
    path(
        "user-rated-items/",
        UserRatedItemsView.as_view(),
        name="user_rated_items",
    ),
]
