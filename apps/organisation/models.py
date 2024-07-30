from django.conf import settings
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Town(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="towns")
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
