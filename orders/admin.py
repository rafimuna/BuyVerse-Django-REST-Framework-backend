from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ("product_name", "price", "quantity", "subtotal")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "status", "payment_status", "total", "created_at")
	search_fields = ("=id", "shipping_name", "shipping_phone", "user__email")
	list_filter = ("status", "payment_status", "created_at")
	readonly_fields = ("subtotal", "shipping_cost", "discount", "total", "created_at", "updated_at")
	inlines = (OrderItemInline,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ("order", "product_name", "quantity", "price", "subtotal")
	search_fields = ("=order__id", "product_name")
