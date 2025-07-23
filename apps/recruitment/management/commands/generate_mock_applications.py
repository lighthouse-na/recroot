import random
from datetime import timedelta, datetime

from django.core.management.base import BaseCommand
from django.utils import timezone
import pytz

from apps.recruitment.models import Application, Vacancy


class Command(BaseCommand):
    help = "Generates mock application data for specified years."

    def add_arguments(self, parser):
        parser.add_argument(
            "--years",
            nargs='+',
            type=int,
            help="Years for which to generate mock applications (e.g., 2023 2024 2025)",
            default=[2023, 2024, 2025],
        )
        parser.add_argument(
            "--count_per_year",
            type=int,
            help="Number of applications to generate per year (default: 5)",
            default=5,
        )

    def handle(self, *args, **options):
        years = options["years"]
        count_per_year = options["count_per_year"]

        vacancies = list(Vacancy.objects.all())
        if not vacancies:
            self.stdout.write(self.style.ERROR("No vacancies found. Please create some vacancies first."))
            return

        for year in years:
            self.stdout.write(self.style.SUCCESS(f"Generating {count_per_year} applications for {year}..."))
            for i in range(count_per_year):
                random_vacancy = random.choice(vacancies)
                # Generate a random date within the year
                start_of_year = datetime(year, 1, 1, tzinfo=pytz.utc)
                end_of_year = datetime(year, 12, 31, tzinfo=pytz.utc)
                random_date = start_of_year + timedelta(
                    days=random.randint(0, (end_of_year - start_of_year).days)
                )

                Application.objects.create(
                    vacancy=random_vacancy,
                    first_name=f"Mock{year}FN{i}",
                    last_name=f"Mock{year}LN{i}",
                    email=f"mock{year}{i}{random.randint(1000, 9999)}@example.com",
                    primary_contact=f"2648112345{year}{i}{random.randint(100, 999)}",
                    date_of_birth=datetime(year - random.randint(18, 40), random.randint(1, 12), random.randint(1, 28)).date(),
                    gender=random.choice(["male", "female"]),
                    cv="mock_cv.pdf", # Placeholder for CV file
                    is_internal=random.choice([True, False]),
                    status=random.choice(["pending", "reviewed", "accepted", "rejected"]),
                    submitted_at=random_date,
                )
            self.stdout.write(self.style.SUCCESS(f"Successfully generated applications for {year}."))

        self.stdout.write(self.style.SUCCESS("Mock application data generation complete."))
