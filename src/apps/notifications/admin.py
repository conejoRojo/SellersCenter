from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipient", "channel", "status", "sent_at", "read_at", "created_at")
    list_filter = ("status", "channel")
    search_fields = ("subject", "recipient__username", "recipient__email")
    readonly_fields = ("created_at", "updated_at", "sent_at", "read_at")
    ordering = ("-created_at",)

    fieldsets = (
        ("Notificación", {"fields": ("recipient", "channel", "subject", "body")}),
        ("Estado", {"fields": ("status", "sent_at", "read_at")}),
        ("Metadata", {"fields": ("metadata",), "classes": ("collapse",)}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
