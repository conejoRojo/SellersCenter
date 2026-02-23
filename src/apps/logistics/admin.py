from django.contrib import admin
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("order", "provider", "tracking_number", "status", "estimated_delivery", "delivered_at")
    list_filter = ("status", "provider")
    search_fields = ("order__external_id", "tracking_number")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Envío", {"fields": ("order", "provider", "status")}),
        ("Tracking", {"fields": ("tracking_number", "tracking_url", "estimated_delivery", "delivered_at")}),
        ("Historial de eventos", {"fields": ("events",), "classes": ("collapse",)}),
        ("Datos originales", {"fields": ("raw_data",), "classes": ("collapse",)}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
