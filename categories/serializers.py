from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']

    def create(self, validated_data):
        category = Category(**validated_data)

        if not category.slug:
            from django.utils.text import slugify
            category.slug = slugify(category.name)

        category.save()
        return category