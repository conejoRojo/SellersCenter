"""
Modelos base compartidos por todas las apps.
"""

import uuid
from django.db import models


class TimeStampedModel(models.Model):
    """
    Modelo abstracto que agrega created_at y updated_at a cualquier modelo.
    Heredar de este en lugar de models.Model directamente.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(TimeStampedModel):
    """
    Modelo con soft delete — nunca borra físicamente, solo marca deleted_at.
    """
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Incluye eliminados

    def delete(self, *args, **kwargs):
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    class Meta:
        abstract = True
