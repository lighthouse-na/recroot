import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.template.loader import get_template


class AdminNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = "admin-notifications"
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)


class RecruiterNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = "recruiter-notifications"
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)


class FinaidNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.GROUP_NAME = "finaid-notifications"
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)


class StaffNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        # if not self.user.is_authenticated
        self.GROUP_NAME = f"staff-notifications-{self.scope['user'].id}"
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)

    def created(self, event):
        # self.send(text_data=event["vacancy_id", "vacancy_slug", "vacancy_title"])
        context = {
            "id": event["id"],
            "user": event["user"],
            "object_id": event["object_id"],
            "message": event["message"],
            "is_read": event["read"],
            "created_at": event["created_at"],
        }
        html = get_template("unfold/partials/notification.html").render(context)
        self.send(text_data=html)
