from django.contrib import admin

from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
	list_display = ("title", "order", "is_active")
	search_fields = ("title", "subtitle")
	list_filter = ("is_active",)
	ordering = ("order",)
