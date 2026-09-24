from django.utils import timezone
from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon

        fields = [
            "id",
            "code",
            "discount_type",
            "discount_value",
            "minimum_order_amount",
            "maximum_discount",
            "usage_limit",
            "used_count",
            "valid_from",
            "valid_until",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "used_count",
            "created_at",
        ]

    def validate_code(self, value):
        return value.strip().upper()

    def validate(self, attrs):
        discount_type = attrs.get(
            "discount_type",
            getattr(self.instance, "discount_type", None)
        )

        discount_value = attrs.get(
            "discount_value",
            getattr(self.instance, "discount_value", None)
        )

        valid_from = attrs.get(
            "valid_from",
            getattr(self.instance, "valid_from", None)
        )

        valid_until = attrs.get(
            "valid_until",
            getattr(self.instance, "valid_until", None)
        )

        maximum_discount = attrs.get(
            "maximum_discount",
            getattr(self.instance, "maximum_discount", None)
        )

        minimum_order_amount = attrs.get(
            "minimum_order_amount",
            getattr(self.instance, "minimum_order_amount", None)
        )

        usage_limit = attrs.get(
            "usage_limit",
            getattr(self.instance, "usage_limit", None)
        )

        # Discount value
        if discount_value is not None and discount_value <= 0:
            raise serializers.ValidationError({
                "discount_value": "Discount value must be greater than zero."
            })

        # Percentage validation
        if discount_type == "percentage":
            if discount_value > 100:
                raise serializers.ValidationError({
                    "discount_value": "Percentage discount cannot be greater than 100."
                })

        # Fixed amount validation
        if discount_type == "fixed":
            if discount_value <= 0:
                raise serializers.ValidationError({
                    "discount_value": "Fixed discount must be greater than zero."
                })

        # Minimum order amount
        if minimum_order_amount is not None and minimum_order_amount < 0:
            raise serializers.ValidationError({
                "minimum_order_amount": "Minimum order amount cannot be negative."
            })

        # Maximum discount
        if maximum_discount is not None and maximum_discount <= 0:
            raise serializers.ValidationError({
                "maximum_discount": "Maximum discount must be greater than zero."
            })

        # Usage limit
        if usage_limit is not None and usage_limit <= 0:
            raise serializers.ValidationError({
                "usage_limit": "Usage limit must be greater than zero."
            })

        # Date validation
        if valid_from and valid_until:
            if valid_until <= valid_from:
                raise serializers.ValidationError({
                    "valid_until": "Valid until must be later than valid from."
                })

        return attrs