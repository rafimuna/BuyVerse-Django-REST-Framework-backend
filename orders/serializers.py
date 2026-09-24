from decimal import Decimal
from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem
from products.models import Product


# =========================================================
# ORDER ITEM SERIALIZER
# =========================================================
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "price",
            "quantity",
            "subtotal",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "price",
            "subtotal",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


# =========================================================
# ORDER SERIALIZER
# =========================================================
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shipping_method",
            "coupon",
            "status",
            "payment_status",
            "subtotal",
            "shipping_cost",
            "discount",
            "total",
            "shipping_name",
            "shipping_phone",
            "shipping_address",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "status",
            "payment_status",
            "subtotal",
            "shipping_cost",
            "discount",
            "total",
            "created_at",
            "updated_at",
        ]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must contain at least one product.")

        product_ids = [item["product"].id for item in items]

        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Duplicate products are not allowed.")

        return items

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        request_user = validated_data.pop("user", self.context["request"].user)
        user = request_user if request_user and request_user.is_authenticated else None

        # Shipping Cost
        shipping_method = validated_data.get("shipping_method")
        shipping_cost = Decimal("0.00")
        if shipping_method:
            shipping_cost = shipping_method.cost

        # Coupon Discount
        coupon = validated_data.get("coupon")
        discount = Decimal("0.00")

        # Subtotal Calculation
        subtotal = Decimal("0.00")
        prepared_items = []

        for item_data in items_data:
            product_id = item_data["product"].id
            quantity = item_data["quantity"]

            # Lock Product Row for Concurrency Control
            product = Product.objects.select_for_update().get(id=product_id)

            if not product.is_active:
                raise serializers.ValidationError({
                    "items": f"{product.name} is not available."
                })

            if product.stock < quantity:
                raise serializers.ValidationError({
                    "items": f"{product.name} has only {product.stock} items in stock."
                })

            price = product.final_price
            item_subtotal = price * quantity
            subtotal += item_subtotal

            prepared_items.append({
                "product": product,
                "product_name": product.name,
                "price": price,
                "quantity": quantity,
                "subtotal": item_subtotal,
            })

        total = subtotal + shipping_cost - discount

        # Order Creation
        order = Order.objects.create(
            user=user,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            discount=discount,
            total=total,
            **validated_data
        )

        # Order Items & Stock Update
        for item in prepared_items:
            product = item["product"]
            quantity = item["quantity"]

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=item["product_name"],
                price=item["price"],
                quantity=quantity,
                subtotal=item["subtotal"],
            )

            # Reduce Stock
            product.stock -= quantity
            product.save(update_fields=["stock"])

        return order