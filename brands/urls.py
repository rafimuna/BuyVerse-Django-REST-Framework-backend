from django.urls import path

from .views import BrandDetailAPIView, BrandListCreateAPIView


urlpatterns = [
    path("", BrandListCreateAPIView.as_view(), name="brand-list-create"),
    path("<int:pk>/", BrandDetailAPIView.as_view(), name="brand-detail"),
]
