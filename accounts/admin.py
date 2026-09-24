from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class AccountUserAdmin(UserAdmin):
	list_display = ("email", "username", "role", "is_staff", "is_active")
	search_fields = ("email", "username", "first_name", "last_name")
	list_filter = ("role", "is_staff", "is_active")
	ordering = ("email",)
	fieldsets = UserAdmin.fieldsets + (("Store access", {"fields": ("role",)}),)
	add_fieldsets = UserAdmin.add_fieldsets + (("Store access", {"fields": ("role",)}),)
