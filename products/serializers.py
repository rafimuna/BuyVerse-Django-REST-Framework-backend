from rest_framework import serializers
from .models import Product, ProductVariant, Color, Size


# 1. Color Serializer
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']


# 2. Size Serializer
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']


# 3. Product Variant Serializer
class ProductVariantSerializer(serializers.ModelSerializer):
    # Color এবং Size-এর বিস্তারিত অবজেক্ট (React Dropdown-এর জন্য)
    color_detail = ColorSerializer(source='color', read_only=True)
    size_detail = SizeSerializer(source='size', read_only=True)
    
    # Variant Image URL Generator
    image_url = serializers.SerializerMethodField()
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = ProductVariant
        fields = [
            'id',
            'sku',
            'price',
            'discount_price',
            'final_price',
            'stock',
            'color',
            'size',
            'color_detail',
            'size_detail',
            'image',
            'image_url',
            'is_active'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


# 4. Main Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    # প্রোডাক্টের সব ভ্যারিয়েন্ট একসাথে লোড করা
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    # Model @property থেকে আসা final_price
    final_price = serializers.ReadOnlyField()
    
    # Main Product Image URL Generator
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'description',
            'price',
            'discount_price',
            'final_price',
            'stock',
            'sku',
            'image',
            'image_url',       # 👈 React component এই key খুঁজবে
            'is_featured',
            'is_active',
            'variants',        # 👈 React component-এর variants array
            'created_at',
            'updated_at'
        ]

    def get_image_url(self, obj):
    if obj.image and hasattr(obj.image, 'url'):
        url = obj.image.url
        # যদি URL ইতোমধ্যে http:// বা https:// দিয়ে শুরু হয় (যেমন Cloudinary-র ক্ষেত্রে)
        if url.startswith('http://') or url.startswith('https://'):
            return url
        
        # যদি লোকাল/রিলেটিভ পাথ হয় (/media/...), তবে Absolute URI বানিয়ে নিবে
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(url)
        return url
        
    return None