from django.urls import path

from .views import (
    CouponListCreateAPIView,
    CouponRetrieveUpdateDestroyAPIView,
)


urlpatterns = [

    # Coupon List + Create
    path(
        "",
        CouponListCreateAPIView.as_view(),
        name="coupon-list-create",
    ),

    # Coupon Retrieve + Update + Delete
    path(
        "<int:pk>/",
        CouponRetrieveUpdateDestroyAPIView.as_view(),
        name="coupon-detail",
    ),
]