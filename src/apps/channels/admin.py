from django.contrib import admin
from .models import Channel, SellerChannelCredential


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "channel_type", "is_active")
    list_filter = ("channel_type", "is_active")
    search_fields = ("name", "slug")
    ordering = ("name",)

    fieldsets = (
        ("Identificación", {"fields": ("slug", "name", "channel_type", "is_active", "logo_url")}),
        ("Configuración", {"fields": ("config",), "classes": ("collapse",)}),
    )


@admin.register(SellerChannelCredential)
class SellerChannelCredentialAdmin(admin.ModelAdmin):
    list_display = ("seller", "channel", "is_valid", "expires_at", "updated_at")
    list_filter = ("channel", "is_valid")
    search_fields = ("seller__business_name", "channel__name")
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        # No mostrar credentials en la lista para mayor seguridad
        return super().get_queryset(request).select_related("seller", "channel")
