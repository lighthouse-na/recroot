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


class Division(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class CostCentre(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.number


class Position(models.Model):
    line_manager = models.ForeignKey(
        "self", on_delete=models.PROTECT, related_name="subordinates"
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
