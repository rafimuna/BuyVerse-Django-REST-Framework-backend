import uuid
from rest_framework import serializers
from .models import Product, ProductVariant, Color, Size


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    # GET রিকোয়েস্টের সময় কালার ও সাইজের পুরো ডিটেইলস (নামসহ) দেখানোর জন্য
    color_detail = ColorSerializer(source='color', read_only=True)
    size_detail = SizeSerializer(source='size', read_only=True)
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'product',
            'color',
            'size',
            'color_detail',
            'size_detail',
            'price',
            'discount_price',
            'final_price',
            'sku',
        ]
        # POST/PUT করার সময় 'color' এবং 'size' ID হিসেবে পাঠাতে পারবেন
        extra_kwargs = {
            'color': {'write_only': True, 'required': False},
            'size': {'write_only': True, 'required': False},
            'sku': {'required': False},
        }

    def create(self, validated_data):
        # যদি রিকোয়েস্টে SKU না থাকে, তবে অটোমেটিক ইউনিক SKU তৈরি করবে
        if not validated_data.get('sku'):
            product_id = validated_data.get('product').id
            color_id = validated_data.get('color').id if validated_data.get('color') else '0'
            size_id = validated_data.get('size').id if validated_data.get('size') else '0'
            
            # উদাহরণ: PROD-1-C2-S3-A1B2
            unique_suffix = uuid.uuid4().hex[:4].upper()
            validated_data['sku'] = f"SKU-{product_id}-C{color_id}-S{size_id}-{unique_suffix}"

        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    # প্রোডাক্টের সাথে সম্পর্কিত সব ভ্যারিয়েন্ট লোড করার জন্য
    # (আপনার Product মডেলে ProductVariant-এর related_name='variants' থাকতে হবে)
    variants = ProductVariantSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'