from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name


class Town(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="towns")
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name


class Division(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class CostCentre(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        return f"{self.number}"


class Position(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="positions"
    )
    line_manager = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="subordinates",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255, unique=True)
    is_manager = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("department", "is_manager"),
                condition=models.Q(is_manager=True),
                name="unique_manager_per_department",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.department}"

    def clean(self) -> None:
        return super().clean()


class Location(models.Model):
    title = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    town = models.ForeignKey(
        Town, on_delete=models.CASCADE, related_name="locations", default=None
    )

    def __str__(self) -> str:
        return self.title
