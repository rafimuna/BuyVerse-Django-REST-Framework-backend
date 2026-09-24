from django.contrib import admin
from .models import Address, ShippingMethod


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
	list_display = ("name", "cost", "estimated_days", "is_active")
	search_fields = ("name", "description")
	list_filter = ("is_active",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_display = ("full_name", "user", "city", "country", "is_default")
	search_fields = ("full_name", "user__email", "phone", "city")
	list_filter = ("country", "is_default")
