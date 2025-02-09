from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    primary_contact = PhoneNumberField(
        region="NA",
        help_text="Enter a valid Namibian phone number",
    )
    secondary_contact = PhoneNumberField(
        region="NA",
        blank=True,
        help_text="Enter a valid Namibian phone number",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """Generate a random password and send an email if a new user is created."""
        is_new = self.pk is None

        if is_new:
            random_password = get_random_string(length=12)
            self.set_password(random_password)
            self.send_welcome_email(random_password)

        super().save(*args, **kwargs)

    def send_welcome_email(self, password):
        """Send an email with login details to the new user."""
        subject = "Welcome to Our Platform"
        message = f"""
        Hi {self.first_name},

        Your account has been created successfully. Here are your login details:

        Email: {self.email}
        Password: {password}

        Please log in and change your password as soon as possible.

        Regards,
        The Team
        """
        send_mail(
            subject,
            message,
            "no-reply@telecom.na",  # Replace with your actual sender email
            [self.email],
            fail_silently=False,
        )
