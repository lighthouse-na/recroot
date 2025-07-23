import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.organisation.models import Department, Division, Location, Position, Region, Town
from apps.recruitment.models import Vacancy, VacancyType

class Command(BaseCommand):
    help = "Generates specific mock vacancy data (Internship and Graduate)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Generating specific mock vacancies..."))

        # Ensure VacancyType objects exist or create them
        internship_type, _ = VacancyType.objects.get_or_create(
            type="Internship"
        )
        graduate_type, _ = VacancyType.objects.get_or_create(
            type="Graduate"
        )

        # Ensure Location and Position exist or create some defaults
        # Ensure Location, Town, and Region exist or create some defaults
        region, _ = Region.objects.get_or_create(name="Default Region")
        town, _ = Town.objects.get_or_create(name="Default Town", region=region)
        location, _ = Location.objects.get_or_create(
            title="Head Office", defaults={"address": "123 Main St", "town": town}
        )
        # Ensure Division and Department exist or create some defaults
        division, _ = Division.objects.get_or_create(name="Default Division")
        department, _ = Department.objects.get_or_create(name="Default Department", division=division)

        position_intern, _ = Position.objects.get_or_create(
            name="Intern", department=department
        )
        position_grad, _ = Position.objects.get_or_create(
            name="Graduate Trainee", department=department
        )

        # Create Internship Vacancy
        internship_vacancy = Vacancy.objects.create(
            title="Software Development Internship",
            content="Join our team as a Software Development Intern and gain hands-on experience.",
            deadline=timezone.now() + timedelta(days=90),
            is_public=True,
            is_published=True,
            vacancy_type=internship_type,
        )
        internship_vacancy.town.add(town)
        self.stdout.write(self.style.SUCCESS("Created 'Software Development Internship' vacancy."))

        # Create Graduate Vacancy
        graduate_vacancy = Vacancy.objects.create(
            title="Graduate Software Engineer Program",
            content="Kickstart your career with our comprehensive Graduate Software Engineer Program.",
            deadline=timezone.now() + timedelta(days=120),
            is_public=True,
            is_published=True,
            vacancy_type=graduate_type,
        )
        graduate_vacancy.town.add(town)
        self.stdout.write(self.style.SUCCESS("Created 'Graduate Software Engineer Program' vacancy."))

        self.stdout.write(self.style.SUCCESS("Specific mock vacancy data generation complete."))
