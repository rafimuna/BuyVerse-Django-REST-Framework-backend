from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Product, ProductVariant, Color, Size
from .serializers import ProductSerializer, ProductVariantSerializer, ColorSerializer, SizeSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "description", "sku", "category__name"]
    ordering_fields = ["created_at", "price", "name"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related("category")

        if self.request.method == "GET":
            return queryset

        user = self.request.user
        if user.is_superuser or getattr(user, "role", "") == "admin":
            return Product.objects.all().select_related("category")

        return queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Product.objects.none()

        if getattr(user, 'is_superuser', False) or getattr(user, 'role', '') == "admin":
            return Product.objects.all()

        return Product.objects.filter(user=user)


class ProductVariantListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductVariantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product", "color", 'size', 'sku', 'price'  ]  # Note: Variant-এ সাধারণত 'product' ফিল্ড থাকে

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ProductVariant.objects.none()

        if getattr(user, 'is_superuser', False) or getattr(user, 'role', '') == "admin":
            return ProductVariant.objects.all()

        return ProductVariant.objects.filter(product__user=user)

    def perform_create(self, serializer):
        serializer.save()


class ProductVariantRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ProductVariant.objects.none()

        if getattr(user, 'is_superuser', False) or getattr(user, 'role', '') == "admin":
            return ProductVariant.objects.all()

        return ProductVariant.objects.filter(product__user=user)


class ColorListCreateView(generics.ListCreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class SizeListCreateView(generics.ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer