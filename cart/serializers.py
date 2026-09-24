from rest_framework import serializers

from .models import Cart, CartItem
from products.models import Product


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "discount_price",
            "final_price",
            "image",
            "stock",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        source="product",
        queryset=Product.objects.filter(is_active=True),
        write_only=True
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_id",
            "quantity",
            "subtotal",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "product",
            "subtotal",
            "created_at",
        ]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Quantity must be at least 1."
            )

        return value

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")

        if product and quantity > product.stock:
            raise serializers.ValidationError({
                "quantity": f"Only {product.stock} items are available."
            })

        return attrs

    def get_subtotal(self, obj):
        price = (
            obj.product.discount_price
            if obj.product.discount_price
            and obj.product.discount_price < obj.product.price
            else obj.product.price
        )

        return price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_total(self, obj):
        total = 0

        for item in obj.items.all():

            price = (
                item.product.discount_price
                if item.product.discount_price
                and item.product.discount_price < item.product.price
                else item.product.price
            )

            total += price * item.quantity

        return total