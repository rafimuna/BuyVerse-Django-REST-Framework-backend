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
    color_detail = ColorSerializer(source='color', read_only=True)
    size_detail = SizeSerializer(source='size', read_only=True)
    
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
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
            if url.startswith('http://') or url.startswith('https://'):
                return url
            
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None


# 4. Main Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
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
            'image_url',
            'is_featured',
            'is_active',
            'variants',
            'created_at',
            'updated_at'
        ]

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            url = obj.image.url
            # Cloudinary URL হলে সরাসরি রিটার্ন করবে
            if url.startswith('http://') or url.startswith('https://'):
                return url
            
            # Local/Relative Media Path হলে Full URL বানাবে
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None