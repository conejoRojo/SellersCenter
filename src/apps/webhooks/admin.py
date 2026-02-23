from django.contrib import admin
from .models import WebhookEvent


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "channel", "status", "retries", "processed_at", "created_at")
    list_filter = ("status", "event_type", "channel")
    search_fields = ("channel__name",)
    readonly_fields = ("created_at", "updated_at", "processed_at", "payload", "headers")
    ordering = ("-created_at",)

    fieldsets = (
        ("Evento", {"fields": ("channel", "event_type", "status", "retries")}),
        ("Payload", {"fields": ("payload", "headers"), "classes": ("collapse",)}),
        ("Resultado", {"fields": ("error_message", "processed_at")}),
        ("Auditoría", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    actions = ["requeue_events"]

    @admin.action(description="Reencolar eventos seleccionados")
    def requeue_events(self, request, queryset):
        count = queryset.filter(status=WebhookEvent.Status.FAILED).update(
            status=WebhookEvent.Status.QUEUED, retries=0
        )
        self.message_user(request, f"{count} evento(s) reencolado(s).")
