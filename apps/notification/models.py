from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from .types import NOTIFICATION_TYPES


class StaffNotification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="staff_notifications"
    )
    notification_type = models.CharField(max_length=255, choices=NOTIFICATION_TYPES.choices)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey("content_type", "object_id")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["content_type", "object_id"]),
        ]
