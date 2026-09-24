from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'slug',
        'image',
    )

    search_fields = (
        'name',
        'slug',
    )

    list_filter = (
        'name',
    )

    prepopulated_fields = {
        'slug': ('name',),
    }