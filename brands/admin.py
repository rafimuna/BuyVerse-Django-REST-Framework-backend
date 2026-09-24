from django.contrib import admin
from .models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ("name", "slug", "is_active", "created_at")
	search_fields = ("name", "slug")
	list_filter = ("is_active",)
	prepopulated_fields = {"slug": ("name",)}
