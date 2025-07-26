from django.test import TestCase, Client
from django.urls import reverse
from apps.recruitment.models import Application, Vacancy
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class ApplicationContactUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(email='admin@example.com', password='password')
        self.client.force_login(self.user)
        self.vacancy = Vacancy.objects.create(title="Test Vacancy", deadline="2025-12-31")
        self.application = Application.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            primary_contact="+264811111111",
            secondary_contact="+264812222222",
            date_of_birth=date(2000, 1, 1),
            vacancy=self.vacancy
        )
        self.url = reverse('recruitment:application_contact_update', args=[self.application.pk])

    def test_get_request(self):
        response = self.client.get(self.url, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruitment/application/contact_form.html')
        self.assertContains(response, "Edit Contact Information")
        self.assertContains(response, "081 111 1111")
        self.assertContains(response, "081 222 2222")

    def test_post_valid_data(self):
        data = {
            'primary_contact': '+264813333333',
            'secondary_contact': '+264814444444',
        }
        response = self.client.post(self.url, data, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.application.refresh_from_db()
        self.assertEqual(self.application.primary_contact, PhoneNumber.from_string("+264813333333"))
        self.assertEqual(self.application.secondary_contact, PhoneNumber.from_string("+264814444444"))
        self.assertIn('HX-Trigger', response.headers)
        self.assertIn('HX-Refresh', response.headers)

    def test_post_invalid_data(self):
        data = {
            'primary_contact': 'invalid',
            'secondary_contact': '+264814444444',
        }
        response = self.client.post(self.url, data, HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid phone number (e.g. 061 221 234) or a number with an international call prefix.")
        self.application.refresh_from_db()
        self.assertEqual(self.application.primary_contact, PhoneNumber.from_string("+264811111111"))

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302) # Redirect to login
