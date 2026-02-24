from django.contrib import admin
from .models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("business_name", "tax_id", "user", "status", "commission_rate", "created_at")
    list_filter = ("status",)
    search_fields = ("business_name", "tax_id", "user__email", "user__username")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("business_name",)

    fieldsets = (
        ("Datos del seller", {"fields": ("user", "business_name", "tax_id")}),
        ("Configuración", {"fields": ("status", "commission_rate", "settings")}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
