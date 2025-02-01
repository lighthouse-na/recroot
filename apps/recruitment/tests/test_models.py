import os
import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from apps.organisation.models import Region, Town
from apps.recruitment.models import Vacancy, VacancyType


class VacancyTypeTestCase(TestCase):
    def test_vacancy_type_creation(self):
        # Test creating a new VacancyType instance
        vacancy_type = VacancyType.objects.create(type=VacancyType.VACANCY_TYPE.INTERNSHIP)
        self.assertEqual(vacancy_type.type, VacancyType.VACANCY_TYPE.INTERNSHIP)

    def test_vacancy_type_choices(self):
        # Test that the choices are correctly defined
        choices = VacancyType.VACANCY_TYPE.choices
        self.assertEqual(len(choices), 6)
        self.assertEqual(choices[0][0], VacancyType.VACANCY_TYPE.INTERNSHIP)
        self.assertEqual(choices[1][0], VacancyType.VACANCY_TYPE.PERMANENT)
        self.assertEqual(choices[2][0], VacancyType.VACANCY_TYPE.PART_TIME)
        self.assertEqual(choices[3][0], VacancyType.VACANCY_TYPE.CONTRACT)
        self.assertEqual(choices[4][0], VacancyType.VACANCY_TYPE.GRADUATE)
        self.assertEqual(choices[5][0], VacancyType.VACANCY_TYPE.VOLUNTEER)

    def test_vacancy_type_str(self):
        # Test the __str__ method
        vacancy_type = VacancyType.objects.create(type=VacancyType.VACANCY_TYPE.INTERNSHIP)
        self.assertEqual(str(vacancy_type), VacancyType.VACANCY_TYPE.INTERNSHIP.upper())

    def test_vacancy_type_unique(self):
        # Test that the type field is unique
        VacancyType.objects.create(type=VacancyType.VACANCY_TYPE.INTERNSHIP)
        with self.assertRaises(IntegrityError):
            VacancyType.objects.create(type=VacancyType.VACANCY_TYPE.INTERNSHIP)

    def test_vacancy_type_max_length(self):
        # Test that the type field has a max length of 50
        long_type = "a" * 51
        vacancy_type = VacancyType(type=long_type)
        with self.assertRaises(ValidationError):
            vacancy_type.full_clean()


class VacancyModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username", email="testuser@email.com", password="password"
        )
        self.vacancy_type = VacancyType.objects.create(type=VacancyType.VACANCY_TYPE.INTERNSHIP)
        self.region = Region.objects.create(name="Test Region")
        self.town = Town.objects.create(region=self.region, name="Test Town")

    def test_vacancy_creation(self):
        vacancy = Vacancy.objects.create(
            title="Test Vacancy",
            vacancy_type=self.vacancy_type,
            pay_grade="PG1",
            content="<p>This is a test vacancy</p>",
            deadline="2023-03-01 12:00:00",
            is_public=True,
        )
        vacancy.town.set([self.town])
        self.assertEqual(vacancy.title, "Test Vacancy")
        self.assertEqual(vacancy.vacancy_type, self.vacancy_type)
        self.assertEqual(vacancy.pay_grade, "PG1")
        self.assertEqual(vacancy.content, "<p>This is a test vacancy</p>")
        self.assertEqual(vacancy.town.first(), self.town)
        self.assertEqual(vacancy.deadline, "2023-03-01 12:00:00")
        self.assertTrue(vacancy.is_public)

    def test_vacancy_advert_upload(self):
        file_path = os.path.join(os.path.dirname(__file__), "test.pdf")

        with open(file_path, "rb") as f:
            file = SimpleUploadedFile("test.pdf", f.read(), content_type="application/pdf")
            vacancy = Vacancy.objects.create(
                title="Test Vacancy",
                advert=file,
                vacancy_type=self.vacancy_type,
                pay_grade="PG1",
                content="<p>This is a test vacancy</p>",
                deadline="2023-03-01 12:00:00",
                is_public=True,
            )
            vacancy.town.set([self.town])
            self.assertTrue(vacancy.advert.name.startswith("adverts/"))
            self.assertTrue(vacancy.advert.name.endswith(".pdf"))
            self.assertEqual(vacancy.advert.size, os.path.getsize(file_path))

    # def test_vacancy_advert_validation(self):
    #     # Test invalid file extension
    #     file_path = os.path.join(os.path.dirname(__file__), "test.txt")

    #     with open(file_path, "rb") as f:
    #         file = SimpleUploadedFile("test.txt", f.read(), content_type="text/plain")

    #         with self.assertRaises(ValidationError):
    #             vacancy = Vacancy.objects.create(
    #                 title="Test Vacancy",
    #                 advert=file,
    #                 vacancy_type=self.vacancy_type,
    #                 pay_grade="PG1",
    #                 content="<p>This is a test vacancy</p>",
    #                 deadline="2023-03-01 12:00:00",
    #                 is_public=True,
    #             )
    #             vacancy.town.set([self.town])

    #     # Test file size limit
    #     file_path = os.path.join(os.path.dirname(__file__), "large_file.pdf")

    #     with open(file_path, "rb") as f:
    #         file = SimpleUploadedFile(
    #             "large_file.pdf", f.read(), content_type="application/pdf"
    #         )

    #         with self.assertRaises(ValidationError):
    #             Vacancy.objects.create(
    #                 title="Test Vacancy",
    #                 advert=file,
    #                 vacancy_type=self.vacancy_type,
    #                 pay_grade="PG1",
    #                 content="<p>This is a test vacancy</p>",
    #                 town=self.town,
    #                 deadline="2023-03-01 12:00:00",
    #                 is_public=True,
    #             )

    def test_vacancy_slug_creation(self):
        vacancy = Vacancy.objects.create(
            title="Test Vacancy",
            vacancy_type=self.vacancy_type,
            pay_grade="PG1",
            content="<p>This is a test vacancy</p>",
            deadline="2023-03-01 12:00:00",
            is_public=True,
        )
        vacancy.town.set([self.town])
        self.assertEqual(vacancy.slug, "test-vacancy-{}".format(vacancy.id))

    def test_vacancy_absolute_url(self):
        vacancy = Vacancy.objects.create(
            title="Test Vacancy",
            vacancy_type=self.vacancy_type,
            pay_grade="PG1",
            content="<p>This is a test vacancy</p>",
            deadline="2023-03-01 12:00:00",
            is_public=True,
        )
        vacancy.town.set([self.town])
        self.assertEqual(
            vacancy.get_absolute_url(),
            reverse("recruitment:vacancy_detail", args=[vacancy.slug]),
        )

    def test_vacancy_string_representation(self):
        vacancy = Vacancy.objects.create(
            title="Test Vacancy",
            vacancy_type=self.vacancy_type,
            pay_grade="PG1",
            content="<p>This is a test vacancy</p>",
            deadline="2023-03-01 12:00:00",
            is_public=True,
        )
        vacancy.town.set([self.town])
        self.assertEqual(str(vacancy), "Test Vacancy")

    def test_vacancy_verbose_name_plural(self):
        self.assertEqual(Vacancy._meta.verbose_name_plural, "Vacancies")

    def test_vacancy_fields(self):
        deadline_date = datetime.strptime("2023-03-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        vacancy = Vacancy.objects.create(
            title="Test Vacancy",
            vacancy_type=self.vacancy_type,
            pay_grade="PG1",
            content="<p>This is a test vacancy</p>",
            deadline=deadline_date,
            is_public=True,
        )
        vacancy.town.set([self.town])
        self.assertIsInstance(vacancy.id, uuid.UUID)
        self.assertIsInstance(vacancy.title, str)
        self.assertIsInstance(vacancy.vacancy_type, VacancyType)
        self.assertIsInstance(vacancy.pay_grade, str)
        self.assertIsInstance(vacancy.content, str)
        self.assertIsInstance(vacancy.town.all()[0], Town)
        self.assertIsInstance(vacancy.deadline, datetime)
        self.assertIsInstance(vacancy.is_public, bool)

    def test_vacancy_fields_max_length(self):
        vacancy = Vacancy.objects.create(
            title="Test Vacancy",
            vacancy_type=self.vacancy_type,
            pay_grade="PG1",
            content="<p>This is a test vacancy</p>",
            deadline="2023-03-01 12:00:00",
            is_public=True,
        )
        vacancy.town.set([self.town])
        title_field = Vacancy._meta.get_field("title")
        pay_grade_field = Vacancy._meta.get_field("pay_grade")
        self.assertEqual(title_field.max_length, 255)
        self.assertEqual(pay_grade_field.max_length, 3)

    def test_vacancy_fields_blank(self):
        vacancy = Vacancy.objects.create(
            title="Test Vacancy",
            vacancy_type=self.vacancy_type,
            pay_grade="PG1",
            content="<p>This is a test vacancy</p>",
            deadline="2023-03-01 12:00:00",
            is_public=True,
        )
        vacancy.town.set([self.town])
        advert_field = Vacancy._meta.get_field("advert")
        remarks_field = Vacancy._meta.get_field("remarks")
        self.assertTrue(advert_field.blank)
        self.assertTrue(remarks_field.blank)

    def test_vacancy_fields_null(self):
        vacancy = Vacancy.objects.create(
            title="Test Vacancy",
            vacancy_type=self.vacancy_type,
            pay_grade="PG1",
            content="<p>This is a test vacancy</p>",
            deadline="2023-03-01 12:00:00",
            is_public=True,
        )
        vacancy.town.set([self.town])
        field = Vacancy._meta.get_field("vacancy_type")
        self.assertTrue(field.null)
