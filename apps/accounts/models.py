from django.contrib.auth.models import User
from django.db import models

from apps.organisation.models import CostCentre, Position


class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="profile"
    )
    salary_reference_number = models.PositiveIntegerField(blank=True,null=True)
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, related_name="profiles",blank=True,null=True
    )
    cost_centre = models.ForeignKey(
        CostCentre, on_delete=models.PROTECT, related_name="profiles",blank=True,null=True
    )
    gender = models.CharField(
        max_length=6, choices=[("male", "Male"), ("female", "Female")],blank=True,null=True
    )
    date_appointed = models.DateField(blank=True,null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
