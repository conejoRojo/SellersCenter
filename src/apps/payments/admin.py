from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "provider", "status", "amount", "currency", "paid_at", "created_at")
    list_filter = ("status", "provider", "currency")
    search_fields = ("order__external_id", "external_id")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Pago", {"fields": ("order", "provider", "external_id", "status")}),
        ("Monto", {"fields": ("amount", "currency", "paid_at")}),
        ("Datos originales", {"fields": ("raw_data",), "classes": ("collapse",)}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
