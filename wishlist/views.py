from django.db import IntegrityError, transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Wishlist, WishlistItem
from .serializers import (
    WishlistItemCreateSerializer,
    WishlistItemSerializer,
    WishlistSerializer,
)


class WishlistAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WishlistItemCreateSerializer
        return WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).prefetch_related(
            "items__product__variants",
            "items__product__category",
        )

    def list(self, request, *args, **kwargs):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(
            wishlist,
            context=self.get_serializer_context(),
        )
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            item = WishlistItem.objects.create(
                wishlist=wishlist,
                product=serializer.validated_data["product"],
            )
        except IntegrityError:
            item = WishlistItem.objects.get(
                wishlist=wishlist,
                product=serializer.validated_data["product"],
            )

        return Response(
            WishlistItemSerializer(item, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )


class WishlistItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(
            wishlist__user=self.request.user
        ).select_related("product", "wishlist")
