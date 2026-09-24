from django.urls import path
from .views import HomePageDataView, BannerListAPIView

urlpatterns = [
    # Explicitly use .as_view() for class-based APIViews
    path('home/', HomePageDataView.as_view(), name='home-page'),
    path('banners/', BannerListAPIView.as_view(), name='banner-list'),
]