from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "get_full_name", "role", "is_active", "is_staff", "date_joined")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)
    readonly_fields = ("date_joined", "last_login")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("SellersCenter", {"fields": ("role", "phone", "avatar_url")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("SellersCenter", {"fields": ("role", "email", "first_name", "last_name")}),
    )
