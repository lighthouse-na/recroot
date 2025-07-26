from django.test import TestCase
from apps.recruitment.forms import ApplicationContactForm
from apps.recruitment.models import Application, Vacancy
from phonenumber_field.phonenumber import PhoneNumber
from datetime import date

class ApplicationContactFormTest(TestCase):

    def setUp(self):
        self.vacancy = Vacancy.objects.create(title="Test Vacancy", deadline="2025-12-31")

    def test_form_valid_data(self):
        form = ApplicationContactForm(data={
            'primary_contact': '+264811234567',
            'secondary_contact': '+264817654321',
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_primary_contact(self):
        form = ApplicationContactForm(data={
            'primary_contact': 'invalid_number',
            'secondary_contact': '+264817654321',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('primary_contact', form.errors)

    def test_form_empty_primary_contact(self):
        form = ApplicationContactForm(data={
            'primary_contact': '',
            'secondary_contact': '+264817654321',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('primary_contact', form.errors)

    def test_form_empty_secondary_contact(self):
        form = ApplicationContactForm(data={
            'primary_contact': '+264811234567',
            'secondary_contact': '',
        })
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        application = Application.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            primary_contact="+264811111111",
            secondary_contact="+264812222222",
            date_of_birth=date(2000, 1, 1),
            vacancy=self.vacancy
        )
        form = ApplicationContactForm(instance=application, data={
            'primary_contact': '+264813333333',
            'secondary_contact': '+264814444444',
        })
        self.assertTrue(form.is_valid())
        form.save()
        application.refresh_from_db()
        self.assertEqual(application.primary_contact, PhoneNumber.from_string("+264813333333"))
        self.assertEqual(application.secondary_contact, PhoneNumber.from_string("+264814444444"))