from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("sku", "name", "quantity", "unit_price", "total_price")
    readonly_fields = ("total_price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("external_id", "channel", "seller", "buyer_name", "status", "total", "currency", "created_at")
    list_filter = ("status", "channel", "seller", "currency")
    search_fields = ("external_id", "buyer_name", "buyer_email")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]

    fieldsets = (
        ("Identificación", {"fields": ("channel", "seller", "external_id", "status")}),
        ("Comprador", {"fields": ("buyer_name", "buyer_email", "buyer_phone", "shipping_address")}),
        ("Totales", {"fields": ("currency", "subtotal", "shipping_cost", "total")}),
        ("Datos originales", {"fields": ("raw_data",), "classes": ("collapse",)}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("channel", "seller")
