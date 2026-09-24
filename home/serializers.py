from rest_framework import serializers
from .models import Banner
from products.serializers import ProductSerializer

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'subtitle', 'image', 'link']