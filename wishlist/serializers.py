from rest_framework import serializers

from products.serializers import ProductSerializer

from .models import Wishlist, WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = WishlistItem
        fields = ["id", "product", "product_detail", "created_at"]
        read_only_fields = ["id", "product_detail", "created_at"]


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)
    item_count = serializers.IntegerField(source="items.count", read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "created_at", "item_count", "items"]
        read_only_fields = fields


class WishlistItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = ["product"]

    def validate_product(self, product):
        if not product.is_active:
            raise serializers.ValidationError("This product is not available.")
        return product