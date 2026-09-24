from django.urls import path
from . import views
from .views import (
    ColorListCreateView, 
    SizeListCreateView, 
    ProductVariantListCreateAPIView
)

urlpatterns = [
    # Products URLs
    path('', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),

    # Product Variants URLs
    path('variants/', views.ProductVariantListCreateAPIView.as_view(), name='variant-list-create'),
    path('variants/<int:pk>/', views.ProductVariantRetrieveUpdateDestroyAPIView.as_view(), name='variant-detail'),

    path('colors/', ColorListCreateView.as_view(), name='color-list-create'),
    path('sizes/', SizeListCreateView.as_view(), name='size-list-create'),
]