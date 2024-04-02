from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.
class CustomUserModel(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^\+?[\d\-]+\b", message="Enter a valid phone number."
            )
        ],
    )
