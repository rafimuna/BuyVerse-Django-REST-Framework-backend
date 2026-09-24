from django.urls import path

from .views import (
    CartRetrieveAPIView,
    CartItemListCreateAPIView,
    CartItemUpdateAPIView,
    CartItemDeleteAPIView,
)


urlpatterns = [

    path(
        "",
        CartRetrieveAPIView.as_view(),
        name="cart-detail"
    ),

    path(
        "items/",
        CartItemListCreateAPIView.as_view(),
        name="cart-item-create"
    ),

    path(
        "items/<int:pk>/",
        CartItemUpdateAPIView.as_view(),
        name="cart-item-update"
    ),

    path(
        "items/<int:pk>/delete/",
        CartItemDeleteAPIView.as_view(),
        name="cart-item-delete"
    ),

]