from django.urls import path

from .views import WishlistAPIView, WishlistItemDeleteAPIView


urlpatterns = [
    path("", WishlistAPIView.as_view(), name="wishlist"),
    path("items/<int:pk>/", WishlistItemDeleteAPIView.as_view(), name="wishlist-item-delete"),
]