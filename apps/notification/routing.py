from django.urls import path

from .consumers import (
    AdminNotificationConsumer,
    FinaidNotificationConsumer,
    RecruiterNotificationConsumer,
    StaffNotificationConsumer,
)

websocket_urlpatterns = [
    path(
        "ws/notifications/admin/",
        AdminNotificationConsumer.as_asgi(),
    ),
    path(
        "ws/notifications/finaid/",
        FinaidNotificationConsumer.as_asgi(),
    ),
    path(
        "ws/notifications/recruiter/",
        RecruiterNotificationConsumer.as_asgi(),
    ),
    path(
        "ws/notifications/staff/",
        StaffNotificationConsumer.as_asgi(),
    ),
]
