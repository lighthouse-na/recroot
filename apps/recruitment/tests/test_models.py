from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.recruitment.models import VacancyType


class VacancyTypeTestCase(TestCase):
    def test_vacancy_type_creation(self):
        # Test creating a new VacancyType instance
        vacancy_type = VacancyType.objects.create(
            type=VacancyType.VACANCY_TYPE.INTERNSHIP
        )
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
        vacancy_type = VacancyType.objects.create(
            type=VacancyType.VACANCY_TYPE.INTERNSHIP
        )
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
