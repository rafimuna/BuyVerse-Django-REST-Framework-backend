from django.urls import path

from .views import (
    ShippingMethodListCreateAPIView,
    ShippingMethodRetrieveUpdateDestroyAPIView,
    AddressListCreateAPIView,
    AddressRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    # Shipping Methods
    path(
        "",
        ShippingMethodListCreateAPIView.as_view(),
        name="shipping-method-list-create",
    ),

    path(
        "<int:pk>/",
        ShippingMethodRetrieveUpdateDestroyAPIView.as_view(),
        name="shipping-method-detail",
    ),

    # Addresses
    path(
        "addresses/",
        AddressListCreateAPIView.as_view(),
        name="address-list-create",
    ),

    path(
        "addresses/<int:pk>/",
        AddressRetrieveUpdateDestroyAPIView.as_view(),
        name="address-detail",
    ),
]