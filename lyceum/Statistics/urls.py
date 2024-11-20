from django.urls import path
from Statistics.views import (
    ItemStatisticsView,
    UserRatedItemsView,
    UserStatisticsView,
)

app_name = "statistics"

urlpatterns = [
    path("user/", UserStatisticsView.as_view(), name="user_statistics"),
    path("items/", ItemStatisticsView.as_view(), name="item_statistics"),
    path(
        "user-rated-items/",
        UserRatedItemsView.as_view(),
        name="user_rated_items",
    ),
]
