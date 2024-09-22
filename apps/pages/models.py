from django.db import models


class Announcement(models.Model):
    class TYPES(models.TextChoices):
        INFO = "info"
        WARNING = "warning"

    content = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPES.choices, default=TYPES.INFO)
    deadline = models.DateTimeField(blank=True)
    is_external = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.content


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
