from django.contrib.auth.models import User
from django.db import models

from apps.organisation.models import CostCentre, Department, Position


class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="profile"
    )
    id_number = models.PositiveIntegerField()
    salary_reference_number = models.PositiveIntegerField()
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="profiles"
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="profiles"
    )
    cost_centre = models.ForeignKey(
        CostCentre, on_delete=models.PROTECT, related_name="profiles"
    )
    gender = models.CharField(
        max_length=6, choices=[("male", "Male"), ("female", "Female")]
    )
    date_appointed = models.DateField()

    def __str__(self):
        return self.user
