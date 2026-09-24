from django.contrib import admin
from .models import Color, Product, ProductVariant, Size


class ProductVariantInline(admin.TabularInline):
	model = ProductVariant
	extra = 0
	fields = ("sku", "color", "size", "price", "discount_price", "stock", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "price", "stock", "is_featured", "is_active")
	search_fields = ("name", "slug", "sku", "description")
	list_filter = ("category", "is_featured", "is_active")
	prepopulated_fields = {"slug": ("name",)}
	autocomplete_fields = ("category", "user")
	inlines = (ProductVariantInline,)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
	search_fields = ("name", "hex_code")


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
	search_fields = ("name",)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
	list_display = ("product", "sku", "color", "size", "price", "stock", "is_active")
	search_fields = ("product__name", "sku")
	list_filter = ("is_active", "color", "size")